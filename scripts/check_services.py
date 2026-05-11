from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "central_project_manifest.json"


def check_url(url: str, timeout: int = 10) -> int | str:
    try:
        request = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status
    except urllib.error.HTTPError as exc:
        return exc.code
    except Exception as exc:
        return f"error: {exc}"


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    checks = [(manifest["central_hub"]["name"], manifest["central_hub"]["dashboard"])]
    checks.extend((project["name"], project["dashboard"]) for project in manifest["projects"])

    failed = []
    for name, url in checks:
        status = check_url(url)
        print(f"{status}\t{name}\t{url}")
        if status != 200:
            failed.append((name, url, status))

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
