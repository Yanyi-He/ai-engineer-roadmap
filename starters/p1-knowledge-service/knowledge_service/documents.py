"""Load markdown documents with a small front-matter header and split them into chunks."""
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

FRONT_MATTER = re.compile(r'---\n(.*?)\n---\n(.*)', re.S)


@dataclass(frozen=True)
class Chunk:
    doc_id: str
    title: str
    roles: frozenset
    version: str
    chunk_id: str
    text: str

    def visible_to(self, role: str) -> bool:
        return 'everyone' in self.roles or role in self.roles


def parse_document(path: Path) -> tuple[dict, str]:
    match = FRONT_MATTER.match(path.read_text(encoding='utf-8'))
    if not match:
        raise ValueError(f'Missing front matter: {path.name}')
    meta = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(':')
        meta[key.strip()] = value.strip()
    if 'id' not in meta:
        raise ValueError(f'Missing id: {path.name}')
    return meta, match.group(2).strip()


def load_chunks(folder: Path, max_chars: int = 600) -> list[Chunk]:
    """Paragraph-based chunks; the version hash changes whenever the document body changes."""
    chunks = []
    for path in sorted(folder.glob('*.md')):
        meta, body = parse_document(path)
        roles = frozenset(r.strip() for r in meta.get('roles', 'everyone').split(',') if r.strip())
        version = hashlib.sha256(body.encode()).hexdigest()[:12]
        buffer, number = '', 0
        for paragraph in [p.strip() for p in body.split('\n\n') if p.strip()] + ['']:
            if paragraph and len(buffer) + len(paragraph) + 2 <= max_chars:
                buffer = f'{buffer}\n\n{paragraph}'.strip()
                continue
            if buffer:
                chunks.append(Chunk(meta['id'], meta.get('title', meta['id']), roles, version, f"{meta['id']}#{number}", buffer))
                number += 1
            buffer = paragraph
    return chunks
