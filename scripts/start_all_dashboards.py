from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import project_manager_app as app  # noqa: E402


def main() -> None:
    for project in app.list_projects():
        if not app.service_config(project):
            continue
        ok, message = app.start_project_app(project)
        print(f"{project.name}: {'ok' if ok else 'failed'} - {message}")
        if not ok:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
