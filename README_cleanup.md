# Limpeza de espaço e recriação de ambientes

Este repositório contém duas ferramentas principais:

- `scripts/cleanup_optimize.py`: remove caches, comprime logs, converte CSVs grandes para Parquet/gzip e arquiva bases de dados.
- `scripts/recreate_envs.sh`: recria os ambientes virtuais removidos usando as informações salvas em backups.

## Como usar

### 1) Recriar ambientes virtuais

Execute a partir do diretório raiz do projecto:

```bash
bash scripts/recreate_envs.sh /Users/carlosferreira/Projecto/projects/venv_removal_backup_20260515_220444
```

O script criará cada ambiente no local original e instalará pacotes a partir de `requirements.txt` ou `pyproject.toml` quando disponíveis.

### 2) Ver o que o cleanup faria

Execute um dry-run para ver as ações sem modificar ficheiros:

```bash
python3 scripts/cleanup_optimize.py --root projects --min-csv-mb 10 --dry-run
```

### 3) Executar o cleanup real

```bash
python3 scripts/cleanup_optimize.py --root projects --min-csv-mb 10
```

### 4) Backups gerados

Os backups automáticos estão em:

- `projects/venv_removal_backup_20260515_220444/`
- `projects/cleanup_backups_20260515_220649/`

Estes diretórios contêm a lista de venvs removidos, ficheiros de requisitos, DBs arquivados e ficheiros originais restauráveis.

## Notas

- O script de recreação instala pacotes com `pip` dentro de cada venv.
- Se quiser usar `poetry` ou `pipenv`, posso adaptar o script.
- Mantenha os backups até ter confirmado que tudo funciona bem.
