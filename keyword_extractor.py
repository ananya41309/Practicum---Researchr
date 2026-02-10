import re
from collections import Counter

STOPWORDS = {
    "the", "and", "of", "to", "in", "for", "on", "with", "as", "by",
    "an", "is", "are", "was", "were", "this", "that", "from", "or",
    "at", "be", "has", "have", "it", "its", "we", "our"
}

def extract_keywords(text, top_n=10):
    # lowercase
    text = text.lower()

    # remove punctuation & numbers
    text = re.sub(r"[^a-z\s]", "", text)

    words = text.split()

    # remove stopwords & short words
    filtered = [
        word for word in words
        if word not in STOPWORDS and len(word) > 3
    ]

    word_counts = Counter(filtered)

    # return top N keywords
    return [word for word, _ in word_counts.most_common(top_n)]
