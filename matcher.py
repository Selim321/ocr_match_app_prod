import re
from difflib import SequenceMatcher

def preprocess_name(name):
    # Convert to lowercase and remove non-alphanumeric characters
    return re.sub(r'[^a-z0-9\s]', '', name.lower()).split()

def word_similarity(word1, word2):
    return SequenceMatcher(None, word1, word2).ratio()

def match_product_names(receipt_name, database_names, similarity_threshold=0.8):
    receipt_words = preprocess_name(receipt_name)

    best_match = None
    max_match_ratio = 0

    for db_name in database_names:
        db_words = preprocess_name(db_name)

        # Check if all database words are present in the receipt name
        words_matched = 0
        for db_word in db_words:
            if any(word_similarity(db_word, receipt_word) >= similarity_threshold for receipt_word in receipt_words):
                words_matched += 1

        # Calculate match ratio
        match_ratio = words_matched / len(db_words)

        # Update best match if this is better
        if match_ratio > max_match_ratio:
            max_match_ratio = match_ratio
            best_match = db_name

    # Return the best match if it's a complete match, otherwise None
    return best_match if max_match_ratio == 1 else None



def check_match(scanned_name: str, product_name: str, alternate_names: List[str], threshold: float = 0.3, n: int = 2) -> Tuple[bool, List[str]]:
    """Check if the scanned name matches the product name or any of the alternate names."""
    words_list = [product_name] + alternate_names
    matches = match_product_names(scanned_name, words_list)

    return bool(matches), matches