# Stack Quick Reference

This document explains the main technologies in the portfolio using the same structure:

- what it is
- what it is used for
- when to use it
- where it appears in the projects
- how to start practicing
- quick commands or shortcuts

## PL/SQL

### What It Is

PL/SQL is Oracle's procedural extension to SQL. SQL asks questions of data; PL/SQL lets you add variables, conditions, loops, procedures, functions, triggers and exception handling around those SQL operations.

### What It Is Used For

- stored procedures and functions
- business rules inside Oracle databases
- triggers that react to inserts, updates or deletes
- batch processing
- validation and exception handling
- reusable database logic

### When To Use It

Use PL/SQL when the logic belongs close to an Oracle database, especially when you need transactional consistency, database-side validation or reusable routines that multiple applications can call.

### Where It Fits In This Portfolio

The current project hub focuses mostly on Python, SQLite, DuckDB, dbt and Streamlit. PL/SQL belongs to the relational database learning layer and connects naturally with the `learning_materials/` folder that contains PL/SQL study PDFs and scripts.

### How To Practice

1. Create a simple table.
2. Write a procedure that inserts validated data.
3. Add an exception handler.
4. Add a trigger that logs changes.
5. Query the audit table to verify behavior.

### PL/SQL Shortcuts / Cheat Sheet

```sql
-- Anonymous block
BEGIN
  DBMS_OUTPUT.PUT_LINE('Hello PL/SQL');
END;
/

-- Variables
DECLARE
  v_total NUMBER := 0;
BEGIN
  SELECT COUNT(*) INTO v_total FROM customers;
  DBMS_OUTPUT.PUT_LINE(v_total);
END;
/

-- IF statement
IF v_total > 100 THEN
  DBMS_OUTPUT.PUT_LINE('High volume');
ELSE
  DBMS_OUTPUT.PUT_LINE('Low volume');
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

-- Exception handling
EXCEPTION
  WHEN NO_DATA_FOUND THEN
    DBMS_OUTPUT.PUT_LINE('No data found');
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

### What It Is

Git is a version-control system. It records how files change over time.

### What It Is Used For

- tracking code changes
- creating commits
- comparing versions
- recovering previous work
- collaborating through GitHub

### When To Use It

Use Git every time a project changes. Commit after a coherent, tested unit of work.

### Where It Appears

The central hub is a Git repository, and each project inside `projects/` keeps its own Git history.

### Quick Commands

```bash
git status --short
git diff
git add README.md
git commit -m "Improve documentation"
git log --oneline
git push
```

## SQL And Relational SQLite

### What It Is

SQL is the language for querying and transforming relational data. SQLite is a lightweight relational database engine.

### What It Is Used For

- tables and relationships
- primary keys and foreign keys
- joins
- aggregations
- transactional examples

### When To Use It

Use SQLite when you need a small local database, a learning database or an application-style relational model.

### Where It Appears

Retail projects use SQLite to explain OLTP-style relational modeling.

### Quick Commands

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

### What It Is

DuckDB is an analytical database designed for fast local OLAP queries.

### What It Is Used For

- reading CSV and Parquet files
- analytical joins
- aggregations
- local data marts
- dashboard backends

### When To Use It

Use DuckDB when data analysis is too analytical for SQLite but does not require a cloud warehouse.

### Where It Appears

Fuel, retail and tyre wear projects use DuckDB for analytical storage and outputs.

### Quick Commands

```sql
CREATE TABLE sales AS
SELECT * FROM read_csv_auto('data/sales.csv');

SELECT product_id, SUM(revenue) AS total_revenue
FROM sales
GROUP BY product_id
ORDER BY total_revenue DESC;
```

## dbt

### What It Is

dbt is a transformation framework that organizes SQL models into tested analytical pipelines.

### What It Is Used For

- staging models
- intermediate models
- marts
- tests
- documentation
- lineage

### When To Use It

Use dbt when SQL transformations need to be repeatable, tested and organized.

### Where It Appears

Fuel, retail and tyre wear projects use dbt or dbt-style concepts.

### Quick Commands

```bash
dbt debug
dbt run
dbt test
dbt build
dbt docs generate
dbt docs serve
```

## Statistical Analysis

### What It Is

Statistical analysis turns data into measured evidence.

### What It Is Used For

- averages
- standard deviation
- distributions
- outlier detection
- correlation
- event studies

### When To Use It

Use statistics before machine learning. It explains the shape, quality and reliability of the data.

### Where It Appears

All analytical projects use statistical summaries, correlations or distributions.

### Quick Formulas

```text
mean = sum(x) / n
variance = sum((x - mean)^2) / (n - 1)
z_score = (x - mean) / standard_deviation
correlation = covariance(X,Y) / (std(X) * std(Y))
```

## Machine Learning

### What It Is

Machine learning uses data to learn patterns that support prediction, classification, ranking or segmentation.

### What It Is Used For

- forecasting
- classification
- feature importance
- clustering
- recommendations
- anomaly detection

### When To Use It

Use machine learning after the data is clean, the baseline is defined and the evaluation metric is clear.

### Where It Appears

Fuel, retail, Portugal bike, Citibike and tyre wear projects include machine-learning concepts or outputs.

### Quick Workflow

```text
target -> features -> train/test split -> baseline -> model -> metrics -> interpretation -> limitations
```

## Streamlit

### What It Is

Streamlit is a Python framework for building interactive data apps quickly.

### What It Is Used For

- dashboards
- filters
- charts
- data exploration
- downloads
- model demos

### When To Use It

Use Streamlit when a project needs to be explored by people who should not need to read the source code first.

### Where It Appears

The central hub and every integrated project has a Streamlit dashboard.

### Quick Commands

```bash
streamlit run project_manager_app.py --server.port 8600
streamlit run app.py --server.port 8610
```

## Results And Interpretation

### What It Is

Results are the final outputs that connect data, method, chart and conclusion.

### What It Is Used For

- decision support
- project presentation
- portfolio evidence
- model evaluation
- stakeholder communication

### When To Use It

Every project should end with results, limitations and next steps.

### Where It Appears

Each dashboard and HTML guide connects outputs to interpretation.

### Quick Checklist

```text
Is the pipeline reproducible?
Are the rows and columns validated?
Does the chart answer a clear question?
Is there a baseline?
Are limitations documented?
```
