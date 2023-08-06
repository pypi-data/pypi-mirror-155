# -*- coding: utf-8 -*-


import os
import subprocess
from collections import namedtuple
from typing import List

from pytcm.options import Option

CommandResult = namedtuple("CommandResult", ["out", "err", "returncode"])


def execute(binary: str, opts: List[Option] = ..., cwd: str = ...) -> CommandResult:
    """Execute a command using options.

    WARNING: letting users specify `binary` is unsafe
    """
    opts = opts if opts != ... else []
    cwd = cwd if cwd != ... else os.getcwd()
    c = [binary]
    c.extend([opt.parse() for opt in opts])

    proc = subprocess.Popen(c, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    out, err = proc.communicate()

    return CommandResult(out.decode(), err.decode(), proc.returncode)
