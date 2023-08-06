# -*- coding: utf-8 -*-


import os
import subprocess
from typing import List, Tuple

from pytcm.options import Option


def execute(binary: str, opts: List[Option], cwd: str = os.getcwd()) -> Tuple[str, str]:
    """Execute a command using options

    WARNING: letting users specify `binary` is unsafe
    """
    c = [binary]
    c.extend([opt.parse() for opt in opts])

    proc = subprocess.Popen(c, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    outs, errs = proc.communicate()

    return outs.decode(), errs.decode()
