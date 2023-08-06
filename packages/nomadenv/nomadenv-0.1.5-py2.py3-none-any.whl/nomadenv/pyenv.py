import os
import shutil
import subprocess
from .utils import get_output

PYENV_ROOT = os.path.expanduser("~/.nomadenv/pyenv")
ENV = {
    "PYENV_ROOT": PYENV_ROOT,
    "PATH": os.path.join(PYENV_ROOT, "bin") + ":" + os.environ["PATH"],
}

def ensure_pyenv_version(version):
    if version not in get_pyenv_versions():
        subprocess.check_call(["/bin/bash", "-c", "pyenv install {}".format(version)], env=ENV)
    return get_pyenv_version_path(version)

def ensure_pyenv_installed():
    if not os.path.exists(PYENV_ROOT):
        pyenv_install()

def pyenv_install():
    subprocess.check_call(["git", "clone", "--depth", "1", "https://github.com/pyenv/pyenv.git", "-b", "v2.3.1", PYENV_ROOT])

def get_pyenv_versions():
    return filter(None, list(v.strip() for v in get_output(["/bin/bash", "-c", "pyenv versions --bare"], env=ENV).split("\n")))

def get_pyenv_version_path(version):
    return get_output(["/bin/bash", "-c", "pyenv prefix {}".format(version)], env=ENV).strip()

def reset_pyenv():
    shutil.rmtree(PYENV_ROOT)