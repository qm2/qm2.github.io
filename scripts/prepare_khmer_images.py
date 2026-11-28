"""Preserve the supplied originals; create full-frame responsive previews on R2."""
from pathlib import Path
from PIL import Image,ImageOps
import json,hashlib,shutil,sys
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'museum-notes/khmer-art'
HOST='https://images.mertonmuseum.com/museum-notes/khmer-art/'
ROTATE={3539:90,3543:90,3545:90,3557:-90,3609:90,3612:-90,3614:90,3618:90,3620:90,3644:90}
def prepare(pack,out):
 rows=json.loads((BASE/'data/photo_manifest.json').read_text());existing=json.loads((BASE/'data/media.json').read_text()) if (BASE/'data/media.json').exists() else {};out.mkdir(parents=True,exist_ok=True)
 def one(r):
  n=r.get('key') or r['number'];src=(pack.parent/r['package'] if r.get('package') else pack)/r['path'];assert hashlib.sha256(src.read_bytes()).hexdigest()==r['sha256']
  orig=out/'originals'/src.name;orig.parent.mkdir(exist_ok=True);shutil.copyfile(src,orig)
  im=ImageOps.exif_transpose(Image.open(src)).convert('RGB');rot=ROTATE.get(n,0)
  if rot:im=im.rotate(rot,expand=True)
  w,h=im.size;vs=[];files=[(orig,'image/jpeg')]
  for width in sorted({min(w,x) for x in [400,900,1600]}):
   dest=out/'images'/f"{n}{existing.get(str(n),{}).get('derivative_version','')}-{width}.webp";dest.parent.mkdir(exist_ok=True);height=round(h*width/w)
   im.resize((width,height),Image.Resampling.LANCZOS).save(dest,'WEBP',quality=89,method=4)
   vs.append({'url':HOST+dest.relative_to(out).as_posix(),'width':width,'height':height});files.append((dest,'image/webp'))
  return str(n),dict(existing.get(str(n),{}),**dict(r,original_url=HOST+'originals/'+src.name,rotation=rot,display_width=w,display_height=h,variants=vs)),[{'source':str(p),'key':'museum-notes/khmer-art/'+p.relative_to(out).as_posix(),'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'content_type':ct} for p,ct in files]
 media={};jobs=[]
 with ThreadPoolExecutor(max_workers=4) as ex:
  for k,m,j in ex.map(one,rows):media[k]=m;jobs+=j
 (BASE/'data/media.json').write_text(json.dumps(media,ensure_ascii=False,indent=2)+'\n');(out/'upload-manifest.json').write_text(json.dumps(jobs,indent=2)+'\n')
 print(len(media),'originals,',len(jobs),'assets,',round(sum(j['size'] for j in jobs)/1e6,1),'MB')
if __name__=='__main__':prepare(Path(sys.argv[1]),Path(sys.argv[2]))
