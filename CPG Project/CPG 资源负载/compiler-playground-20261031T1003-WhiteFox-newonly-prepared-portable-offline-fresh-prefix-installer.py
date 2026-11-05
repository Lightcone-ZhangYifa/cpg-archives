#!/usr/bin/env python3
"""Install saved, prepared WhiteFox source-only CPG Datasets offline in a BRAND-NEW prefix.
Inputs: immutable inherited original pinned tar (not republished), new delta-only
prepared SQLite archive, new exact local adapter, and explicit immutable hashes.
No compiler, model, pip, apt, network, system paths or source-index rebuild.
"""
from __future__ import annotations
import argparse,datetime,hashlib,importlib.metadata,json,os,stat,sys,tarfile,time,zipfile
from pathlib import Path,PurePosixPath

ORIG_ROOT='WhiteFox-e402f40e90184f3c24c2358d62730dfbf4e2c9be'
ORIG_SHA='010b736b9b802f20a5177ff259dcb9b02e69ce42335a600d05831b20ff3e615a'
ORIG_BYTES=10870539
ADAPTER_SHA='6d23393dd1a6430b5153d7d68b21b282ff81f4eac754867f57f52bbd8e15123a'
NEW_INDEX_SHA='3112530239a94c0c1a0b2c6cb5ae6c217c8de779286251e825dd671154fb1fa5'
NEW_INDEX_BYTES=12669309
NUM_TAR=80632;NUM_FILES=74313;NUM_BYTES=114892921

def sha(p:Path):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def main():
 p=argparse.ArgumentParser()
 p.add_argument('--inherited-original-tar',required=True,type=Path)
 p.add_argument('--saved-newonly-prepared-zip',required=True,type=Path)
 p.add_argument('--saved-newonly-prepared-manifest',required=True,type=Path)
 p.add_argument('--saved-derived-adapter-json',required=True,type=Path)
 p.add_argument('--fresh-new-output',required=True,type=Path)
 a=p.parse_args()
 st=time.monotonic()
 if a.fresh_new_output.exists() or a.fresh_new_output.is_symlink():raise FileExistsError('Will not mutate or retry a partially built prefix')
 if (a.inherited_original_tar.stat().st_size,sha(a.inherited_original_tar))!=(ORIG_BYTES,ORIG_SHA):raise ValueError('Inherited original raw tar SHA/bytes wrong')
 if (a.saved_newonly_prepared_zip.stat().st_size,sha(a.saved_newonly_prepared_zip))!=(NEW_INDEX_BYTES,NEW_INDEX_SHA):raise ValueError('New-only stored prepared index ZIP SHA/bytes wrong')
 if sha(a.saved_derived_adapter_json)!=ADAPTER_SHA:raise ValueError('New local CPG adapter SHA wrong')
 manifest=json.loads(a.saved_newonly_prepared_manifest.read_text())
 if (manifest['archive_sha256'],manifest['archive_bytes'])!=(NEW_INDEX_SHA,NEW_INDEX_BYTES):raise ValueError('Saved manifest disagrees with index')
 out=a.fresh_new_output
 out.mkdir(parents=True,exist_ok=False)
 source=out/'source';source.mkdir()
 dirs=[];names=set();nfiles=total=ntar=0
 with tarfile.open(a.inherited_original_tar,'r:gz') as tar:
  for m in tar:
   ntar+=1
   path=PurePosixPath(m.name)
   if path.is_absolute() or not path.parts or '..' in path.parts or '\x00' in m.name or path.parts[0]!=ORIG_ROOT or m.name in names:
    raise ValueError('Unsafe/duplicate/upstream source tar path '+m.name)
   names.add(m.name)
   target=source.joinpath(*path.parts)
   if m.isdir():
    target.mkdir(parents=True,exist_ok=True);dirs.append((target,m.mode&0o777));continue
   if not m.isfile() or m.mode&0o6000 or m.size<0 or m.size>NUM_BYTES:raise ValueError('Unsafe file type/mode/size '+m.name)
   target.parent.mkdir(parents=True,exist_ok=True)
   content=tar.extractfile(m).read()
   if len(content)!=m.size:raise ValueError('Short original source member '+m.name)
   with target.open('xb') as f:f.write(content)
   target.chmod(m.mode&0o777)
   nfiles+=1;total+=len(content)
   if nfiles>NUM_FILES or total>NUM_BYTES:raise ValueError('Upstream original source archive larger than locked inventory')
 for d,mode in sorted(dirs,key=lambda t:len(t[0].parts),reverse=True):d.chmod(mode)
 if (ntar,nfiles,total)!=(NUM_TAR,NUM_FILES,NUM_BYTES):raise ValueError('Original source manifest incomplete')
 adapter=source/ORIG_ROOT/'CPG-LOCAL-SOURCE-ADAPTER.json'
 if adapter.exists():raise ValueError('Upstream source collides with local adapter')
 adapter.write_bytes(a.saved_derived_adapter_json.read_bytes());adapter.chmod(0o644)
 if sha(adapter)!=ADAPTER_SHA:raise ValueError('Local derived adapter copy changed')
 with zipfile.ZipFile(a.saved_newonly_prepared_zip) as z:
  assert len(z.namelist())==manifest['member_count']==len(manifest['members'])
  if len(set(z.namelist()))!=len(z.namelist()):raise ValueError('Duplicate new-only index member')
  for v in manifest['members']:
   name=PurePosixPath(v['name']);i=z.getinfo(v['name']);mode=i.external_attr>>16
   if name.is_absolute() or '..' in name.parts or not stat.S_ISREG(mode) or oct(mode&0o777)!=v['logical_mode']:
    raise ValueError('Unsafe new-only prepared index mode/path')
   content=z.read(v['name'])
   if len(content)!=v['bytes'] or hashlib.sha256(content).hexdigest()!=v['sha256']:
    raise ValueError('Saved prepared member SHA/bytes mismatch '+v['name'])
   target=out.joinpath(*name.parts)
   if target.exists():raise ValueError('Prepared member would overwrite original source')
   target.parent.mkdir(parents=True,exist_ok=True)
   with target.open('xb') as f:f.write(content)
   target.chmod(int(v['logical_mode'],8))
   if sha(target)!=v['sha256'] or stat.S_IMODE(target.stat().st_mode)!=int(v['logical_mode'],8):raise ValueError('Prepared index changed on disk')
 if importlib.metadata.version('compiler-playground')!='0.21.13':raise ValueError('The installed official CPG wheel is not exactly 0.21.13')
 from compiler_playground.datasets.storage import load_from_disk
 verified={}
 for name,count,lang in [('python',61255,'python'),('cxx',173,'c++')]:
  p=out/'indices'/name
  with load_from_disk(p,verify=True,verify_files=True) as ds:
   if len(ds)!=count or ds.purpose!='compile_only' or ds[0].payload['language']!=lang or ds[-1].payload['language']!=lang:
    raise ValueError('Incorrect actual original source-only Dataset '+name)
   verified[name]={'real_actual_qualifying_source_records':len(ds),'fingerprint':ds.fingerprint,
       'source_material_SHA_verified_by_official_CPG':True,'actual_original_source_root_exists':ds.material_root.resolve()==(source/ORIG_ROOT).resolve()}
  if not verified[name]['actual_original_source_root_exists']:raise ValueError('Portable path resolved outside source root')
 output={'format':'cpg-whitefox-only-new-index-offline-independent-actual-original-official-wheel-installed-in-fresh-prefix-v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
  'installed_official_CPG_version':importlib.metadata.version('compiler-playground'),'actual_python':sys.executable,
  'source_archive_inherited_from_0.21.13':True,'upstream_source_archive_SHA256':ORIG_SHA,
  'all_inherited_original_files_restored':nfiles,'all_inherited_original_regular_bytes':total,'original_tar_members':ntar,
  'new_only_prepared_ZIP_SHA256':NEW_INDEX_SHA,'new_only_prepared_ZIP_bytes':NEW_INDEX_BYTES,
  'local_additive_adapter_SHA256':ADAPTER_SHA,'no_index_source_generation_in_this_install':True,
  'no_compilation_or_source_build_performed':True,'actual_offline_verified':verified,'source_model_or_benchmark_execution':False,
  'all_actual_materials_SHA_verified_during_CPG_load':True,'elapsed_sec':round(time.monotonic()-st,2),
  'main_original_1862_resource_cover_unchanged':1700,'main_original_195_dataset_cover_unchanged':88,
  'formal_release_new':False,'new_candidate_cpus_and_models_not_qualified':True}
 receipt=out/'only-new-prepared-source-Datasets-independent-actual-official-wheel-receipt.json'
 receipt.write_text(json.dumps(output,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps({'pass':True,'fresh_prefix':str(out),'original_files':nfiles,'new_original_Python':verified['python']['real_actual_qualifying_source_records'],
    'new_original_CXX':verified['cxx']['real_actual_qualifying_source_records'],'elapsed_sec':output['elapsed_sec']}))

if __name__=='__main__':main()
