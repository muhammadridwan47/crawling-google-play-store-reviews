import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from .text_preprocessing import text_preprocessing
from .gata_api import send_to_gata_framework
from .logging_config import logger


def remove_slang(text: str, slank_dict: dict) -> str:
    words = text.split()
    mapped = [slank_dict.get(w.lower(), w) for w in words]
    return ' '.join(mapped)


def remove_stopwords(text: str, stopword_set: set) -> str:
    words = text.split()
    filtered = [w for w in words if w.lower() not in stopword_set]
    return ' '.join(filtered)


def process_single_row(row, slank_dict: dict, stopword_set: set):
    row_num = row.get('no', 'Unknown')
    logger.debug(f"Processing row {row_num}")

    txt = text_preprocessing(row['ulasan'])
    result = row.copy()

    txt = remove_slang(txt, slank_dict)
    result['slang'] = txt

    txt = remove_stopwords(txt, stopword_set)
    result['indonesian_stopword_removal'] = txt

    txt = send_to_gata_framework(txt, '3')
    result['indonesian_stemming'] = txt

    logger.debug(f"✓ Row {row_num} completed")
    return result


def process_text_mining(df: pd.DataFrame, slank_dict: dict, stopword_set: set, max_workers: int = 4) -> pd.DataFrame:
    total_rows = len(df)
    logger.info(f"Starting text mining processing with {total_rows} rows using {max_workers} workers...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_single_row, row, slank_dict, stopword_set): idx for idx, (_, row) in enumerate(df.iterrows())}
        results = []
        completed = 0
        for future in as_completed(futures):
            completed += 1
            result = future.result()
            results.append(result)
            logger.info(f"Progress: {completed}/{total_rows} ({(completed/total_rows)*100:.1f}%)")
    logger.info(f"✓ Text mining processing completed! Total rows processed: {total_rows}")
    return pd.DataFrame(results)
