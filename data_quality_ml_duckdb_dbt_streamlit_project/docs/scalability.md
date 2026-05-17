# Scalability

Este projeto foi criado para escalar de forma natural. As recomendações incluem:

- mover a base transacional para PostgreSQL para suportar mais dados e conexões simultâneas;
- migrar a camada analítica para Redshift, Snowflake ou BigQuery para consultas maiores;
- usar Docker para criar um ambiente reproducível;
- usar Airflow ou similar para orquestração de pipeline;
- adicionar CI/CD com GitHub Actions para testes automáticos;
- adicionar Great Expectations ou Soda para data quality automatizada;
- usar MLflow para rastrear modelos e versões;
- armazenar dados brutos em S3 e separar camadas Bronze/Silver/Gold;
- monitorar modelos em produção com métricas de performance e drift.
