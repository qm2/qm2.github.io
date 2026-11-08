"""Import the 44 original photographs once; make reversible, upright WebP derivatives."""
from pathlib import Path
from PIL import Image,ImageOps
import csv,json,hashlib,shutil,sys
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'museum-notes/greek-roman-bronzes'
PACK=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/home/qingxi/museum/greek-roman-bronzes-codex-pack')
images=BASE/'images';originals=images/'originals';originals.mkdir(parents=True,exist_ok=True)
captions=json.loads((BASE/'data/photo-captions.json').read_text());photos={}
for row in csv.DictReader((PACK/'image_manifest.csv').open(encoding='utf-8-sig')):
 if row['role']=='excluded_unrelated':continue
 n=row['number'];src=PACK/row['package_path'];dst=originals/src.name
 assert hashlib.sha256(src.read_bytes()).hexdigest()==row['sha256']
 if not dst.exists():shutil.copyfile(src,dst)
 assert dst.read_bytes()==src.read_bytes()
 im=ImageOps.exif_transpose(Image.open(dst)).convert('RGB');rotation={'1966':90,'1992':90,'1993':-90}.get(n,0)
 if rotation:im=im.rotate(rotation,expand=True)
 width,height=im.size;variants=[]
 for w in sorted(set(min(width,s) for s in [400,960,1600,width])):
  name=f'{n}-{w}.webp';target=images/name
  if not target.exists():im.resize((w,round(height*w/width)),Image.Resampling.LANCZOS).save(target,'WEBP',quality=87,method=6)
  variants.append(dict(width=w,file=name))
 photos[n]=dict(original=dst.name,sha256=row['sha256'],role=row['role'],works=row['object_ids'].split(';'),display_width=width,display_height=height,rotation=rotation,variants=variants,full=variants[-1]['file'],caption=captions[n])
(BASE/'data/photos.json').write_text(json.dumps(photos,ensure_ascii=False,indent=2)+'\n')
print(f'Prepared {len(photos)} originals; all hashes match the handoff.')
