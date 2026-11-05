"""Local equivalent of the tag-gated release job; ordinary CI does not call it."""

import argparse
import subprocess
from pathlib import Path

from release_manager.core import check_tag


def main():
    parser = argparse.ArgumentParser(description="Проверить релизный тег и собрать wheel + sdist")
    parser.add_argument("--tag")
    parser.add_argument("--output", default="dist")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    try:
        check_tag(root / "pyproject.toml", args.tag)
    except ValueError as exc:
        parser.exit(2, f"Ошибка: {exc}\n")
    subprocess.run(
        ["uv", "build", str(root), "--out-dir", str(Path(args.output).resolve())], check=True
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
