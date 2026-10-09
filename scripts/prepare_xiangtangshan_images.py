"""Regenerate derived JPEGs from the unchanged, organized local photo archive.

Usage: python3 scripts/prepare_xiangtangshan_images.py /path/to/xiangtangshan-organized
Requires Pillow only for this optional image preparation step, not the site build.
"""
from pathlib import Path
import hashlib,json,sys
from PIL import Image,ImageOps
base=Path(__file__).resolve().parents[1]/'museum-notes/xiangtangshan'
source=Path(sys.argv[1]);data=json.loads((base/'data/works.json').read_text())
for a in data['assets']:
 path=source/a['organized_path']
 assert hashlib.sha256(path.read_bytes()).hexdigest()==a['sha256'],path
 if 'web_path' not in a:continue
 im=ImageOps.exif_transpose(Image.open(path)).convert('RGB');im.thumbnail((1800,1800))
 assert im.size==(a['web_width'],a['web_height'])
 im.save(base/a['web_path'],quality=88,optimize=True)
 im.thumbnail((600,600));assert im.size==(a['thumbnail_width'],a['thumbnail_height'])
 im.save(base/a['thumbnail_path'],quality=80,optimize=True)
print('Verified 45 originals; prepared 43 shared large images and thumbnails. Originals unchanged.')
