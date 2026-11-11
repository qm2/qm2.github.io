"""Prepare self-photographed Etruscan assets outside Git; retain byte-identical originals.
Usage: python3 scripts/prepare_etruscans_images.py PACKAGE_DIR EXTERNAL_ASSET_DIR
"""
from pathlib import Path
import json,hashlib,sys,shutil
from PIL import Image,ImageOps
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parents[1]
def run(source,out):
 source=Path(source);out=Path(out);out.mkdir(parents=True,exist_ok=True)
 original_dir=out/'originals';original_dir.mkdir(exist_ok=True)
 photos=json.loads((source/'data/photos.json').read_text());manifest=[]
 index=ROOT/'museum-notes/etruscans/data/photos.json'
 existing={p['photo_id']:p for p in json.loads(index.read_text())} if index.exists() else {}
 def prepare(p):
  origin=source/p['path'];digest=hashlib.sha256(origin.read_bytes()).hexdigest();assert digest==p['sha256']
  name=p['photo_id'];assert name not in existing or existing[name]['sha256']==digest, 'Do not overwrite an existing photograph ID'
  original=original_dir/(name+'.jpg')
  if not original.exists():shutil.copyfile(origin,original)
  assert hashlib.sha256(original.read_bytes()).hexdigest()==digest
  im=ImageOps.exif_transpose(Image.open(origin)).convert('RGB');width,height=im.size;vs=[]
  for w in sorted(set(min(x,width) for x in [320,640,960,1600])):
   f=f'{name}-{w}.webp';path=out/f
   if not path.exists():im.resize((w,round(height*w/width)),Image.Resampling.LANCZOS).save(path,'WEBP',quality=85,method=6)
   vs.append({'file':f,'width':w})
  return {**p,**existing.get(name,{}),'path':'originals/'+name+'.jpg','source':'Merton现场摄影','display_width':width,'display_height':height,'variants':vs}
 with ThreadPoolExecutor(max_workers=4) as pool:result=list(pool.map(prepare,photos))
 crops={
 'e045':('p154',(0,50,1280,1650),'抬起的脸与胸前护符'),
 'e010':('p038',(50,400,1230,1580),'金带上的人物与细纹'),
 'e001':('p005',(380,200,1380,1200),'器沿前方的狮首'),
 'e122':('p347',(220,0,1220,1000),'头部、肩与举起的手臂'),
 'e106':('p298',(40,270,1240,1470),'小祠中央的神话人物群')}
 cropdata={}
 for wid,(pid,box,caption) in crops.items():
  im=ImageOps.exif_transpose(Image.open(source/'photos'/f'{pid}.jpg')).convert('RGB').crop(box)
  # Seated boy retains face-to-hand relation, fitted without cropping in the guide.
  vs=[]
  for w in [320,640]:
   h=round(im.height*w/im.width);f=f'{wid}-detail-{w}.webp';im.resize((w,h),Image.Resampling.LANCZOS).save(out/f,'WEBP',quality=88,method=6);vs.append({'file':f,'width':w})
  cropdata[wid]={'photo_id':pid,'crop_box':list(box),'caption':caption,'width':im.width,'height':im.height,'variants':vs}
 for path in sorted(out.rglob('*')):
  if path.is_file() and path.suffix in ['.jpg','.webp']:
   rel=path.relative_to(out).as_posix();manifest.append({'source':str(path),'key':'museum-notes/etruscans/images/'+rel,'size':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'content_type':'image/jpeg' if path.suffix=='.jpg' else 'image/webp'})
 target=ROOT/'museum-notes/etruscans/data';target.mkdir(parents=True,exist_ok=True)
 for name,data in [('photos',result),('detail-crops',cropdata)]: (target/f'{name}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 (out.parent/'etruscans-upload-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(f'{len(result)} originals, {len(manifest)} remote assets, {sum(x["size"] for x in manifest)/1e6:.1f} MB')
if __name__=='__main__':run(*sys.argv[1:])
