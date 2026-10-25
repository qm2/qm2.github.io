"""Preserve the 115 supplied originals and generate uncropped WebP derivatives.
Run only for image intake, not during the ordinary site build.
"""
from pathlib import Path
import argparse,csv,hashlib,json,shutil
from PIL import Image,ImageOps
ROOT=Path(__file__).resolve().parents[1]
def main():
 parser=argparse.ArgumentParser();parser.add_argument('photos',type=Path);parser.add_argument('handoff',type=Path);a=parser.parse_args()
 base=ROOT/'museum-notes/xuzhou';dest=base/'images';(dest/'originals').mkdir(parents=True,exist_ok=True)
 rows=list(csv.DictReader((a.handoff/'photos.csv').open(encoding='utf-8-sig')))
 rows.append({'photo_number':'SUPP01','filename':'30544ed57d589d64d994729d28a64807.jpg','object_id':'X28','role':'补充独立展签'})
 photos={}
 for r in rows:
  n=r['photo_number'];src=(a.handoff/'supplement' if n=='SUPP01' else a.photos)/r['filename'];raw=src.read_bytes();sha=hashlib.sha256(raw).hexdigest();target=dest/'originals'/src.name
  if target.exists():assert hashlib.sha256(target.read_bytes()).hexdigest()==sha, f'Original collision: {n}'
  else:shutil.copy2(src,target)
  im=ImageOps.exif_transpose(Image.open(src)).convert('RGB');w,h=im.size
  variants=[]
  for width in [480,960]:
   width=min(width,w);out=dest/f'{n}-{width}.webp';im.resize((width,round(h*width/w)),Image.Resampling.LANCZOS).save(out,'WEBP',quality=85,method=6)
   variants.append({'file':out.name,'width':width,'height':round(h*width/w)})
  photos[n]={'number':n,'original_filename':src.name,'original':f'originals/{src.name}','sha256':sha,'bytes':len(raw),'width':w,'height':h,'rotation':0,'variants':variants,'object_id':r['object_id'].lower(),'role':r['role']}
 (base/'data/photos.json').write_text(json.dumps(photos,ensure_ascii=False,indent=2)+'\n')
 (base/'data/intake.json').write_text(json.dumps({'reviewed':'2026-10-25','total':len(photos),'missing_originals':[],'manifest':'photos.json','original_policy':'Byte-identical originals; uncropped resized WebP derivatives. No generative edits.','source_directory':str(a.photos),'supplement':str(a.handoff/'supplement'),'all_label_originals_reviewed':True,'main_photo_mapping_reviewed':True,'book_pages_available':False},ensure_ascii=False,indent=2)+'\n')
 print(f'Preserved {len(photos)} originals, generated {len(photos)*2} WebP derivatives.')
if __name__=='__main__':main()
