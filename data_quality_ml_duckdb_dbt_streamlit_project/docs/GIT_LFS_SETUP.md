# Git LFS Setup Guide

## Current Status

Git LFS is **not installed** on this macOS system, so large model artifacts (>100 MB) are tracked in `.gitignore` to prevent GitHub push errors.

The `.gitattributes` configuration has been committed to prepare the repository for Git LFS support.

## To Enable Git LFS

If you want to track large model files with Git LFS:

### Option 1: Install via MacPorts
```bash
sudo port install git-lfs
git lfs install
```

### Option 2: Install via source (download binary)
1. Download Git LFS from: https://github.com/git-lfs/git-lfs/releases
2. Extract and add to PATH
3. Run `git lfs install`

### Option 3: Wait for Homebrew to become available
When Homebrew is installed on system:
```bash
brew install git-lfs
git lfs install
```

## Once Git LFS is Installed

1. Remove `data_quality_ml_duckdb_dbt_streamlit_project/models/` from `.gitignore`
2. Track models with LFS:
   ```bash
   git add -f data_quality_ml_duckdb_dbt_streamlit_project/models/**/*.joblib
   git commit -m "chore: add large model artifacts via Git LFS"
   git push origin main
   ```

## Current Workaround

For now, the project is pushed without model binaries. To use the models locally:
- Regenerate them by running: `make ml-predict`
- Or manually train new models and save locally

The `.joblib` files will be auto-generated during the ML pipeline runs.
