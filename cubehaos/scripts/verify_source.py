#!/usr/bin/env python3
"""Run available tests on the source; do not claim image readiness."""
import json
import os
from pathlib import Path
import subprocess
import sys
root=Path(__file__).resolve().parents[1]
r=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=root,text=True,capture_output=True)
print(r.stdout)
print(r.stderr,file=sys.stderr)
checks={}
for script in sorted((root/'scripts').glob('*.sh')):
    v=subprocess.run(['bash','-n',str(script)],capture_output=True,text=True)
    checks[script.name]=(v.returncode==0)
    if v.returncode:print(v.stderr,file=sys.stderr)
report={'version':'v0.3','unit_tests_ok':r.returncode==0,'shell_scripts_syntax_ok':all(checks.values()),'scripts_checked':checks,
        'full_os_compiled':False,'real_cube_boot_tested':False,'flashable_firmware_generated_here':False}
(root/'TEST_RESULT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(report,indent=2,ensure_ascii=False))
sys.exit(0 if report['unit_tests_ok'] and report['shell_scripts_syntax_ok'] else 1)
