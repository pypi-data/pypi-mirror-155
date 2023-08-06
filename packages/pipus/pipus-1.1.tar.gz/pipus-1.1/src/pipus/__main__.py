from pathlib import Path
import shutil
import subprocess
import site
import sys

from .args import args, parser


INSTALL_CMD = ['pip', 'install', '--user', '-U']


def command(f):
    """
    Decorator for commands, always exit after running, and run abort() on errors
    """

    def wrapped(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except Exception as e:
            abort(str(e))
        exit()
    return wrapped


def run(*argv):
    """Runs a command"""

    result = subprocess.run(argv)
    try:
        result.check_returncode()
    except subprocess.CalledProcessError as e:
        abort(str(e))


def prepare(path: Path = args.file, error=False):
    """Ensures a file exists"""

    if path.exists():
        return
    if error:
        raise FileNotFoundError(path)
    path.touch()


def ask(msg: str = None):
    """Asks for user's permission before continuing"""

    if args.yes:
        return
    if msg:
        print(msg)
    reply = input("Proceed? [y/N] ")
    if not (reply and 'yes'.startswith(reply.lower())):
        abort("Aborted by user")


def get_pkgs():
    """Retrieves packages from the packages file"""

    try:
        prepare(error=args.no_write)
    except Exception:
        abort(f"No packages list file. Create {args.file} before running.")
    with args.file.open() as f:
        return [
            x for x in f.read().splitlines(keepends=False)
            if x and not x.strip().startswith('#')
        ]


def save_pkgs(l):
    """Writes the packages file"""

    if args.no_write:
        warn("Not writting packages list because we were asked not to")
        return
    pkgs = set(sorted(l))
    with args.file.open('w') as f:
        f.write('\n'.join(pkgs) + '\n')


def abort(msg: str = None, code=1):
    """Exits with an error"""

    if msg:
        print(msg, file=sys.stderr)
    sys.exit(code)


def exit():
    """Gracefully exits"""

    sys.exit(0)


def warn(msg: str):
    """Writes warning messages to stderr"""

    print("WARNING:", msg, file=sys.stderr)


@command
def update():
    if not get_pkgs():
        warn("Packages list is empty, nothing to do!")
        return
    run(*INSTALL_CMD, '-r', args.file)


@command
def install(packages: list[str]):
    run(*INSTALL_CMD, *packages)
    if args.no_write:
        return
    pkgs = get_pkgs()
    for package in packages:
        pkgs.append(package)
    save_pkgs(pkgs)


@command
def uninstall(packages: list[str]):
    try:
        pkgs = get_pkgs()
    except Exception:
        pkgs = []
    for package in packages:
        pkgs.remove(package)
    save_pkgs(pkgs)
    refresh()


@command
def refresh():
    path = site.getusersitepackages()
    ask(f"This will delete all installed packages in {path} before attempting to install all packages picked up by {__package__}")
    shutil.rmtree(path)
    print("Deleted", path)
    update()


@command
def print_list():
    print('\n'.join(get_pkgs()))


def main():
    if args.quiet:
        INSTALL_CMD.append('-q')

    if args.verbose:
        INSTALL_CMD.append('-vvv')

    if args.help:
        parser.print_help()
        exit()

    if args.list:
        print_list()

    if args.refresh:
        refresh()

    if args.remove:
        if not args.packages:
            abort("You must specify which packages to remove")
        if args.no_write:
            abort("Uninstalling is incompatible with not writing changes")
        uninstall(args.packages)

    if args.packages:
        install(args.packages)

    if args.update or not args.packages:
        update()


if __name__ == '__main__':
    main()
