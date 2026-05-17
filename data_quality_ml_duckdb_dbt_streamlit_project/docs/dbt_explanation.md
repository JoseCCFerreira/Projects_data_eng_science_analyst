# dbt Explanation

## O que é dbt

dbt é uma ferramenta de transformação de dados que usa SQL para criar pipelines versionáveis e testáveis.

## Por que usar dbt

- Mantém transformações bem documentadas.
- Garante qualidade com testes e validações.
- Facilita lineage e colaboração.

## Camadas dbt

- **staging**: limpa e padroniza dados vindos de fontes brutas.
- **intermediate**: aplica regras de negócio e prepara dados.
- **marts**: constrói tabelas finais para relatórios.

## Tests e documentação

- `not_null`, `unique`, `accepted_values` e `relationships` ajudam a validar suposições.
- A documentação torna o pipeline mais confiável e rastreável.
