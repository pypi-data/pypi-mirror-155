import sys
from pip._vendor.distlib.scripts import ScriptMaker
def main():
    right_value = "$(dirname $(dirname \"$(readlink -f \"$0\")\"))/bin/python{}.{}".format(sys.version_info[0], sys.version_info[1])
    if ScriptMaker.executable != right_value:
        raise Exception("pip._vendor.distlib.scripts.ScritpMaker.executable as an invalid value {}. Should be {}.".format(repr(ScriptMaker.executable), repr(right_value)))

if __name__ == "__main__":
    main()