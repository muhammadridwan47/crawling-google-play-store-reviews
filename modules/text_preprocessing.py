import re


def text_preprocessing(text: str) -> str:
    """Clean and normalize text."""
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    emoticon_pattern = re.compile(r'(?::|;|=)(?:-)?(?:\)|\(|D|P|O)')
    text = emoticon_pattern.sub('', text)
    text = re.sub(r'#\w+', '', text)
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text
