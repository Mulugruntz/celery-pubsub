import argparse
import itertools
import json
import sys
from argparse import Namespace
from typing import Any, Optional

import pip._internal.commands.index
from pip._internal.commands.index import IndexCommand
from pip._vendor.packaging.specifiers import SpecifierSet

VERSION_START_TOKEN = "Available versions: "


class OutputCapture(list[str]):
    def write_output(self, msg: Any, *args: Any) -> None:
        self.append(msg)


def get_versions(
    package_name: str,
    platform: Optional[str],
    python_version: Optional[str],
    implementation: Optional[str],
) -> list[str]:
    index = IndexCommand("index", "Inspect information available from package indexes.")
    arguments = [package_name]
    if platform is not None:
        arguments += ["--platform", platform]
    if python_version is not None:
        arguments += ["--python-version", python_version]
    if implementation is not None:
        arguments += ["--implementation", implementation]
    opts, args = index.parse_args(arguments)
    output = OutputCapture()
    pip._internal.commands.index.write_output = output.write_output
    index.get_available_package_versions(opts, args)
    for line in output:
        if line.startswith(VERSION_START_TOKEN):
            return line[len(VERSION_START_TOKEN) :].split(", ")
    print("No version found.", file=sys.stderr)
    exit(1)


def get_python_version_and_implementation(python_code: str) -> tuple[str, str]:
    if python_code.startswith("pypy"):
        impl, py_ver, *pypy_ver = python_code.split("-")
        return "pp", py_ver
    return "cp", python_code


def contains_version(version: str, version_specifier: str) -> bool:
    specifier = SpecifierSet(version_specifier)
    return specifier.contains(version)


def filter_versions(versions: list[str], version_specifier: str) -> list[str]:
    return [v for v in versions if contains_version(v, version_specifier)]


def parse_args() -> Namespace:
    parser = argparse.ArgumentParser(description="Resolve versions.")
    subparsers = parser.add_subparsers(dest="action")

    parser_versions = subparsers.add_parser(
        "versions", help="Finds all satisfying versions of a package."
    )

    parser_versions.add_argument("-c", "--python-code", type=str, help="Python code")
    parser_versions.add_argument(
        "-o", "--operating-system", type=str, help="Operating system"
    )
    parser_versions.add_argument("-n", "--package-name", type=str, help="Package name")
    parser_versions.add_argument("-s", "--specifier", type=str, help="Specifier")

    parser_matrix = subparsers.add_parser("matrix", help="Enter The Matrix")

    parser_matrix.add_argument("-c", "--python-codes", type=str, help="Python codes")
    parser_matrix.add_argument(
        "-o", "--operating-systems", type=str, help="Operating systems"
    )
    parser_matrix.add_argument("-n", "--package-name", type=str, help="Package name")
    parser_matrix.add_argument("-s", "--specifiers", type=str, help="Specifiers")
    parser_matrix.add_argument(
        "--invert",
        action="store_true",
        default=False,
        help="Invert matrix (only show the skipped ones)",
    )

    return parser.parse_args()


def get_compatible_versions(
    python_code: str, operating_system: str, package_name: str, specifier: str
) -> list[str]:
    implementation, python_version = get_python_version_and_implementation(python_code)
    versions = get_versions(
        package_name, operating_system, python_version, implementation
    )
    return filter_versions(versions, specifier)


def process_versions(args: Namespace) -> None:
    filtered_versions = get_compatible_versions(
        args.python_code, args.operating_system, args.package_name, args.specifier
    )
    if not filtered_versions:
        print(f"Found no {args.package_name} version.", file=sys.stderr)
        exit(1)
    print(
        f"Found the following {args.package_name} versions: {', '.join(v for v in filtered_versions)}",
        file=sys.stderr,
    )


def process_matrix(args: Namespace) -> None:
    python_codes = json.loads(args.python_codes)
    operating_systems = json.loads(args.operating_systems)
    package_name = args.package_name
    specifiers = json.loads(args.specifiers)
    is_inverted = args.invert
    matrix = itertools.product(
        python_codes, operating_systems, [package_name], specifiers
    )
    output = {"include": []}
    for c, o, n, s in matrix:
        compatible_versions = get_compatible_versions(c, o, n, s)
        if compatible_versions:
            # This is because celery 3 depends on use_2to3,
            # which is no longer supported by 3.9 and 3.10
            # and by newer pypy versions.
            if (
                n == "celery"
                and (
                    c.replace(".", "").startswith("39")
                    or c.replace(".", "").startswith("310")
                    or c.startswith("pypy-3")
                )
                and all(cv.startswith("3") for cv in compatible_versions)
            ):
                if is_inverted:
                    output["include"].append(
                        {
                            "python-version": c,
                            "os": o,
                            "celery": s,
                        }
                    )
                continue
            if not is_inverted:
                output["include"].append(
                    {
                        "python-version": c,
                        "os": o,
                        "celery": s,
                    }
                )
        elif is_inverted:
            output["include"].append(
                {
                    "python-version": c,
                    "os": o,
                    "celery": s,
                }
            )
    print(json.dumps(output))


def main() -> None:
    args = parse_args()

    if args.action == "versions":
        process_versions(args)
    elif args.action == "matrix":
        process_matrix(args)


if __name__ == "__main__":
    main()
