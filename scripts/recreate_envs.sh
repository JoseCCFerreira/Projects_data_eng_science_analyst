#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <backup_dir_with_venv_list.txt>"
  echo "Example: $0 /absolute/path/to/projects/venv_removal_backup_20260515_220444"
  exit 1
fi
BACKUP_DIR="$1"
VENV_LIST="$BACKUP_DIR/venv_to_remove_ordered.txt"
if [ ! -f "$VENV_LIST" ]; then
  echo "Cannot find $VENV_LIST"
  exit 1
fi

while IFS= read -r VENV; do
  PROJECT_DIR=$(dirname "$VENV")
  echo "Recreating venv: $VENV for project: $PROJECT_DIR"
  python3 -m venv "$VENV"
  # shellcheck disable=SC1090
  source "$VENV/bin/activate"
  pip install -U pip setuptools wheel
  if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    pip install -r "$PROJECT_DIR/requirements.txt"
  elif [ -f "$PROJECT_DIR/pyproject.toml" ]; then
    pip install "$PROJECT_DIR"
  else
    echo "No requirements.txt or pyproject.toml found in $PROJECT_DIR — venv created but no packages installed"
  fi
  deactivate
done < "$VENV_LIST"

echo "Done: environments recreated (or venvs created)."
