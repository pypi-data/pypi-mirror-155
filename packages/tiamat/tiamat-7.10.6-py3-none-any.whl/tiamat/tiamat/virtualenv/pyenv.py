"""
Create and manage the venvs used for build environments.
"""
import os
import pathlib
import shutil
import sys
from typing import List

__func_alias__ = {"bin_": "bin"}


def pyenv_bin(hub, timeout=300):
    """
    Return the full path to pyenv and root
    """
    pyenv = shutil.which("pyenv")
    if not pyenv:
        user_home = pathlib.Path().home()
        pyenv = user_home / ".pyenv" / "bin" / "pyenv"
        if sys.platform == "win32":
            pyenv = user_home / ".pyenv" / "pyenv-win" / "bin" / "pyenv.bat"

    if sys.platform == "win32":
        if not isinstance(pyenv, pathlib.Path):
            pyenv = pathlib.Path(pyenv)
        root = str(pyenv.parent.parent)
    else:
        root = hub.tiamat.cmd.run(
            [pyenv, "root"], timeout=timeout, fail_on_error=True
        ).stdout.strip()

    if isinstance(pyenv, pathlib.Path):
        pyenv = str(pyenv)
    return pyenv, root


def bin_(hub, bname: str, vname=None) -> List[str]:
    """
    Ensure that the desired binary version is present and return the path to
    the python bin to call.

    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]
    timeout = opts.get("timeout")
    hub.log.debug(f"config timeout is '{timeout}'")
    pyenv, root = hub.tiamat.virtualenv.pyenv.pyenv_bin(timeout=timeout)
    installed = hub.tiamat.cmd.run(
        [pyenv, "versions"], timeout=timeout, fail_on_error=True
    ).stdout.strip()

    avail = set()
    for line in installed.split("\n"):
        avail.add(line.strip())

    cmd = []
    python_env = hub.tiamat.virtualenv.init.env(bname)
    if opts.pyenv not in avail:
        if "env" not in python_env:
            python_env.append("env")

        if shutil.which("env"):
            cmd = python_env + [
                "PYTHON_CONFIGURE_OPTS=--enable-shared --enable-ipv6",
                "CONFIGURE_OPTS=--enable-shared --enable-ipv6",
            ]

        hub.tiamat.cmd.run(
            cmd
            + [
                pyenv,
                "install",
                opts.pyenv,
            ],
            timeout=timeout,
            fail_on_error=True,
        )
    else:
        hub.log.info(f"Pyenv version {opts.pyenv} already installed")

    pyenv_dir = opts.pyenv
    if vname:
        pyenv_dir = vname
    return python_env + [os.path.join(root, "versions", pyenv_dir, "bin", "python3")]


def create(hub, bname: str):
    """
    Make a virtual environment based on the version of python used to call this script.

    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]
    timeout = opts.get("timeout")
    hub.log.info(f"timeout is '{timeout}'")
    venv_dir = pathlib.Path(opts.venv_dir)
    hub.tiamat.virtualenv.pyenv.bin(bname)
    pyenv, root = hub.tiamat.virtualenv.pyenv.pyenv_bin(timeout=timeout)
    cmd = [
        pyenv,
        "virtualenv",
        opts.pyenv,
        venv_dir.name,
    ]
    hub.tiamat.cmd.run(cmd, timeout=timeout, fail_on_error=True)

    venv_dir.rmdir()
    virt_env_bin = hub.tiamat.virtualenv.pyenv.bin(bname, vname=venv_dir.name)
    # create symlink from pyenv virtualenv directory to tiamat's tmp virt dir
    venv_dir.symlink_to(pathlib.Path(virt_env_bin[-1]).parent.parent)
    return True
