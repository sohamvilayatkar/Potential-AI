"""
NLP Preprocessing Module for Potential AI.
Provides text cleaning, tokenization, normalization, and entity keyword extraction.
Guarantees safe fallback if NLTK corpora are not yet downloaded.
"""

import re
import string

# Safe NLTK imports with try-except fallbacks
_STEMMER = None
try:
    import nltk
    from nltk.stem import PorterStemmer
    _STEMMER = PorterStemmer()
except Exception:
    _STEMMER = None

# Custom college stop words that do not alter intent meaning
CUSTOM_STOPWORDS = {
    'a', 'an', 'the', 'is', 'are', 'was', 'were', 'am', 'be', 'been', 'being',
    'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'about',
    'please', 'tell', 'me', 'give', 'show', 'i', 'want', 'know', 'can', 'you'
}

def clean_text(text: str) -> str:
    """
    Standardize text: lowercase, remove special characters/punctuation, normalize whitespace.
    """
    if not text:
        return ""
    text = text.lower()
    # Replace punctuation with spaces
    text = re.sub(r'[' + re.escape(string.punctuation) + r']', ' ', text)
    # Normalize multiple whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize(text: str) -> list:
    """
    Tokenize cleaned text into word tokens.
    """
    cleaned = clean_text(text)
    if not cleaned:
        return []
    return cleaned.split()

def preprocess_query(text: str, remove_stopwords: bool = False) -> str:
    """
    Full pipeline to clean and normalize a user query.
    """
    tokens = tokenize(text)
    if remove_stopwords:
        tokens = [t for t in tokens if t not in CUSTOM_STOPWORDS]
    if _STEMMER:
        tokens = [_STEMMER.stem(t) for t in tokens]
    return " ".join(tokens)

def extract_entities(query: str) -> dict:
    """
    Extract key college entities: Department, Program, Information Type from user query.
    Uses rule-based synonym mapping with word boundaries.
    """
    q = clean_text(query)
    entities = {
        "department": None,
        "department_name": None,
        "program": None,
        "academic_year": None,
        "info_type": None
    }

    # Department identification with word boundaries for short tokens
    if re.search(r'\b(cse|computer science|computer engineering|computer|comp)\b', q):
        if re.search(r'\b(aiml|ai ml|machine learning)\b', q):
            entities["department"] = "cse_aiml"
            entities["department_name"] = "Computer Science and Engineering (Artificial Intelligence & Machine Learning)"
        else:
            entities["department"] = "cse"
            entities["department_name"] = "Computer Science and Engineering"
    elif re.search(r'\b(aids|ai ds|data science|artificial intelligence)\b', q):
        entities["department"] = "aids"
        entities["department_name"] = "Artificial Intelligence and Data Science"
    elif re.search(r'\b(mechanical|mech|me)\b', q):
        entities["department"] = "me"
        entities["department_name"] = "Mechanical Engineering"
    elif re.search(r'\b(electrical|ee|power system)\b', q):
        entities["department"] = "ee"
        entities["department_name"] = "Electrical Engineering"
    elif re.search(r'\b(civil|ce)\b', q):
        entities["department"] = "ce"
        entities["department_name"] = "Civil Engineering"
    elif re.search(r'\b(extc|electronics and telecommunication|electronics|telecom)\b', q):
        entities["department"] = "extc"
        entities["department_name"] = "Electronics and Telecommunication Engineering"
    elif re.search(r'\b(first year|applied science|fe|fy)\b', q):
        entities["department"] = "fy"
        entities["department_name"] = "First Year Engineering (Applied Science & Humanities)"
    elif re.search(r'\b(mba|management)\b', q):
        entities["department"] = "mba"
        entities["department_name"] = "Master of Business Administration"
    elif re.search(r'\b(mca|computer applications)\b', q):
        entities["department"] = "mca"
        entities["department_name"] = "Master of Computer Applications"

    # Program identification
    if re.search(r'\b(btech|b tech|b e|bachelor|undergraduate|ug)\b', q):
        entities["program"] = "btech"
    elif re.search(r'\b(mtech|m tech|m e|postgraduate|pg|master)\b', q):
        entities["program"] = "mtech"
    elif re.search(r'\b(mba)\b', q):
        entities["program"] = "mba"
    elif re.search(r'\b(mca)\b', q):
        entities["program"] = "mca"

    # Academic year extraction if mentioned
    year_match = re.search(r'20[2-3][0-9][\s\-_/]?20?[2-3][0-9]', q)
    if year_match:
        entities["academic_year"] = year_match.group(0)

    return entities
