# Churn Lifecycle & Retention Modeling

End-to-end churn prediction project: data cleaning, feature engineering, model training, evaluation,
and a lightweight inference app.
 
## Goals

- Predict churn probability

- Identify drivers of churn

- Provide actionable segments for retention


## Tech

- Python
- pandas
- scikit-learn
- PostgreSQL
- Docker
- Kaggle API

## Start Postgres (Docker)

```bash
docker run --name churn-postgres \
-e POSTGRES_PASSWORD=postgres \
-e POSTGRES_USER=postgres \
-e POSTGRES_DB=churn \
-p 5432:5432 \
-d postgres:16
```

## Data Ingestion (Kaggle)

This project acquires the dataset programmatically using the Kaggle API to ensure full reproducibility.

```bash
mkdir -p data/raw
kaggle datasets download -d yeanzc/telco-customer-churn-ibm-dataset -p data/raw --unzip
```

The raw dataset is staged in `data/raw/` and is not committed to the repository.


## Build Database

From the repo root:

```bash
psql "postgresql://postgres:postgres@localhost:5432/churn" -f sql/01_create_staging.sql

CSV_PATH=$(realpath data/raw/*.csv)
psql "postgresql://postgres:postgres@localhost:5432/churn" \
-c "\copy staging.telco_raw FROM '$CSV_PATH' WITH (FORMAT csv, HEADER true);"

psql "postgresql://postgres:postgres@localhost:5432/churn" -f sql/03_build_core_and_analytics.sql


