import os
import sys
import argparse
import logging
from .nomadenv import create_env, patch_file_shebang

def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action")
    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("destination", default=".nomadenv", nargs="?", help="Directory to create environment at.")
    create_parser.add_argument("--python-version", help="Source python prefix.")
    create_parser.add_argument("--force", "-f", action="store_true", help="Overrite destination if already exists.")
    
    patch_shebang_parser = subparsers.add_parser("patch-shebang")
    patch_shebang_parser.add_argument("path", nargs="*", help="File or directory to patch.")
    patch_shebang_parser.add_argument("--dry", action="store_true", help="Output result to stdout instead of modifying file.")

    reset_pyenv_parser = subparsers.add_parser("reset-pyenv")
    args = parser.parse_args()

    if args.action == "create":
        create_env(args.destination, python_version=args.python_version, force=args.force)
    elif args.action == "patch-shebang":
        for path in args.path:
            if os.path.isdir(path):
                raise Exception("Directory not supported")
            elif os.path.islink(path):
                raise Exception("Symlinks not supported")
            else:
                patch_file_shebang(path, dry=args.dry)
    elif args.action == "reset-pyenv":
        from .pyenv import reset_pyenv
        reset_pyenv()




if __name__ == "__main__":
    main()