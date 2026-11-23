"""Crop only Merton's originals; no enlargement, color changes or altered source files."""
import json,sys,hashlib
from pathlib import Path
from PIL import Image,ImageOps
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'museum-notes/pala-stone'
originals=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/home/qingxi/museum/pala-stone-assets/originals')
media=json.loads((B/'data/media.json').read_text());rows=json.loads((B/'data/details.json').read_text());out=originals.parent/'images/details';out.mkdir(parents=True,exist_ok=True)
for r in rows:
 m=media[str(r['photo'])];src=originals/m['original_filename'];assert hashlib.sha256(src.read_bytes()).hexdigest()==m['sha256'],src
 im=ImageOps.exif_transpose(Image.open(src)).convert('RGB');box=tuple(round(v*(im.width if i%2==0 else im.height)) for i,v in enumerate(r['box']));im=im.crop(box)
 r.update(source_sha256=m['sha256'],pixel_box=box,width=im.width,height=im.height,variants=[])
 for width in sorted(set([min(360,im.width),im.width])):
  target=im.resize((width,round(im.height*width/im.width)),Image.Resampling.LANCZOS);name=f'{r["id"]}-{width}.webp';target.save(out/name,'WEBP',quality=88)
  r['variants'].append({'url':'https://images.mertonmuseum.com/museum-notes/pala-stone/images/details/'+name,'sha256':hashlib.sha256((out/name).read_bytes()).hexdigest(),'width':target.width,'height':target.height})
(B/'data/details.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');print('Prepared',len(rows),'detail crops; originals unchanged.')
