#!/usr/bin/env python3
from __future__ import annotations
import pathlib,shutil,subprocess,hashlib,json,concurrent.futures,datetime,stat,os
R=pathlib.Path(__file__).resolve().parent; D=R/'dataset-lane/ccg';orig=next((D/'source').iterdir());out=D/'reproducible-debug-prefixmap-check'
assert not out.exists()
out.mkdir()
orig_source_files={p.relative_to(orig).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in orig.rglob('*') if p.is_file()}
assert len(orig_source_files)>=15

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def cmd(args,cwd=None,timeout=120):
 p=subprocess.run(args,cwd=cwd,capture_output=True,text=True,timeout=timeout);return {'argv':list(map(str,args)),'status':p.returncode,'stdout':p.stdout[-1000:],'stderr':p.stderr[-2000:]}
def build(suffix):
 src=out/('source-'+suffix);shutil.copytree(orig,src,symlinks=True)
 before={p.relative_to(src).as_posix():sha(p) for p in src.rglob('*') if p.is_file()};assert before==orig_source_files
 flags=f'-c -g -pipe -Wall -Wextra -std=c11 -fdebug-prefix-map={src}=. -ffile-prefix-map={src}=.'
 p=cmd(['make','-j4',f'CFLAGS={flags}'],cwd=src)
 if p['status']!=0:return {'id':suffix,'build':p,'source_files_unchanged_before':True}
 binary=src/'ccg';version=cmd([str(binary),'--version']);seed=cmd([str(binary),'--seed','1000','--max-functions','3','--max-localvars','3','--max-function-parameters','3','--min-statements-per-block','1','--max-statements-per-block','3','--max-expression-nesting','3','--max-block-nesting','3','--max-pointer-depth','2','--no-omitted-operand-conditional'])
 return {'id':suffix,'build':p,'source_files_unchanged_before':True,'sha256':sha(binary),'bytes':binary.stat().st_size,'mode':oct(binary.stat().st_mode&0o777),'version':version,'seed_1000':seed}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex: pair=list(ex.map(build,['C','D']))
assert all(x['build']['status']==0 and x['version']['status']==0 and x['seed_1000']['status']==0 for x in pair)
old=[]
for suffix in ['A','B']:
 src=D/('prefix-'+suffix)/'bin/ccg';copy=out/('old-'+suffix+'-stripdebug');shutil.copy2(src,copy)
 p=cmd(['strip','--strip-debug',str(copy)])
 assert p['status']==0
 old.append({'orig_sha256':sha(src),'orig_bytes':src.stat().st_size,'stripped_sha256':sha(copy),'stripped_bytes':copy.stat().st_size,'status':p['status']})
assert old[0]['orig_sha256']!=old[1]['orig_sha256']
report={'format':'cpg-independent-CCG-native-compiler-reproducible-C-D-source-build-v1','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate_no_resource_qualification_added':True,'original_source_commit':'108f4304f9b2f187173a44749b56b3eb64dd4590','original_input_sha256':'5ce850a78f49665919ccdcb0fe759827c039e49632695f35b4a47d59c6c915b9','host':{'os':'Debian 13 Linux x86_64','compiler':cmd(['gcc','--version'])['stdout'].splitlines()[0]},'builds':pair,'normalized_binary_identical':pair[0]['sha256']==pair[1]['sha256'],'generated_seed_identical':pair[0]['seed_1000']['stdout']==pair[1]['seed_1000']['stdout'],'old_A_B_builds_with_upstream_flags':old,'old_A_B_strip_debug_identical':old[0]['stripped_sha256']==old[1]['stripped_sha256'],'original_source_tree_unchanged':orig_source_files=={p.relative_to(orig).as_posix():sha(p) for p in orig.rglob('*') if p.is_file()},'OCI_Ubuntu_24_04_qualified':False,'generated_C_programs_executed':False,'binary_from_this_new_build_is_not_in_earlier_saved_newSHA_zip':True}
(R/'release/compiler-playground-20261031T1003-independent-CCG-debug-prefix-map-source-reproducibility.json').write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
print(json.dumps({'original_A_B_with_upstream_compiler_flags_equal':old[0]['orig_sha256']==old[1]['orig_sha256'],'original_A_B_after_debug_strip_equal':report['old_A_B_strip_debug_identical'],'normalized_C_D_bit_identical':report['normalized_binary_identical'],'C_D_generated_seed_1000_identical':report['generated_seed_identical'],'C_D_SHA256':[x.get('sha256') for x in pair]},indent=2))
