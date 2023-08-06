import os
from subprocess import call, CalledProcessError

def makelib(src: str, out: str) -> int:
    return call(["gcc", "-static", "-shared", "-o", out, src])
def build(src: str, out: str) -> int:
    return call(["gcc", "-o", out, src])