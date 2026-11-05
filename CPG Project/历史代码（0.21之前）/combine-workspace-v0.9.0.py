#!/usr/bin/env python3
"""Split or reassemble the complete ZIP with per-part and full-file SHA-256.

No dependencies, network requests, decompression, or execution of archive code.
The same script works with Python 3.11+ on Linux, macOS, and Windows.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile


def file_sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def filename(value):
    if (not isinstance(value, str) or value in (".", "..")
            or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", value) is None
            or value.endswith(".")
            or value.split(".", 1)[0].upper() in {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}):
        raise ValueError("Manifest filenames must be ordinary portable basenames")
    return value


def digest(value):
    if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{64}", value) is None:
        raise ValueError("Invalid SHA-256 in parts manifest")
    return value


def split_archive(archive, directory, *, part_bytes=40 * 1024 * 1024):
    archive, directory = Path(archive), Path(directory)
    if not archive.is_file() or archive.is_symlink():
        raise ValueError("Input must be a regular archive file")
    if type(part_bytes) is not int or part_bytes <= 0:
        raise ValueError("part_bytes must be a positive integer")
    filename(archive.name)
    if directory.exists() or directory.is_symlink():
        raise FileExistsError("Use a new parts directory")
    directory.mkdir(parents=True)
    rows, whole, total = [], hashlib.sha256(), 0
    with archive.open("rb") as source:
        index = 1
        while True:
            chunk = source.read(min(part_bytes, 1024 * 1024))
            if not chunk:
                break
            name = archive.name + f".{index:03d}"
            part_sha, written = hashlib.sha256(), 0
            with (directory / name).open("xb") as target:
                while chunk:
                    target.write(chunk); whole.update(chunk); part_sha.update(chunk)
                    written += len(chunk); total += len(chunk)
                    if written == part_bytes:
                        break
                    chunk = source.read(min(part_bytes - written, 1024 * 1024))
            rows.append({"file": name, "bytes": written, "sha256": part_sha.hexdigest()})
            index += 1
    if not rows:
        raise ValueError("Cannot split an empty archive")
    document = {"schema_version": 1, "archive": archive.name, "bytes": total,
                "sha256": whole.hexdigest(), "parts": rows,
                "format": "Raw consecutive chunks of one ZIP; combine before extracting"}
    manifest = directory / "parts.json"
    manifest.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    shutil.copyfile(Path(__file__), directory / "multipart_workspace.py")
    return {"manifest": str(manifest.resolve()), "archive_sha256": whole.hexdigest(),
            "bytes": total, "part_count": len(rows), "part_bytes": part_bytes}


def read_manifest(path):
    path = Path(path)
    def unique(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("Duplicate key in parts manifest")
            result[key] = value
        return result
    data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)
    if (data.get("schema_version") != 1 or type(data.get("bytes")) is not int
            or data["bytes"] <= 0 or not isinstance(data.get("parts"), list) or not data["parts"]):
        raise ValueError("Invalid parts manifest")
    filename(data["archive"]); digest(data["sha256"])
    seen = set()
    for index, row in enumerate(data["parts"], 1):
        name = filename(row["file"]); digest(row["sha256"])
        if (name != data["archive"] + f".{index:03d}" or name.casefold() in seen
                or type(row["bytes"]) is not int or row["bytes"] <= 0):
            raise ValueError("Invalid, duplicate or out-of-order part")
        seen.add(name.casefold())
    if sum(row["bytes"] for row in data["parts"]) != data["bytes"]:
        raise ValueError("Part sizes do not add up to the archive size")
    return data


def combine_parts(manifest, output=None):
    manifest = Path(manifest)
    data = read_manifest(manifest)
    output = Path(output) if output is not None else manifest.parent / data["archive"]
    if output.exists() or output.is_symlink():
        raise FileExistsError("Refusing to overwrite an existing destination")
    output.parent.mkdir(parents=True, exist_ok=True)
    handle, name = tempfile.mkstemp(prefix=".cpg-join-", dir=output.parent)
    temporary = Path(name)
    whole = hashlib.sha256()
    try:
        with os.fdopen(handle, "wb") as target:
            for row in data["parts"]:
                path = manifest.parent / row["file"]
                if path.is_symlink() or not path.is_file() or path.stat().st_size != row["bytes"]:
                    raise ValueError("Missing, linked or truncated part: " + row["file"])
                part_sha, size = hashlib.sha256(), 0
                with path.open("rb") as source:
                    for block in iter(lambda: source.read(1024 * 1024), b""):
                        target.write(block); whole.update(block); part_sha.update(block); size += len(block)
                if size != row["bytes"] or part_sha.hexdigest() != row["sha256"]:
                    raise ValueError("Part checksum mismatch: " + row["file"])
            target.flush(); os.fsync(target.fileno())
        if temporary.stat().st_size != data["bytes"] or whole.hexdigest() != data["sha256"]:
            raise ValueError("Combined archive checksum mismatch")
        # Same-directory hard-link publication is atomic and refuses to replace
        # a concurrently created destination. No second copy can leave a partial
        # final ZIP on interruption or ENOSPC. Use an ext4/XFS/APFS/NTFS-like
        # filesystem supporting hard links; unsupported filesystems fail cleanly.
        os.link(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)
    return {"status": "passed", "archive": str(output.resolve()),
            "bytes": data["bytes"], "sha256": whole.hexdigest(), "parts_verified": len(data["parts"])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    make = sub.add_parser("split")
    make.add_argument("archive", type=Path); make.add_argument("directory", type=Path)
    make.add_argument("--part-mib", type=int, default=40)
    join = sub.add_parser("combine")
    join.add_argument("manifest", type=Path); join.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = (split_archive(args.archive, args.directory, part_bytes=args.part_mib * 1024 * 1024)
              if args.command == "split" else combine_parts(args.manifest, args.output))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
