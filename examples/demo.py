"""The same gate used before the release workflow build."""

import json
from pathlib import Path

from release_manager.core import bump, check_tag

out = Path(__file__).parent
project = out.parent / "pyproject.toml"
result = {
    "bump": {part: bump("1.2.3", part) for part in ("major", "minor", "patch")},
    "success": check_tag(project, "v1.0.0"),
}
for tag in ("v1.0.1", "vbad", ""):
    try:
        check_tag(project, tag)
    except ValueError as exc:
        result[f"rejected:{tag}"] = str(exc)
(out / "release-checks.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(result)
