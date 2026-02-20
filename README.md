# Churn Lifecycle & Retention Modeling

Skills Demonstrated
SQL · Feature Engineering · ML Pipelines · Data Validation · Model Evaluation · Experimentation Infrastructure


Production-style churn prediction system built with a full data engineering → feature store → ML training → artifact pipeline.

This project demonstrates how a structured analytics layer can support reproducible model training, experiment tracking, and deployable inference workflows.
 
## Goals

- Predict customer churn probability

- Identify drivers of churn

- Provide actionable insights for customer retention

- Demonstrate an end-to-end DS/MLE workflow

## Key Outcomes
- Built relational data pipeline transforming raw CSV → analytics feature view
- Designed reusable SQL feature layer for model training
- Achieved reproducible training workflow with saved artifacts and metrics
- Structured system to support future model comparison experiments

## Project Architecture

PostgreSQL (Docker)
        ↓
staging → core → analytics.churn_features_v1 (SQL pipeline)
        ↓
src/train.py (sklearn pipeline)
        ↓
artifacts/model.joblib + metrics.json
        ↓
Streamlit app (planned)

Design Decisions
- Used database-level feature engineering instead of Python preprocessing to ensure consistency across training runs
- Separated staging/core/analytics schemas to mimic production data warehouse patterns
- Saved metrics + model artifacts to support benchmarking and experiment comparison

## Tech

- Python
- pandas
- scikit-learn
- PostgreSQL
- Docker
- Kaggle API
- SQLalchemy
- Streamlit (planned)

## Start Postgres (Docker)

First time only:

```bash
docker run --name churn-postgres \
-e POSTGRES_PASSWORD=postgres \
-e POSTGRES_USER=postgres \
-e POSTGRES_DB=churn \
-p 5432:5432 \
-d postgres:16
```

Otherwise:

```bash
docker start churn-postgres
```

Verify server is running properly:

```bash
psql -h localhost -U postgres -d churn
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

```

## Train the Model

Install dependencies:


```bash

pip install -r requirements.txt

```
Set the database connection:

```bash

export DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/churn"

```
Run training:

```bash

python -m src.train

```

This code trains from the analytics view and saves:

```bash

artifacts/model.joblib
artifacts/metrics.json
```



