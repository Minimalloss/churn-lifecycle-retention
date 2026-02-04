import os
import json
from pathlib import Path

import pandas as pd
import sqlalchemy as sa

from joblib import dump

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)


DEFAULT_VIEW = 'analytics.churn_features_v1'
DEFAULT_TARGET = 'churn'
DEFAULT_ID_COL = 'customer_id'


def load_from_postgres(view_name: str) -> pd.DataFrame:
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        raise RuntimeError('Set DATABASE_URL to load from Postgres.')

    engine = sa.create_engine(db_url)
    query = f'SELECT * FROM {view_name};'
    return pd.read_sql(query, engine)


def split_xy(df: pd.DataFrame):
    X = df.drop(columns = [DEFAULT_TARGET, DEFAULT_ID_COL])
    y = df[DEFAULT_TARGET].astype(int)
    return X, y


def make_splits(X, y):
    return train_test_split(
        X, y,
        test_size = 0.2,
        random_state = 42,
        stratify = y if y.nunique() > 1 else None,
    )


def build_pipeline(X: pd.DataFrame) -> Pipeline:
    num_cols = X.select_dtypes(include = ['number', 'bool']).columns.tolist()
    cat_cols = [c for c in X.columns if c not in num_cols]

    numeric = Pipeline(
        steps=[
            ('impute', SimpleImputer(strategy = 'median')),
            ('scale', StandardScaler()),
        ]
    )

    categorical = Pipeline(
        steps = [
            ('impute', SimpleImputer(strategy = 'most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown = 'ignore')),
        ]
    )

    pre = ColumnTransformer(
        transformers = [
            ('num', numeric, num_cols),
            ('cat', categorical, cat_cols),
        ]
    )

    model = LogisticRegression(max_iter=2000, class_weight = 'balanced')

    return Pipeline(
        steps = [
            ('preprocess', pre),
            ('model', model),
        ]
    )


def evaluate(model: Pipeline, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    probs = model.predict_proba(X_test)[:, 1]
    preds = (probs >= 0.5).astype(int)

    return {
        "accuracy": float(accuracy_score(y_test, preds)),
        "precision": float(precision_score(y_test, preds, zero_division = 0)),
        "recall": float(recall_score(y_test, preds, zero_division = 0)),
        "f1": float(f1_score(y_test, preds, zero_division = 0)),
        "roc_auc": float(roc_auc_score(y_test, probs)) if y_test.nunique() > 1 else None,
    }


def main():
    df = load_from_postgres(DEFAULT_VIEW)

    X, y = split_xy(df)
    X_train, X_test, y_train, y_test = make_splits(X, y)

    pipe = build_pipeline(X_train)
    pipe.fit(X_train, y_train)

    metrics = evaluate(pipe, X_test, y_test)

    Path('artifacts').mkdir(exist_ok = True)
    dump(pipe, 'artifacts/model.joblib')

    with open('artifacts/metrics.json', 'w') as f:
        json.dump(metrics, f, indent = 2)

    print('Training complete.')
    print(metrics)


if __name__ == '__main__':
    main()
