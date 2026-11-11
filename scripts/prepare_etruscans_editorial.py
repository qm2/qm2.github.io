"""Generate editorial crops from untouched originals, with content-versioned URLs.
No upscaling, color correction, object removal or perspective alteration.
"""
from pathlib import Path
import hashlib,json,sys
from PIL import Image,ImageOps
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'museum-notes/etruscans/data'
def prepare(out):
 out=Path(out);config=json.loads((DATA/'photo-editing.json').read_text());derived={};manifest=[]
 for key,c in config['crops'].items():
  original=out/'originals'/(c['photo_id']+'.jpg')
  source=ImageOps.exif_transpose(Image.open(original)).convert('RGB');l,t,r,b=c['box']
  assert 0<=l<r<=source.width and 0<=t<b<=source.height,(key,source.size,c['box'])
  im=source.crop((l,t,r,b));token=hashlib.sha256(original.read_bytes()+json.dumps(c['box']).encode()).hexdigest()[:10];variants=[]
  for width in sorted({min(w,im.width) for w in [320,640,960,1600]}):
   name=f'{key}-{token}-{width}.webp';path=out/name
   im.resize((width,round(im.height*width/im.width)),Image.Resampling.LANCZOS).save(path,'WEBP',quality=90,method=6)
   assert Image.open(path).width==width
   variants.append({'file':name,'width':width})
   manifest.append({'source':str(path),'key':'museum-notes/etruscans/images/'+name,'size':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'content_type':'image/webp'})
  derived[key]={**c,'display_width':im.width,'display_height':im.height,'width':im.width,'height':im.height,'path':'originals/'+c['photo_id']+'.jpg','variants':variants}
 (DATA/'image-derivatives.json').write_text(json.dumps(derived,ensure_ascii=False,indent=2)+'\n')
 (DATA/'detail-crops.json').write_text(json.dumps({wid:derived[key] for wid,key in config['favorites'].items()},ensure_ascii=False,indent=2)+'\n')
 (out.parent/'editorial-upload-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(f'{len(derived)} crops; {len(manifest)} new versioned assets; {sum(x["size"] for x in manifest)/1e6:.2f} MB')
 return derived
if __name__=='__main__':prepare(sys.argv[1])
