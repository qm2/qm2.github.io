"""Explicit, reproducible crops of personal originals; no enlargement or retouching."""
from pathlib import Path
from PIL import Image, ImageOps
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'museum-notes/khmer-art/data'
OUT=Path('/home/qingxi/museum/khmer-art-assets');PREFIX='museum-notes/khmer-art/'
def main():
 media=json.loads((DATA/'media.json').read_text());details=json.loads((DATA/'details.json').read_text());manifest=json.loads((OUT/'upload-manifest.json').read_text())
 for d in details:
  m=media[d['photo']];package='khmer-kimbell-harihara-addendum' if d['photo'].startswith('k03') else 'khmer-art-codex-pack';src=Path('/home/qingxi/museum')/package/m['path']
  assert hashlib.sha256(src.read_bytes()).hexdigest()==m['sha256']
  im=ImageOps.exif_transpose(Image.open(src));x0,y0,x1,y1=d['box'];assert 0<=x0<x1<=im.width and 0<=y0<y1<=im.height
  im=im.crop(d['box']);d.update(width=im.width,height=im.height,source_sha256=m['sha256'],variants=[])
  for width in sorted(set([min(320,im.width),im.width])):
   thumb=im.resize((width,round(im.height*width/im.width)),Image.Resampling.LANCZOS);name=f'detail-{d["id"]}-v1-{width}.webp';p=OUT/'images'/name;thumb.save(p,quality=91,method=6)
   key=PREFIX+'images/'+name;d['variants'].append(dict(url='https://images.mertonmuseum.com/'+key,width=thumb.width,height=thumb.height))
   manifest=[r for r in manifest if r['key']!=key];manifest.append(dict(source=str(p),key=key,size=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),content_type='image/webp'))
 (DATA/'details.json').write_text(json.dumps(details,ensure_ascii=False,indent=2)+'\n');(OUT/'upload-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(f'{len(details)} detail crops from existing originals')
if __name__=='__main__':main()
