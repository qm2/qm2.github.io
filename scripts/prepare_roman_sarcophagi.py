"""Generate honest responsive derivatives from Merton's unchanged originals.

No network access. Source filenames, rotations and crop boxes live in photos.json.
Never enlarges a source, edits an original, or infers a new object from a photo.
"""
from pathlib import Path
import json
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'museum-notes/roman-sarcophagi'

def prepare():
    path = BASE / 'data/photos.json'
    photos = json.loads(path.read_text())
    for key, p in photos.items():
        original = photos[p['source']]['original'] if p.get('source') else p['original']
        with Image.open(BASE / 'images/originals' / original) as opened:
            im = ImageOps.exif_transpose(opened).convert('RGB')
        if p.get('rotation'):
            im = im.rotate(p['rotation'], expand=True)
        if p.get('crop'):
            x1,y1,x2,y2 = p['crop']; w,h = im.size
            im = im.crop((round(x1*w),round(y1*h),round(x2*w),round(y2*h)))
        p['display_width'], p['display_height'] = im.size
        p['variants'] = []
        for width in sorted(set(min(im.width, s) for s in (400, 960, 1600, im.width))):
            name = f'{key}-{width}.webp'
            target = BASE / 'images' / name
            if not target.exists():
                output = im.resize((width, round(width*im.height/im.width)), Image.Resampling.LANCZOS)
                output.save(target, 'WEBP', quality=86, method=6)
            p['variants'].append({'width':width, 'file':name})
        p['full'] = p['variants'][-1]['file']
    path.write_text(json.dumps(photos, ensure_ascii=False, indent=2)+'\n')
    print(f'Prepared {len(photos)} photograph / crop records; originals unchanged.')

if __name__ == '__main__':
    prepare()
