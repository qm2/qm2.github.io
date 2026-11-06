"""Regenerate atlas derivatives from recorded personal originals, without altering originals.

After adding photo records to data/atlas-photos.json, run with --source-dir pointing
to the new original archive. Existing shared reading photos are verified, not copied.
No research data, captions, object associations or original files are overwritten.
"""
from pathlib import Path
import argparse,hashlib,json,shutil
from PIL import Image,ImageOps

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'museum-notes/images-and-vows'
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source-dir',type=Path,help='Private directory containing the recorded original filenames')
parser.add_argument('--refresh',action='store_true',help='Recreate WebP derivatives; never modify original photographs')
args=parser.parse_args()
datafile=BASE/'data/atlas-photos.json'
photos=json.loads(datafile.read_text())
generated=0
for number,p in photos.items():
 original=(BASE/'atlas'/p['original']).resolve()
 assert original.is_relative_to(BASE.resolve()),original
 if not original.exists():
  assert args.source_dir,'Missing original; supply --source-dir: '+str(original)
  source=args.source_dir/p['original_filename']
  assert hashlib.sha256(source.read_bytes()).hexdigest()==p['sha256'],source
  original.parent.mkdir(parents=True,exist_ok=True)
  shutil.copy2(source,original)
 assert hashlib.sha256(original.read_bytes()).hexdigest()==p['sha256'],original
 # Shared photos retain their existing render settings and resources.
 if p['original'].startswith('../'):
  assert all((BASE/'atlas'/v['file']).exists() for v in p['variants'])
  continue
 with Image.open(original) as raw:
  image=ImageOps.exif_transpose(raw).convert('RGB')
 if p.get('rotation_ccw'):image=image.rotate(p['rotation_ccw'],expand=True)
 p['width'],p['height']=image.size
 variants=[]
 for width in sorted({min(x,image.width) for x in (400,900,1600)}):
  file=f'images/{number}-{width}.webp';dest=BASE/'atlas'/file
  if args.refresh or not dest.exists():
   dest.parent.mkdir(parents=True,exist_ok=True)
   image.resize((width,round(image.height*width/image.width)),Image.Resampling.LANCZOS).save(dest,'WEBP',quality=86,method=6)
   generated+=1
  variants.append(dict(file=file,width=width))
 p['variants']=variants;p['file']=variants[min(1,len(variants)-1)]['file']
datafile.write_text(json.dumps(photos,ensure_ascii=False,indent=2)+'\n')
print(f'Checked {len(photos)} personal originals; generated {generated} responsive images.')
