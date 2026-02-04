import os 
import pandas as pd
import sqlalchemy as sa
from sklearn.model_selection import train_test_split

def load_from_postgres(view_name: str) -> pd.DataFrame:
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        raise RuntimeError('Set DATABASE_URL to load from Postgres.')

    engine = sa.create_engine(db_url)
    query = f"SELECT * FROM {view_name}"
    return pd.read_sql(query, engine)

DEFAULT_VIEW = 'analytics.churn_features_v1'
DEFAULT_TARGET = 'churn'
DEFAULT_ID_COL = 'customer_id'

def split_xy(df: pd.DataFrame):
    X = df.drop(columns = [DEFAULT_TARGETm DEFAULT_ID_COL])
    y = df[DEFAULT_TARGET].astype(int)
    return X, y
