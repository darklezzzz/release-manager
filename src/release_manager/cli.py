"""Command line interface; run --help for available operations."""

import argparse
import json
import sqlite3

from .core import bump, package_version, check_tag, register


def main():
    parser = argparse.ArgumentParser(description="release-manager")
    commands = parser.add_subparsers(dest="command", required=True)
    sub = commands.add_parser("show")
    sub.add_argument("--project", default="pyproject.toml")
    sub = commands.add_parser("bump")
    sub.add_argument("version")
    sub.add_argument("part")
    sub = commands.add_parser("register")
    sub.add_argument("version")
    sub.add_argument("changes")
    sub.add_argument("--project", default="pyproject.toml")
    sub.add_argument("--changelog", default="CHANGELOG.md")
    sub = commands.add_parser("check-tag")
    sub.add_argument("--tag")
    sub.add_argument("--project", default="pyproject.toml")
    args = parser.parse_args()
    try:
        if args.command == "show":
            result = package_version(args.project)
        if args.command == "bump":
            result = bump(args.version, args.part)
        if args.command == "register":
            result = register(args.project, args.changelog, args.version, json.loads(args.changes))
        if args.command == "check-tag":
            result = check_tag(args.project, args.tag)
        print(
            json.dumps(result, ensure_ascii=False, indent=2)
            if not isinstance(result, str)
            else result
        )
        if isinstance(result, dict) and result.get("passed") is False:
            return 1
        return 0
    except (ValueError, OSError, sqlite3.Error) as exc:
        parser.exit(2, f"Ошибка: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
