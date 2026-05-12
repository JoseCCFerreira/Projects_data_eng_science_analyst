# Referência Rápida Da Stack

Este documento explica as tecnologias principais do portfólio usando sempre a mesma estrutura:

- o que é
- para que é utilizado
- quando usar
- onde aparece nos projetos
- como começar a praticar
- atalhos ou comandos rápidos

## PL/SQL

### O Que É

PL/SQL é a extensão procedural do SQL na Oracle. O SQL consulta e transforma dados; o PL/SQL permite adicionar variáveis, condições, ciclos, procedures, functions, triggers e tratamento de exceções à volta dessas operações.

### Para Que É Utilizado

- stored procedures e functions
- regras de negócio dentro da base Oracle
- triggers que reagem a inserts, updates ou deletes
- processamento batch
- validação e tratamento de erros
- lógica reutilizável na base de dados

### Quando Usar

Usa PL/SQL quando a lógica deve viver perto da base de dados Oracle, especialmente quando precisas de consistência transacional, validação no lado da base ou rotinas reutilizáveis por várias aplicações.

### Onde Entra Neste Portfólio

O hub atual foca-se sobretudo em Python, SQLite, DuckDB, dbt e Streamlit. O PL/SQL entra na camada de aprendizagem relacional e liga-se aos materiais em `learning_materials/`, onde existem PDFs e scripts de estudo de PL/SQL.

### Como Praticar

1. Criar uma tabela simples.
2. Escrever uma procedure que insere dados validados.
3. Adicionar tratamento de exceções.
4. Criar um trigger que regista alterações.
5. Consultar a tabela de auditoria para validar o comportamento.

### Atalhos PL/SQL

```sql
-- Bloco anónimo
BEGIN
  DBMS_OUTPUT.PUT_LINE('Hello PL/SQL');
END;
/

-- Variáveis
DECLARE
  v_total NUMBER := 0;
BEGIN
  SELECT COUNT(*) INTO v_total FROM customers;
  DBMS_OUTPUT.PUT_LINE(v_total);
END;
/

-- IF
IF v_total > 100 THEN
  DBMS_OUTPUT.PUT_LINE('Volume alto');
ELSE
  DBMS_OUTPUT.PUT_LINE('Volume baixo');
END IF;

-- Loop
FOR r IN (SELECT customer_id, customer_name FROM customers) LOOP
  DBMS_OUTPUT.PUT_LINE(r.customer_id || ' - ' || r.customer_name);
END LOOP;

-- Procedure
CREATE OR REPLACE PROCEDURE add_customer(p_name IN VARCHAR2) AS
BEGIN
  INSERT INTO customers(customer_name) VALUES (p_name);
  COMMIT;
END;
/

-- Function
CREATE OR REPLACE FUNCTION get_customer_count RETURN NUMBER AS
  v_count NUMBER;
BEGIN
  SELECT COUNT(*) INTO v_count FROM customers;
  RETURN v_count;
END;
/

-- Tratamento de exceções
EXCEPTION
  WHEN NO_DATA_FOUND THEN
    DBMS_OUTPUT.PUT_LINE('Sem dados');
  WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE(SQLERRM);

-- Trigger
CREATE OR REPLACE TRIGGER trg_customers_audit
AFTER INSERT OR UPDATE OR DELETE ON customers
FOR EACH ROW
BEGIN
  INSERT INTO customers_audit(action_date) VALUES (SYSDATE);
END;
/
```

## Git

### O Que É

Git é um sistema de controlo de versões. Regista como os ficheiros mudam ao longo do tempo.

### Para Que É Utilizado

- acompanhar alterações no código
- criar commits
- comparar versões
- recuperar trabalho anterior
- colaborar através do GitHub

### Quando Usar

Usa Git sempre que um projeto muda. Faz commit depois de uma unidade de trabalho coerente e testada.

### Onde Aparece

O hub central é um repositório Git, e cada projeto dentro de `projects/` mantém o seu próprio histórico Git.

### Comandos Rápidos

```bash
git status --short
git diff
git add README.md
git commit -m "Improve documentation"
git log --oneline
git push
```

## SQL E SQLite Relacional

### O Que É

SQL é a linguagem para consultar e transformar dados relacionais. SQLite é uma base de dados relacional leve e local.

### Para Que É Utilizado

- tabelas e relações
- primary keys e foreign keys
- joins
- agregações
- exemplos transacionais

### Quando Usar

Usa SQLite quando precisas de uma base pequena local, uma base de aprendizagem ou um modelo relacional estilo aplicação.

### Onde Aparece

Os projetos de retail usam SQLite para explicar modelação relacional OLTP.

### Comandos Rápidos

```sql
CREATE TABLE customers (
  customer_id INTEGER PRIMARY KEY,
  customer_name TEXT NOT NULL
);

SELECT c.customer_name, SUM(t.total_amount) AS revenue
FROM customers c
JOIN transactions t ON t.customer_id = c.customer_id
GROUP BY c.customer_name
ORDER BY revenue DESC;
```

## DuckDB

### O Que É

DuckDB é uma base analítica local desenhada para queries OLAP rápidas.

### Para Que É Utilizado

- ler CSV e Parquet
- joins analíticos
- agregações
- marts locais
- backend para dashboards

### Quando Usar

Usa DuckDB quando a análise é demasiado analítica para SQLite, mas não precisa de uma data warehouse cloud.

### Onde Aparece

Fuel, retail e tyre wear usam DuckDB para armazenamento analítico e outputs.

### Comandos Rápidos

```sql
CREATE TABLE sales AS
SELECT * FROM read_csv_auto('data/sales.csv');

SELECT product_id, SUM(revenue) AS total_revenue
FROM sales
GROUP BY product_id
ORDER BY total_revenue DESC;
```

## dbt

### O Que É

dbt é uma framework de transformação que organiza modelos SQL em pipelines analíticos testáveis.

### Para Que É Utilizado

- staging models
- intermediate models
- marts
- testes
- documentação
- lineage

### Quando Usar

Usa dbt quando as transformações SQL precisam de ser repetíveis, testadas e organizadas.

### Onde Aparece

Fuel, retail e tyre wear usam dbt ou conceitos de dbt.

### Comandos Rápidos

```bash
dbt debug
dbt run
dbt test
dbt build
dbt docs generate
dbt docs serve
```

## Análise Estatística

### O Que É

A análise estatística transforma dados em evidência medida.

### Para Que É Utilizada

- médias
- desvio padrão
- distribuições
- deteção de outliers
- correlação
- estudos de eventos

### Quando Usar

Usa estatística antes de machine learning. Ela explica a forma, qualidade e fiabilidade dos dados.

### Onde Aparece

Todos os projetos analíticos usam resumos estatísticos, correlações ou distribuições.

### Fórmulas Rápidas

```text
media = soma(x) / n
variancia = soma((x - media)^2) / (n - 1)
z_score = (x - media) / desvio_padrao
correlacao = covariancia(X,Y) / (std(X) * std(Y))
```

## Machine Learning

### O Que É

Machine learning usa dados para aprender padrões que apoiam previsão, classificação, ranking ou segmentação.

### Para Que É Utilizado

- forecasting
- classificação
- importância de features
- clustering
- recomendações
- deteção de anomalias

### Quando Usar

Usa machine learning depois de os dados estarem limpos, o baseline definido e a métrica de avaliação clara.

### Onde Aparece

Fuel, retail, Portugal bike, Citibike e tyre wear incluem conceitos ou outputs de machine learning.

### Fluxo Rápido

```text
target -> features -> train/test split -> baseline -> model -> metrics -> interpretation -> limitations
```

## Streamlit

### O Que É

Streamlit é uma framework Python para criar aplicações interativas de dados rapidamente.

### Para Que É Utilizado

- dashboards
- filtros
- gráficos
- exploração de dados
- downloads
- demos de modelos

### Quando Usar

Usa Streamlit quando um projeto precisa de ser explorado por pessoas que não devem ter de ler o código primeiro.

### Onde Aparece

O hub central e todos os projetos integrados têm dashboard Streamlit.

### Comandos Rápidos

```bash
streamlit run project_manager_app.py --server.port 8600
streamlit run app.py --server.port 8610
```

## Resultados E Interpretação

### O Que É

Resultados são os outputs finais que ligam dados, método, gráfico e conclusão.

### Para Que É Utilizado

- apoio à decisão
- apresentação de projeto
- evidência de portfólio
- avaliação de modelos
- comunicação com stakeholders

### Quando Usar

Cada projeto deve terminar com resultados, limitações e próximos passos.

### Onde Aparece

Cada dashboard e guia HTML liga outputs à interpretação.

### Checklist Rápida

```text
O pipeline é reproduzível?
As linhas e colunas foram validadas?
O gráfico responde a uma pergunta clara?
Existe baseline?
As limitações estão documentadas?
```
