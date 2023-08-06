# -*- coding: utf-8 -*-


import os
from copy import deepcopy
from typing import List

from pytcm.options import Option
from pytcm.utils import execute


class Command:
    def __init__(self, binary: str, opts: List[Option] = ..., cwd: str = ...) -> None:
        """An object that holds the context for a command.

        Parameters
        ----------
            binary: str
                path to the binary to execute
            opts: List[Option]
                list of options to pass to the binary
            cwd: str
                path to the directory where the command is executed
        """
        self._binary = binary
        self._opts = opts if opts != ... else []
        self._cwd = cwd if cwd != ... else os.getcwd()
        self._out = None
        self._err = None
        self._returncode = None

    def execute(self) -> None:
        """Execute the command. Sets the out, err and returncode properties."""
        self._out, self._err, self._returncode = execute(
            self._binary, self._opts, self._cwd
        )

    @property
    def binary(self) -> str:
        """Path to the binary to execute."""
        return self._binary

    @property
    def opts(self) -> List[Option]:
        """List of options passed to the binary."""
        return deepcopy(self._opts)

    @property
    def cwd(self) -> str:
        """Path to the directory where the command is executed."""
        return self._cwd

    @property
    def out(self) -> str:
        """Represents the stdout of the last executed command.
        Default is None.
        """
        return self._out

    @property
    def err(self) -> str:
        """Represents the stderr of the last executed command.
        Default is None.
        """
        return self._err

    @property
    def returncode(self) -> int:
        """Represents the return code of the last executed command.
        Default is None.
        """
        return self._returncode
