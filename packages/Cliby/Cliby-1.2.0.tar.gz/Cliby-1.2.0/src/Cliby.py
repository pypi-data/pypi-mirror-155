import os
from windows.builder import makelib as wlib
from linux.build import makelib as llib
import sys


def make(src: str, out: str) -> int:
    # If windows, use windows\build.py
    if os.name == "nt":
        wlib(src, out)
    # If linux, use linux\build.py 
    else:
        llib(src, out)

def main():
    args = sys.argv
    print(f"makeing {args[1]} to {args[2]}")
    make(args[1], args[2])