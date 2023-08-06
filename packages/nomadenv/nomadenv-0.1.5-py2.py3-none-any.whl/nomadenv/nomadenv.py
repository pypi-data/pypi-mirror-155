import os
import re
import sys
import json
import glob
import logging
import shutil
import subprocess

from pprint import pprint

from .utils import get_output
from .pyenv import (
    get_pyenv_versions,
    ensure_pyenv_installed,
    ensure_pyenv_version,
)

DIR = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger(__name__)

SITECUSTOMIZE=os.path.join(DIR, "resources", "sitecustomize.py")

TEST_SCRIPTMAKER_SCRIPT = os.path.join(DIR, "resources", "test_scriptmaker.py")

def get_python_version(executable):
    return list(int(v) for v in get_output([executable, "-c", 'import sys;print("{}.{}.{}".format(*sys.version_info))']).strip().split("."))

def get_sysconfig_prefix(executable):
    return get_output([executable, "-c", 'import sysconfig;print(sysconfig.get_config_vars()["prefix"])']).strip()

def get_prefix(executable):
    return get_output([executable, "-c", 'import sys;print(sys.prefix)']).strip()

def get_site_packages(executable):
    return json.loads(get_output([executable, "-c", 'import site, json;print(json.dumps(site.getsitepackages()))']).strip())

def get_sys_path(executable):
    return json.loads(get_output([executable, "-c", 'import sys, json;print(json.dumps(sys.path))']).strip())

def resolve_executable(executable):
    if os.path.isdir(executable):
        executable = os.path.join(executable, "bin", "python")
    if os.path.islink(executable):
        executable = os.path.realpath(executable)
    return executable

textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))
def patch_shebangs(prefix):
    bin_dir = os.path.join(prefix, "bin")
    for executable in os.listdir(bin_dir):
        executable_path = os.path.join(bin_dir, executable)
        if os.path.islink(executable_path):
            continue
        with open(executable_path, "rb") as f:
            if is_binary_string(f.read(1024)):
                continue
        patch_file_shebang(executable_path)

def get_python_from_dir(directory):
    python = glob.glob(os.path.join(directory, "python?.?"))
    return sorted(python)[-1]

def test_scriptmaker(python):
    get_output([python, TEST_SCRIPTMAKER_SCRIPT])

SHEBANG_REG = re.compile("^#!(?P<executable>.+)\n('''(?P<args>[\w' $()\"-/@]+\n?)\n' ''')?", re.MULTILINE)
def patch_file_shebang(executable_path, dry=False):
    executable_path = os.path.abspath(executable_path)
    logging.info("Patching Shebang of \"{}\"".format(executable_path))
    with open(executable_path) as f:
        data = f.read()
    m = SHEBANG_REG.search(data)
    if not m:
        raise Exception("Shebang of \"{}\" doesn't match pattern {}".format(executable_path, repr(SHEBANG_REG.pattern)))
    fields = m.groupdict()
    if fields["executable"] in ["/bin/bash", "/bin/sh"] and fields["args"] is None:
        return False
    if not "python" in fields["executable"]:
        if "python" not in (fields.get("args") or ""):
            raise Exception("Not a python shebang in file \"{}\".".format(executable_path))
    prefix = os.path.dirname(os.path.dirname(executable_path))
    python = get_python_from_dir(os.path.dirname(executable_path))
    python = os.path.relpath(python, prefix)
    data = """#!/bin/sh
'''exec' $(dirname $(dirname "$(readlink -f "$0")"))/{} "$0" "$@"
' '''\n""".format(python) + data[m.end():]
    if dry:
        print(data)
    else:
        with open(executable_path, "w") as f:
            f.write(data)


def create_env(destination, python_version=None, force=False):
    destination = os.path.abspath(destination)
    ensure_pyenv_installed()
    source_prefix = ensure_pyenv_version(python_version)
    source_python = os.path.join(source_prefix, "bin", "python")
    if os.path.islink(source_python):
        source_python = os.path.realpath(source_python)
    
    if os.path.exists(destination):
        if force:
            shutil.rmtree(destination)
        else:
            raise Exception("Destination already exists \"{}\".".format(destination))
    logger.info("Creating Environnement using \"{}\".".format(source_python))
    shutil.copytree(source_prefix, destination, symlinks=True)
    dest_python = os.path.join(destination, os.path.relpath(source_python, source_prefix))
    version_info = get_python_version(dest_python)
    sitecustomize_dest = os.path.join(destination, "lib", "python{}.{}".format(version_info[0], version_info[1]), "site-packages", "sitecustomize.py")
    if not os.path.exists(os.path.dirname(sitecustomize_dest)):
        os.makedirs(os.path.dirname(sitecustomize_dest))
    print(sitecustomize_dest)
    shutil.copy(SITECUSTOMIZE, sitecustomize_dest)
    test_scriptmaker(dest_python)
    patch_sysconfigdata(dest_python, destination)
    patch_shebangs(destination)
    pip_package = "pip"
    setuptools_package = "setuptools"
    if version_info[0] == 2:
        pip_package = "pip<21.0.0"
        setuptools_package = "setuptools<45.0.0"
    subprocess.check_call([dest_python, "-m", "pip", "install", "--upgrade", "--force-reinstall", pip_package, setuptools_package])
    test_env(dest_python)
    


def test_env(python):
    # python = os.path.join(envpath, "bin", "python")
    # pip = os.path.join(envpath, "bin", "pip")
    subprocess.check_call([python, "--version"])
    subprocess.check_call([python, "-c", "import sys;print(sys.exec_prefix)"])
    # subprocess.check_call([pip, "--version"])

def get_sysconfigdata_path(python):
    version_info = get_python_version(python)
    if version_info[0] >= 3:
        return get_output([python, "-c", "import sysconfig;import importlib;print(importlib.import_module(sysconfig._get_sysconfigdata_name()).__file__)"]).strip()
    else:
        return get_output([python, "-c", "import _sysconfigdata;print(_sysconfigdata.__file__)"]).strip()

def patch_sysconfigdata(python, destination):
    version_info = get_python_version(python)
    prefix = get_prefix(python)
    sysconfig_prefix = get_sysconfig_prefix(python)
    sysconfigdata_path = get_sysconfigdata_path(python).replace(sysconfig_prefix, destination)
    base, ext = os.path.splitext(sysconfigdata_path)
    sysconfigdata_bkp_path = base + "_bkp" + ext
    if not os.path.exists(sysconfigdata_bkp_path):
        shutil.copy(sysconfigdata_path, sysconfigdata_bkp_path)
    exec_prefix = get_sysconfig_prefix(python)
    data = ""
    if sys.version_info[0] >=3:
        try:
            with open(sysconfigdata_bkp_path, encoding="utf-8") as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            with open(sysconfigdata_bkp_path, encoding="latin-1") as f:
                lines = f.readlines()
    else:
        with open(sysconfigdata_bkp_path) as f:
            lines = f.readlines()
    data += lines.pop(0)
    data += "import sys\n"
    for l in lines:
        if l.startswith("build_time_vars = {"):
            l = "_" + l
        data += l.replace(exec_prefix, "${EXEC_PREFIX}")
    data += "build_time_vars = {}\n"
    data += "for key, value in _build_time_vars.items():\n"
    data += "    if isinstance(value, str):\n"
    data += "        value = value.replace(\"${EXEC_PREFIX}\", sys.exec_prefix)\n"
    data += "    build_time_vars[key] = value\n"
    data += "del _build_time_vars\n"
    with open(sysconfigdata_path, 'w') as f:
        f.write(data)