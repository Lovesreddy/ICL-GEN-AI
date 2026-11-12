"""NLP preprocessing, keyword extraction, and farming intent classification.

Stopwords are removed only for keyword lists. Text that is embedded or stored
keeps words such as "not", "without", and crop names so the meaning stays intact.
"""

from __future__ import annotations

import re

from app.services.embeddings import get_embedding_service

_ready = False
_stopwords: set[str] = set()
_lemmatizer_name = "identity"

FALLBACK_STOPWORDS = {
    "a", "an", "the", "and", "or", "of", "to", "in", "on", "for", "with", "from",
    "by", "at", "is", "are", "was", "were", "be", "been", "being", "this", "that",
    "these", "those", "it", "its", "as", "into", "about", "than", "then", "so",
    "if", "can", "could", "should", "would", "i", "we", "you", "they", "my", "our",
    "your", "do", "does", "did", "how", "what", "which", "when", "where", "who",
}

# Words that change agricultural meaning and must survive keyword extraction.
PROTECTED_WORDS = {"not", "no", "without", "organic", "natural", "sandy", "clay", "before", "after"}

SYNONYMS = {
    "pesticide": "pest management",
    "pesticides": "pest management",
    "insecticide": "pest management",
    "fym": "farmyard manure",
    "dung": "farmyard manure",
    "vermi compost": "vermicompost",
    "vermicomposting": "vermicompost",
    "jeevamrutha": "jeevamrutham",
    "jeevamrut": "jeevamrutham",
    "panchagavya": "panchagavya",
    "sandy soil": "sandy soil",
    "chemical pesticide": "pest management without chemical pesticides",
}

INTENTS: dict[str, list[str]] = {
    "crop_information": [
        "crop", "rice", "wheat", "tomato", "chilli", "chili", "cotton", "groundnut",
        "banana", "mango", "turmeric", "sugarcane", "variety", "sowing", "harvest", "cultivate",
    ],
    "soil_management": [
        "soil", "fertility", "sandy", "loam", "clay", "ph", "organic matter", "erosion", "seedbed",
    ],
    "organic_fertilizers": [
        "fertilizer", "fertiliser", "compost", "vermicompost", "manure", "jeevamrutham",
        "panchagavya", "neem cake", "biofertilizer", "green manure",
    ],
    "pest_management": [
        "pest", "insect", "neem", "aphid", "borer", "pesticide", "mite", "thrips", "whitefly", "trap",
    ],
    "irrigation": ["water", "irrigation", "drip", "moisture", "mulch", "drought", "flood"],
    "disease_management": ["disease", "blight", "fungus", "wilt", "mildew", "rot", "virus", "smut"],
    "general_organic_farming": ["organic", "sustainable", "certification", "rotation", "intercrop"],
}

INTENT_PRIORITY = (
    "disease_management",
    "pest_management",
    "irrigation",
    "soil_management",
    "organic_fertilizers",
    "crop_information",
    "general_organic_farming",
)

INJECTION_PATTERN = re.compile(
    r"(ignore (all|any|previous|above) (instructions|prompts)|you are now|disregard the system|"
    r"<\s*/?\s*system\s*>|reveal (the |your )?prompt)",
    re.IGNORECASE,
)


def ensure_nlp_ready() -> None:
    global _ready, _stopwords
    if not _ready:
        _stopwords = set(FALLBACK_STOPWORDS)
        _ready = True


def clean_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def remove_duplicate_paragraphs(text: str) -> str:
    paragraphs = re.split(r"\n\s*\n", text)
    seen: set[str] = set()
    kept: list[str] = []
    for paragraph in paragraphs:
        normalized = re.sub(r"\s+", " ", paragraph).strip().lower()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        kept.append(paragraph.strip())
    return "\n\n".join(kept)


def neutralize_instructions(text: str) -> str:
    """Drop lines that try to override the assistant. Agricultural sentences stay."""
    kept = []
    for line in text.splitlines():
        if INJECTION_PATTERN.search(line):
            kept.append("[removed possible instruction override]")
        else:
            kept.append(line)
    return "\n".join(kept)


def tokenize(text: str) -> list[str]:
    ensure_nlp_ready()
    tokens = re.findall(r"[A-Za-z][A-Za-z'-]*|\d+", text)
    return [token for token in tokens if re.search(r"[A-Za-z0-9]", token)]


def lemmatize(tokens: list[str]) -> list[str]:
    ensure_nlp_ready()
    return [token.lower() for token in tokens]


def keywords_from(lemmas: list[str], limit: int = 8) -> list[str]:
    counts: dict[str, int] = {}
    for lemma in lemmas:
        if len(lemma) < 3:
            continue
        if lemma in _stopwords and lemma not in PROTECTED_WORDS:
            continue
        if not lemma.isalpha():
            continue
        counts[lemma] = counts.get(lemma, 0) + 1
    ranked = sorted(counts, key=lambda item: (-counts[item], item))
    return ranked[:limit]


def normalize_query(text: str) -> str:
    lowered = clean_text(text).lower()
    lowered = lowered.replace("chili", "chilli")
    for source, target in SYNONYMS.items():
        lowered = re.sub(rf"\b{re.escape(source)}\b", target, lowered)
    lowered = re.sub(r"\s+", " ", lowered).strip()
    return lowered


def classify_intent(text: str) -> tuple[str, float, dict[str, float]]:
    haystack = normalize_query(text)
    scores: dict[str, float] = {}
    for intent, terms in INTENTS.items():
        score = 0.0
        for term in terms:
            if re.search(rf"(?<![a-z0-9]){re.escape(term)}(?:s|es)?(?![a-z0-9])", haystack):
                score += 2.0 if " " in term else 1.0
        scores[intent] = score
    best = max(INTENT_PRIORITY, key=scores.get)
    total = sum(scores.values()) or 1.0
    if scores[best] == 0:
        return "general_organic_farming", 0.2, scores
    return best, round(min(0.95, scores[best] / total + 0.25), 2), scores


def semantic_similarity(left: str, right: str) -> float | None:
    service = get_embedding_service()
    if not service.ready:
        return None
    vectors = service.embed([left, right])
    return float((vectors[0] * vectors[1]).sum())


def analyze(text: str, compare_to: str | None = None) -> dict:
    ensure_nlp_ready()
    cleaned = clean_text(text)
    tokens = tokenize(cleaned)
    lemmas = lemmatize(tokens)
    without_stops = [
        lemma for lemma in lemmas if lemma not in _stopwords or lemma in PROTECTED_WORDS
    ]
    intent, confidence, scores = classify_intent(cleaned)
    similarity = semantic_similarity(cleaned, compare_to) if compare_to else None
    return {
        "original": text,
        "cleaned": cleaned,
        "tokens": tokens[:80],
        "tokens_without_stopwords": without_stops[:80],
        "lemmas": lemmas[:80],
        "keywords": keywords_from(lemmas),
        "intent": intent,
        "confidence": confidence,
        "intent_scores": scores,
        "normalized_query": normalize_query(cleaned),
        "semantic_similarity": similarity,
        "lemmatizer": _lemmatizer_name,
    }


def looks_like_injection(text: str) -> bool:
    return bool(INJECTION_PATTERN.search(text))
