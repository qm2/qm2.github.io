"""Join local image paths or use independently hosted image records unchanged."""
import json
from pathlib import Path
from functools import lru_cache

def asset_url(prefix,path):
    return path if path.startswith(('https://','http://','/')) else prefix+path

@lru_cache(maxsize=1)
def sama_media():
    return json.loads((Path(__file__).resolve().parents[1]/'museum-notes/data/sama-2026-media.json').read_text())


def responsive_attributes(record, sizes="(max-width:650px) 92vw, (max-width:1000px) 80vw, 900px"):
    """Use the shared cloud variants without changing existing local image markup."""
    key=record.get('remote_asset')
    if not key:return ''
    variants=sama_media()[str(key)]['variants']
    srcset=', '.join(f'{v["path"]} {v["width"]}w' for v in variants)
    return f' srcset="{srcset}" sizes="{sizes}"'
