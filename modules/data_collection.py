from google_play_scraper import reviews, Sort
from .logging_config import logger

APP_ID = 'net.myinfosys.PermataMobileX'


def fetch_reviews_from_playstore(count: int = 10, lang: str = 'id', country: str = 'id'):
    """Scrape reviews from Google Play Store for Permata Bank app."""
    logger.info("Starting: Fetch Reviews from Google Play Store")
    result, _ = reviews(
        APP_ID,
        lang=lang,
        country=country,
        sort=Sort.NEWEST,
        count=count,
    )
    logger.info(f"✓ Successfully fetched {len(result)} reviews")
    return result
