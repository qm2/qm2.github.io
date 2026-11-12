"""Generate SAMA responsive images outside Git; preserve verified original JPEGs.

Usage: python3 scripts/prepare_sama_images.py PACKAGE_DIR OUTPUT_DIR
Upload remains a separate, explicit operation.
"""
import json,hashlib,shutil,argparse
from pathlib import Path
from PIL import Image,ImageOps
from concurrent.futures import ThreadPoolExecutor
args=argparse.ArgumentParser();args.add_argument('package',type=Path);args.add_argument('output',type=Path);opts=args.parse_args()
R=Path(__file__).resolve().parents[1];P=opts.package.resolve();OUT=opts.output.resolve()
if OUT.is_relative_to(R):raise SystemExit('Keep the photo archive outside the Git repository.')
OUT.mkdir(exist_ok=True,parents=True)
records=json.loads((P/'catalogue.json').read_text())['records'];rows=[]
base='https://images.mertonmuseum.com/museum-notes/sama-2026/'
def one(pair):
 w,p=pair;n=str(p['number']);src=P/p['file'];raw=src.read_bytes();assert hashlib.sha256(raw).hexdigest()==p['sha256'];im=ImageOps.exif_transpose(Image.open(src)).convert('RGB');vs=[]
 dest=OUT/'originals'/p['original_name'];dest.parent.mkdir(exist_ok=True);shutil.copyfile(src,dest)
 for size in sorted(set([min(s,im.width) for s in [400,900,1600,im.width]])):
  dst=OUT/f'{n}-{size}.webp';h=round(im.height*size/im.width);im.resize((size,h),Image.Resampling.LANCZOS).save(dst,'WEBP',quality=88,method=5);vs.append(dict(path=base+dst.name,file=base+dst.name,width=size,height=h))
 return n,dict(width=im.width,height=im.height,variants=vs,full=vs[-1]['path'],original=base+'originals/'+p['original_name'],sha256=p['sha256'],original_filename=p['original_name'],role=p['role'],package_id=w['id'],bytes=len(raw))
with ThreadPoolExecutor(max_workers=6) as ex:media=dict(ex.map(one,[(w,p) for w in records if w['status']=='include' for p in w['photos']]))
(R/'museum-notes/data/sama-2026-media.json').write_text(json.dumps(media,ensure_ascii=False,indent=2)+'\n')
for p in sorted(OUT.rglob('*')):
 if p.suffix not in ['.webp','.jpg']:continue
 raw=p.read_bytes();rows.append(dict(source=str(p),key='museum-notes/sama-2026/'+p.relative_to(OUT).as_posix(),sha256=hashlib.sha256(raw).hexdigest(),size=len(raw),content_type='image/jpeg' if p.suffix=='.jpg' else 'image/webp'))
(OUT/'upload-manifest.json').write_text(json.dumps(rows,indent=2)+'\n');print(len(media),'originals;',len(rows),'assets;',round(sum(r['size'] for r in rows)/1e6,1),'MB')
