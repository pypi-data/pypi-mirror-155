from . import preprocessing as process
from subprocess import call
import os
from .resources.locator import locate_devconsole

def makelib(src: str, out: str) -> int:
    path = locate_devconsole()
    process.generate_header(src)
    source = src.split('.')[-2] + "_.c"
    call(f"cd \"{out}\" && \"{path}\" && cl -LD \"{source}\"", shell=True)
    return 0
def build(src: str, out: str):
    path = locate_devconsole()
    call(f"cd \"{out}\" && \"{path}\" cl \"{src}\"", shell=True)


if __name__ == "__main__":
    build("./tests/add.c", './tests/build')
