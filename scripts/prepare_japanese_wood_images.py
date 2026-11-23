"""Optional image intake: pack directory and outside-Git output directory. No upload or content overwrite."""
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import csv,json,hashlib,shutil,sys
from concurrent.futures import ThreadPoolExecutor
pack=Path(sys.argv[1]); base=Path(__file__).resolve().parents[1]/'museum-notes/japanese-buddhist-sculpture';out=Path(sys.argv[2]);out.mkdir(exist_ok=True);base.mkdir(exist_ok=True)
rows=list(csv.DictReader((pack/'data/photo_manifest.csv').open(encoding='utf-8-sig')));prefix='museum-notes/japanese-buddhist-sculpture/';cdn='https://images.mertonmuseum.com/'+prefix
upload=[];media={}
def make(row):
 n=row['number'];src=pack/row['path'];raw=src.read_bytes();assert hashlib.sha256(raw).hexdigest()==row['sha256']
 orig=out/'originals'/row['original_filename'];orig.parent.mkdir(exist_ok=True);shutil.copyfile(src,orig)
 im=ImageOps.exif_transpose(Image.open(src)).convert('RGB');w,h=im.size;vs=[];files=[(orig,'image/jpeg')]
 for size in sorted({min(w,400),min(w,900),min(w,1600)}):
  dest=out/'previews'/f'{n}-{size}.webp';dest.parent.mkdir(exist_ok=True);im.resize((size,round(h*size/w)),Image.Resampling.LANCZOS).save(dest,'WEBP',quality=87,method=4)
  vs.append({'url':cdn+dest.relative_to(out).as_posix(),'width':size,'height':round(h*size/w)});files.append((dest,'image/webp'))
 ent={'number':int(n),'width':w,'height':h,'original_url':cdn+orig.relative_to(out).as_posix(),'original_filename':row['original_filename'],'sha256':row['sha256'],'role':row['role'],'variants':vs}
 jobs=[]
 for f,ct in files:jobs.append({'source':str(f),'key':prefix+f.relative_to(out).as_posix(),'size':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'content_type':ct})
 return n,ent,jobs
with ThreadPoolExecutor(max_workers=4) as ex:
 for n,ent,jobs in ex.map(make,rows):media[n]=ent;upload+=jobs
(base/'data/media.json').write_text(json.dumps(media,ensure_ascii=False,indent=2)+'\n');(out/'upload-manifest.json').write_text(json.dumps(upload,indent=2)+'\n')
print(len(media),'photos;',len(upload),'assets;',round(sum(x['size'] for x in upload)/1024/1024,1),'MB')
