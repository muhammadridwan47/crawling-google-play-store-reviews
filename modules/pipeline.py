from .logging_config import logger
from .data_collection import fetch_reviews_from_playstore
from .data_preparation import prepare_dataframe, save_raw_data
from .labeling import auto_label_data, save_labeled_data
from .dictionaries import load_dictionaries
from .text_mining import process_text_mining
from .exporting import export_results


def main():
    logger.info("=" * 80)
    logger.info("STARTING PERMATA BANK REVIEWS ANALYSIS PIPELINE")
    logger.info("=" * 80)

    try:
        logger.info("\n[STEP 1/6] Fetching reviews from Google Play Store...")
        raw_reviews = fetch_reviews_from_playstore()

        logger.info("\n[STEP 2/6] Preparing dataframe...")
        df = prepare_dataframe(raw_reviews)
        save_raw_data(df)

        logger.info("\n[STEP 3/6] Applying auto labeling...")
        labeled_data = auto_label_data(df)
        save_labeled_data(labeled_data)

        logger.info("\n[STEP 4/6] Loading dictionaries...")
        slank_dict, stopword_set = load_dictionaries()

        logger.info("\n[STEP 5/6] Processing text mining...")
        processed_df = process_text_mining(labeled_data, slank_dict, stopword_set, max_workers=4)

        logger.info("\n[STEP 6/6] Exporting results...")
        export_results(processed_df)

        logger.info("\n" + "=" * 80)
        logger.info("✓ PIPELINE COMPLETED SUCCESSFULLY!")
        logger.info("=" * 80)

    except Exception as e:
        logger.error(f"✗ Pipeline failed with error: {str(e)}", exc_info=True)
        raise
