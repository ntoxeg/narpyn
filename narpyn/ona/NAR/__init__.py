# -*- coding: utf-8 -*-
import os
import subprocess
import sys

NARPKG_PATH = os.path.dirname(__file__)


def _program(name: str, args: list[str]) -> int:
    return subprocess.call([os.path.join(NARPKG_PATH, name)] + args, close_fds=False)


def NAR():
    raise SystemExit(_program("NARexe", sys.argv[1:]))
