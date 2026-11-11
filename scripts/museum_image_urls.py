"""Resolve verified, migrated image prefixes without changing photo identities.

Object keys retain their repository-relative paths. Removing a prefix from the
configuration restores the generator's original local URLs on the next build.
This module contains no upload credentials and performs no network requests.
"""
import json
from pathlib import Path, PurePosixPath
from urllib.parse import quote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
HOSTS = json.loads((ROOT / 'museum-notes/image-hosts.json').read_text())
for prefix, origin in HOSTS.items():
    parsed = urlsplit(origin)
    if (not prefix.startswith('museum-notes/') or not prefix.endswith('/images/')
            or '..' in PurePosixPath(prefix).parts or parsed.scheme != 'https'
            or not parsed.netloc or parsed.path or parsed.query or parsed.fragment
            or parsed.username or parsed.password):
        raise ValueError('Invalid public image host configuration')


def image_url(repository_path, local_url):
    """Return a configured public URL, or the caller's existing local URL."""
    path = PurePosixPath(repository_path)
    if path.is_absolute() or '..' in path.parts:
        raise ValueError('Expected repository-relative image path')
    key = path.as_posix()
    for prefix in sorted(HOSTS, key=len, reverse=True):
        if key.startswith(prefix):
            return HOSTS[prefix] + '/' + quote(key, safe='/')
    return local_url
