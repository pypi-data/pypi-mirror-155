import subprocess
import sys

def get_output(cmd, **kwargs):
    if sys.version_info[0] >= 3:
        kwargs["encoding"] = "utf-8"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
    returncode = p.wait()
    if returncode:
        raise Exception("Something went wrong:\n{}".format(p.stderr.read()))
    return p.stdout.read()