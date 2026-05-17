#!/usr/bin/env python3
"""Limpeza e compressão/arquivamento de dados no workspace.

Operações:
- Remove `__pycache__` e ficheiros `*.pyc` (recriáveis)
- Compacta logs (`*.log`) em gzip
- Converte CSVs grandes para Parquet (usa pyarrow quando disponível)
- Arquiva bases de dados (.duckdb, .db, .sqlite) em .tar.gz

Cria um backup timestamped em caso de recuperação.
"""
import argparse
import os
import shutil
import sys
import tarfile
import gzip
from pathlib import Path
from datetime import datetime


def make_backup_dir(base):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    d = Path(base) / f"cleanup_backups_{ts}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def remove_pycache_and_pyc(root):
    removed = 0
    for p in Path(root).rglob('__pycache__'):
        try:
            shutil.rmtree(p)
            removed += 1
            print(f"Removed: {p}")
        except Exception as e:
            print(f"Failed remove {p}: {e}")
    for p in Path(root).rglob('*.pyc'):
        try:
            p.unlink()
            removed += 1
        except Exception as e:
            print(f"Failed remove {p}: {e}")
    return removed


def compress_logs(root, backup_dir):
    compressed = 0
    for p in Path(root).rglob('*.log'):
        try:
            rel = p.relative_to(root)
            target_backup = backup_dir / rel.parent
            target_backup.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target_backup / p.name)
            with open(p, 'rb') as f_in, gzip.open(str(p) + '.gz', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
            p.unlink()
            compressed += 1
            print(f"Compressed log: {p} -> {p}.gz")
        except Exception as e:
            print(f"Failed compress {p}: {e}")
    return compressed


def archive_db_file(p: Path, backup_dir: Path, root: Path):
    rel = p.relative_to(root)
    target_dir = backup_dir / rel.parent
    target_dir.mkdir(parents=True, exist_ok=True)
    backup_path = target_dir / p.name
    shutil.copy2(p, backup_path)
    tarname = str(backup_path) + '.tar.gz'
    with tarfile.open(tarname, 'w:gz') as tf:
        tf.add(str(backup_path), arcname=p.name)
    backup_path.unlink()
    p.unlink()
    print(f"Archived DB: {p} -> {tarname}")


def gzip_file(p: Path, backup_dir: Path, root: Path):
    rel = p.relative_to(root)
    target_backup_dir = backup_dir / rel.parent
    target_backup_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(p, target_backup_dir / p.name)
    gz_path = p.with_suffix(p.suffix + '.gz')
    with open(p, 'rb') as f_in, gzip.open(gz_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    p.unlink()
    print(f"Gzipped: {p} -> {gz_path}")


def convert_csv_to_parquet(p: Path, backup_dir: Path, root: Path):
    # backup original
    rel = p.relative_to(root)
    target_backup_dir = backup_dir / rel.parent
    target_backup_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(p, target_backup_dir / p.name)

    try:
        import pyarrow as pa
        import pyarrow.csv as pv
        import pyarrow.parquet as pq
        tbl = pv.read_csv(str(p))
        out = p.with_suffix('.parquet')
        pq.write_table(tbl, str(out), compression='snappy')
        p.unlink()
        print(f"Converted CSV->Parquet: {p} -> {out}")
        return True
    except Exception as e:
        print(f"pyarrow conversion failed for {p}: {e}. Falling back to gzip.")
        try:
            gzip_file(p, backup_dir, root)
            return True
        except Exception as e2:
            print(f"Fallback gzip failed for {p}: {e2}")
            return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.', help='Root path to operate on')
    ap.add_argument('--min-csv-mb', type=int, default=10, help='Minimum CSV size (MB) to convert/compress')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    root = Path(args.root).resolve()
    print(f"Root: {root}")
    backup_dir = make_backup_dir(root)
    print(f"Backup dir: {backup_dir}")

    if args.dry_run:
        print("DRY RUN: no changes will be made")

    # 1. remove pycache and pyc
    if not args.dry_run:
        removed = remove_pycache_and_pyc(root)
        print(f"Removed pycache/pyc entries: {removed}")

    # 2. compress logs
    if not args.dry_run:
        logs = compress_logs(root, backup_dir)
        print(f"Compressed logs: {logs}")

    # 3. process CSVs
    min_bytes = args.min_csv_mb * 1024 * 1024
    csvs = list(root.rglob('*.csv'))
    processed_csv = 0
    for p in csvs:
        try:
            if p.stat().st_size >= min_bytes:
                ok = convert_csv_to_parquet(p, backup_dir, root) if not args.dry_run else True
                if ok:
                    processed_csv += 1
        except Exception as e:
            print(f"Error processing {p}: {e}")
    print(f"CSV processed: {processed_csv}")

    # 4. archive DBs
    db_exts = ['*.duckdb', '*.db', '*.sqlite']
    archived = 0
    for pat in db_exts:
        for p in root.rglob(pat):
            try:
                if not args.dry_run:
                    archive_db_file(p, backup_dir, root)
                archived += 1
            except Exception as e:
                print(f"Failed archive {p}: {e}")
    print(f"DB archived: {archived}")

    print("Done.")


if __name__ == '__main__':
    main()
