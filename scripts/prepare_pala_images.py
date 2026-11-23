"""Prepare only the author's 48 photographs; original bytes stay outside Git and on R2."""
from pathlib import Path
from PIL import Image,ImageOps
import hashlib,json,shutil,sys
from concurrent.futures import ThreadPoolExecutor
BASE=Path(__file__).resolve().parents[1]/'museum-notes/pala-stone'
def prepare(pack,out):
 out.mkdir(exist_ok=True,parents=True);media={};manifest=[]
 paths=sorted(p for p in pack.rglob('*.jpg') if p.name.startswith('Image_'))
 assert len(paths)==48
 def one(src):
  n=src.name.split('_')[-2];original=out/'originals'/src.name;original.parent.mkdir(exist_ok=True);shutil.copyfile(src,original)
  im=ImageOps.exif_transpose(Image.open(src)).convert('RGB');w,h=im.size;variants=[];files=[(original,'image/jpeg')]
  for width in sorted({min(w,x) for x in [400,900,1600]}):
   dest=out/'images'/f'{n}-{width}.webp';dest.parent.mkdir(exist_ok=True);height=round(h*width/w)
   im.resize((width,height),Image.Resampling.LANCZOS).save(dest,'WEBP',quality=88,method=4)
   variants.append({'url':'https://images.mertonmuseum.com/museum-notes/pala-stone/'+dest.relative_to(out).as_posix(),'width':width,'height':height});files.append((dest,'image/webp'))
  entry={'id':n,'original_filename':src.name,'source_folder':src.parent.name,'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'width':w,'height':h,'role':'artwork' if int(n)%2==0 else 'label','original_url':'https://images.mertonmuseum.com/museum-notes/pala-stone/originals/'+src.name,'variants':variants}
  jobs=[{'source':str(p),'key':'museum-notes/pala-stone/'+p.relative_to(out).as_posix(),'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'content_type':ct} for p,ct in files]
  return n,entry,jobs
 with ThreadPoolExecutor(max_workers=4) as ex:
  for n,m,jobs in ex.map(one,paths):media[n]=m;manifest.extend(jobs)
 (BASE/'data/media.json').write_text(json.dumps(media,ensure_ascii=False,indent=2)+'\n');(out/'upload-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(len(media),'originals;',len(manifest),'assets;',round(sum(x['size'] for x in manifest)/1e6,1),'MB')
if __name__=='__main__':prepare(Path(sys.argv[1]),Path(sys.argv[2]))
