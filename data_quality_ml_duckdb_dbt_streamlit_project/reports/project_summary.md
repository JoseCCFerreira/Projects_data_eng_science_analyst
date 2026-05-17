# Project Summary

## O que foi criado

- Pipeline completo de dados com geração, armazenamento, dbt, qualidade, limpeza, ML e dashboard.
- Page pessoal de portfólio em `docs/index.html`.

## Arquitetura do projeto

- Raw CSV → SQLite OLTP → DuckDB OLAP → dbt → ML → Streamlit.

## Como correr

Use `make all` para executar o pipeline completo ou os comandos individuais para cada etapa.

## Limitações

- Dados sintéticos gerados localmente.
- Modelos não foram validados em produção.

## Próximos passos

- Mover para PostgreSQL/Redshift.
- Implementar orquestração e monitorização.
- Adicionar testes de integração e data quality automatizada.

## Portfolio Story

Este projeto demonstra habilidade de entregar um pipeline industrial escalável e de comunicar os resultados em um dashboard profissional.
