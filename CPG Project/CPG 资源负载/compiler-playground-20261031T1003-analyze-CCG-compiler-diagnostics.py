#!/usr/bin/env python3
import pathlib,hashlib,json,concurrent.futures,subprocess,collections,datetime
r=pathlib.Path(__file__).resolve().parent;d=r/'dataset-lane/ccg/generated-compile-only';src=sorted(d.glob('seed-*.c'))
assert len(src)==24

def run(pair):
 f,flags=pair
 p=subprocess.run(flags+[str(f)],capture_output=True,text=True,timeout=30)
 return {'source':f.name,'source_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'cmd':flags+[str(f)],'status':p.returncode,'stderr':p.stderr[-2500:],'stdout':p.stdout[-200:]}
profiles={'gcc14_original':['gcc','-std=c11','-fsyntax-only','-w'],
 'gcc14_Wno_error_incompatible_pointer':['gcc','-std=c11','-fsyntax-only','-w','-Wno-error=incompatible-pointer-types'],
 'gcc14_Wno_error_incompatible_pointer_int':['gcc','-std=c11','-fsyntax-only','-w','-Wno-error=incompatible-pointer-types','-Wno-error=int-conversion'],
 'clang_original':['clang','-std=c11','-fsyntax-only','-w'],
 'clang_strict_incompatible_pointer':['clang','-std=c11','-fsyntax-only','-Werror=incompatible-pointer-types']}
res={}
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
 for key,flags in profiles.items():
  vals=list(ex.map(run,[(p,flags) for p in src]));assert len(vals)==24
  res[key]={'pass':sum(x['status']==0 for x in vals),'fail':sum(x['status']!=0 for x in vals),'results':vals}
assert res['clang_original']['pass']==24 and res['gcc14_original']['pass']==15
report={'format':'cpg-source-generated-CCG-GCC14-vs-Clang-C11-diagnostic-study-v1','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pure_compile_syntax_only_no_run':True,'generated_under_exact_original_CCG_commit':'108f4304f9b2f187173a44749b56b3eb64dd4590','source_program_files':24,'all_source_SHA_verified':True,'profiles':res,'gcc14_version':subprocess.run(['gcc','--version'],capture_output=True,text=True).stdout.splitlines()[0],'clang_version':subprocess.run(['clang','--version'],capture_output=True,text=True).stdout.splitlines()[0],'success_not_proof_of_defined_runtime_behavior':True,'original_programs_executed':False,'CCG_qualification_increment':0,'formal_coverage_increment':0}
out=r/'release/compiler-playground-20261031T1003-independent-CCG-generated-program-GCC14-Clang-diagnostic-differences.json';out.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print({k:{'pass':v['pass'],'fail':v['fail']} for k,v in res.items()})
