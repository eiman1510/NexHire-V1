import re
import unicodedata


# The number is the education level. A higher level can satisfy a lower one.
DEGREE_PATTERNS = [
    (1, r"\b(high school|secondary school|matriculation|intermediate|a levels?|ged)\b"),
    (2, r"\b(associates?|associate of|associate in|aa|aas)\b"),
    (3, r"\b(bachelors?|baccalaureate|undergraduate|bsc|bs|ba|beng|btech|bcom|bba|llb|b (sc|s|a|eng|tech|com))\b"),
    (4, r"\b(masters?|postgraduate|msc|ms|ma|mba|meng|mtech|mcom|mphil|llm|m (sc|s|a|eng|tech|com|phil))\b"),
    (5, r"\b(doctorates?|doctoral|doctor of|phd|dphil)\b"),
]


def normalize_education_text(value):
    """Convert degree text into simple lowercase words."""
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(char for char in text if not unicodedata.combining(char))
    text = text.replace("'", "").replace("’", "").lower()
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def get_degree_level(value):
    """Return a degree level when the text matches a known degree pattern."""
    for level, pattern in DEGREE_PATTERNS:
        if re.search(pattern, value):
            return level
    return None


def education_matches(required_education, candidate_degrees):
    """Check the required education against every degree in the resume."""
    required = normalize_education_text(required_education)
    if not required:
        return True

    if isinstance(candidate_degrees, str):
        candidate_degrees = [candidate_degrees]

    candidates = [
        normalize_education_text(degree)
        for degree in (candidate_degrees or [])
        if degree
    ]

    required_level = get_degree_level(required)
    if required_level:
        for candidate in candidates:
            candidate_level = get_degree_level(candidate)
            if candidate_level and candidate_level >= required_level:
                return True
        return False

    # For an uncommon qualification, use a word-boundary phrase match.
    words = [
        word
        for word in required.split()
        if word not in {"degree", "education", "minimum", "required", "qualification"}
    ]
    if not words:
        return False

    phrase = r"\s+".join(map(re.escape, words))
    pattern = rf"\b{phrase}\b"
    return any(re.search(pattern, candidate) for candidate in candidates)
