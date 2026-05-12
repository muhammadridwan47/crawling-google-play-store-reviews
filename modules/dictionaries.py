import json
from .logging_config import logger


def load_dictionaries(slank_path: str = 'slank.json', stopword_path: str = 'stopword.json'):
    """Load slang dictionary and stopword list from JSON files."""
    logger.info("Starting: Load Dictionaries")
    with open(slank_path, 'r', encoding='utf-8') as f:
        slank_data = json.load(f)
    slank_dict = {item['slank'].lower(): item['slankmean'].lower() for item in slank_data}

    with open(stopword_path, 'r', encoding='utf-8') as f:
        stopword_list = json.load(f)
    stopword_set = set(word.lower() for word in stopword_list)

    logger.info(f"✓ Dictionaries loaded: {len(slank_dict)} slang words, {len(stopword_set)} stopwords")
    return slank_dict, stopword_set
