"""BM25 retrieval with the permission filter applied before scoring."""
import math
import re
from collections import Counter

from .documents import Chunk

TOKEN = re.compile(r'[a-z0-9]+')
STOPWORDS = {'a', 'an', 'the', 'is', 'are', 'what', 'who', 'how', 'for', 'to', 'of', 'in', 'on', 'do', 'does', 'i', 'my', 'must', 'should', 'be', 'by', 'and', 'or', 'with', 'at', 'before'}


def tokenize(text: str) -> list[str]:
    return [t for t in TOKEN.findall(text.lower()) if t not in STOPWORDS]


class BM25Index:
    def __init__(self, chunks: list[Chunk], k1: float = 1.5, b: float = 0.75):
        self.chunks = chunks
        self.term_counts = [Counter(tokenize(f'{c.title} {c.text}')) for c in chunks]
        self.lengths = [sum(tc.values()) for tc in self.term_counts]
        self.avg_length = sum(self.lengths) / max(len(self.lengths), 1)
        document_frequency = Counter(term for tc in self.term_counts for term in tc)
        n = len(chunks)
        self.idf = {term: math.log(1 + (n - df + 0.5) / (df + 0.5)) for term, df in document_frequency.items()}
        self.k1, self.b = k1, b

    def search(self, query: str, role: str, k: int = 3) -> list[tuple[float, Chunk]]:
        terms = tokenize(query)
        scored = []
        for i, chunk in enumerate(self.chunks):
            # Filter by permission first, so restricted text never reaches ranking or the model.
            if not chunk.visible_to(role):
                continue
            tf, length = self.term_counts[i], self.lengths[i]
            norm = self.k1 * (1 - self.b + self.b * length / self.avg_length)
            score = sum(self.idf[t] * tf[t] * (self.k1 + 1) / (tf[t] + norm) for t in terms if t in tf)
            if score > 0:
                scored.append((score, chunk))
        scored.sort(key=lambda item: -item[0])
        return scored[:k]
