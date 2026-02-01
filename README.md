# Churn Lifecycle & Retention Modeling

End-to-end churn predictino project: data cleaning, feature engineering, model training, evaluation,
and a lightweight inference app.
 
## Goals
- Predict churn probability

- Identify drivers of churn

- Provide actionable segments for retention


## Tech

Python, pandas, scikit-learn


## Data Ingestion

This project acquires the dataset programmatically using the Kaggle API to ensure full reproducibility.

```bash
mkdir -p data/raw
kaggle datasets download -d yeanzc/telco-customer-churn-ibm-dataset -p data/raw --unzip
```

The raw dataset is staged in `data/raw/` and is not committed to the repository.

