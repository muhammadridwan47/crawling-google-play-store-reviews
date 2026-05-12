import pandas as pd
from .logging_config import logger


def auto_label_data(data: pd.DataFrame) -> pd.DataFrame:
    """Label reviews based on rating: 1-2 Negatif, 3 Netral, 4-5 Positif."""
    logger.info("Starting: Auto Labeling Process")
    label = []
    for _, row in data.iterrows():
        if row["rating"] <= 2:
            label.append("Negatif")
        elif row["rating"] == 3:
            label.append("Netral")
        else:
            label.append("Positif")
    data["label"] = label
    logger.info(f"✓ Labeling completed: {len(data)} rows labeled")
    return data


def save_labeled_data(data: pd.DataFrame, path: str = 'data/bank-permata-labeling-data-set.csv'):
    data.to_csv(path, index=False)
    logger.info(f"✓ Labeled data saved to: {path}")
