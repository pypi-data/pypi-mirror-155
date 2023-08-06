import subprocess
import json
import os
import sys

def locate_devconsole():
    path = os.path.dirname(os.path.abspath(__file__))
    output = subprocess.check_output(f"{path}\\vswhere.exe -products * -format json", shell=True)
    vswhere_output = json.loads(output)
    path = vswhere_output[0]["installationPath"]

    # Set platform to 32-bit if 64-bit is not supported
    if sys.maxsize > 2**32:
        platform = 64
    else:
        platform = 32

    return os.path.join(path, f"VC\\Auxiliary\\Build\\vcvars{platform}.bat")