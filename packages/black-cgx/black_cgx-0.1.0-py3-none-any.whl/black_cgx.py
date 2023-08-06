import logging
from os.path import relpath
from pathlib import Path

import black

try:
    import tomllib
except ImportError:
    import tomli as tomllib
from collagraph.cgx import cgx


logger = logging.getLogger(__name__)


class BadBlackConfig(ValueError):
    """Bad black TOML configuration file."""

    pass


def project_root_config(path):
    project_root, _ = black.find_project_root((path,))
    pyproject_path = project_root / "pyproject.toml"
    return pyproject_path


def load_black_mode_from_config(pyproject_path):
    black_config = {}
    if pyproject_path.is_file():
        try:
            with pyproject_path.open(mode="rb") as toml_file:
                pyproject_toml = tomllib.load(toml_file)
        except ValueError:
            raise BadBlackConfig(relpath(pyproject_path))

        config = pyproject_toml.get("tool", {}).get("black", {})
        black_config = {
            k.replace("--", "").replace("-", "_"): v for k, v in config.items()
        }

    return black.FileMode(
        target_versions={
            black.TargetVersion[val.upper()]
            for val in black_config.get("target_version", [])
        },
        # cast to int explicitly otherwise line length could be a string
        line_length=int(black_config.get("line_length", black.DEFAULT_LINE_LENGTH)),
        string_normalization=not black_config.get("skip_string_normalization", False),
        magic_trailing_comma=not black_config.get("skip_magic_trailing_comma", False),
        preview=bool(black_config.get("preview", False)),
    )


def load_black_mode(path, modes=None):
    pyproject_path = project_root_config(path)
    if pyproject_path not in modes:
        modes[pyproject_path] = load_black_mode_from_config(pyproject_path)

    return modes[pyproject_path]


def format(path, mode=None, check=False):
    """Format CGX files (the contents of the script tag) with black"""
    path = Path(path)
    if path.suffix != ".cgx":
        return

    if mode is None:
        mode = load_black_mode(path, {})

    parser = cgx.CGXParser()
    parser.feed(path.read_text())

    # Find beginning and end of script block
    script_node = parser.root.child_with_tag("script")
    start, end = script_node.location[0], script_node.end[0] - 1

    with open(path, mode="r") as fh:
        lines = fh.readlines()

    source = "".join(lines[start:end])
    try:
        formatted_source = black.format_file_contents(source, fast=False, mode=mode)
        if check:
            logger.warning(f"Would change: {path}")
            return 1

        lines[start:end] = formatted_source

        logger.warning(f"Blackened: {path}")
        with open(path, mode="w") as fh:
            fh.writelines(lines)
    except black.report.NothingChanged:
        pass
    except Exception as e:
        logger.exception(e)
        return 1
    return 0


def main(argv=None):
    import argparse
    import sys

    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Format cgx files with black")
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "path",
        nargs="*",
        type=Path,
        default=[Path(".")],
        help="path(s) of files and/or folders to format",
    )
    args = parser.parse_args(argv)

    modes = {}

    code = 0
    for path in args.path:
        if not path.exists():
            pass

        if path.is_file():
            code |= format(path, mode=load_black_mode(path, modes), check=args.check)
        else:
            for file in path.glob("**/*.cgx"):
                code |= format(
                    file, mode=load_black_mode(file, modes), check=args.check
                )

    if code:
        exit(code)


if __name__ == "__main__":
    main()
