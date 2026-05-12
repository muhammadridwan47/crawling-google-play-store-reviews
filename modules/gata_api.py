import time
import urllib.parse
import urllib.request
from .logging_config import logger

BASE_URL = "http://www.gataframework.com/textmining/index.php?model=transaction_text&action=processTextPublic&techniques="


def send_to_gata_framework(text: str, technique: str, max_retries: int = 3, retry_delay: float = 0.1) -> str:
    """Call GataFramework API and return processed text (or 'time out')."""
    encoded_text = urllib.parse.quote_plus(text.strip())
    url = f"{BASE_URL}{technique}&textbefore={encoded_text}"

    technique_name = {
        '3': 'Stemming',
        '10': 'Slang Removal',
        '2': 'Stopword Removal',
    }.get(technique, technique)

    for attempt in range(max_retries + 1):
        try:
            logger.info(f"Calling GataFramework API - Technique: {technique_name} (attempt {attempt + 1}/{max_retries + 1})")
            with urllib.request.urlopen(url) as response:
                result = response.read().decode('utf-8')
                logger.info(f"✓ GataFramework API Success - {technique_name}")
                time.sleep(0.03)
                return result
        except Exception as e:
            logger.warning(f"✗ GataFramework API Error - {technique_name}: {str(e)}")
            if attempt < max_retries:
                wait_time = retry_delay * (attempt + 1)
                logger.info(f"Retrying in {wait_time}s...")
                time.sleep(wait_time)
                continue
            logger.error(f"✗ GataFramework API Failed after {max_retries + 1} attempts - {technique_name}")
            return "time out"
    return "time out"
