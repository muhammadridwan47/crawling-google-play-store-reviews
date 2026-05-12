import os
import pandas as pd
from .logging_config import logger


def prepare_dataframe(raw_reviews):
    """Format raw reviews into structured DataFrame."""
    logger.info("Starting: Data Preparation")
    df = pd.DataFrame(raw_reviews)
    df = df[['content', 'score', 'at']]
    df.columns = ['ulasan', 'rating', 'tanggal']
    df['no'] = range(1, len(df) + 1)
    cols = ['no'] + [c for c in df.columns if c != 'no']
    df = df[cols]
    df['label'] = ""
    logger.info(f"✓ Data preparation completed: {len(df)} rows")
    return df


def save_raw_data(df, path: str = 'data/bank-permata-data-set.csv'):
    os.makedirs('data', exist_ok=True)
    df.to_csv(path, index=False)
    logger.info(f"✓ Raw data saved to: {path}")
