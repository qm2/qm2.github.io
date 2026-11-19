"""Optional intake only; keep original photographs private and generate true-size previews."""
from pathlib import Path
from PIL import Image, ImageOps
import json,sys,shutil,hashlib
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'museum-notes/gusu-prints'
def prepare(pack):
    assets=json.loads((BASE/'data/assets.json').read_text()); out=BASE/'images';out.mkdir(exist_ok=True); manifest={}
    def emit(key,im,full=None):
        w,h=im.size; vs=[]
        for size in sorted(set([min(480,w),min(960,w),w])):
            name=f'{key}.webp' if size==w else f'{key}-{size}.webp';path=out/name
            if size==w and full:shutil.copyfile(full,path)
            else:im.resize((size,round(h*size/w)),Image.Resampling.LANCZOS).save(path,'WEBP',quality=88,method=6)
            vs.append({'path':f'images/{name}','width':size,'height':round(h*size/w)})
        manifest[key]={'width':w,'height':h,'full':vs[-1]['path'],'variants':vs}
    for a in assets:
        orig=pack/a['original_path'];assert hashlib.sha256(orig.read_bytes()).hexdigest()==a['source_sha256']
        im=Image.open(pack/a['web_path']).convert('RGB');assert im.size==(a['web_width'],a['web_height'])
        emit(a['id'],im,pack/a['web_path'])
    crops=[('g03',2956,.50,.53,.95),('g30',3067,.50,.43,.95),('g17',3021,.58,.44,.90),('g23',3034,.57,.43,.65),('g29',3060,.50,.53,.95)]
    for wid,n,cx,cy,fraction in crops:
        im=ImageOps.exif_transpose(Image.open(pack/f'assets/originals/p{n}.jpg')).convert('RGB');edge=round(min(im.size)*fraction)
        x=max(0,min(im.width-edge,round(im.width*cx-edge/2)));y=max(0,min(im.height-edge,round(im.height*cy-edge/2)))
        key='detail-'+wid;box=[x,y,x+edge,y+edge];emit(key,im.crop(box))
        manifest[key].update(source=f'p{n}',crop_box=box,role='首页局部导览；作品正文另保留完整图')
    (BASE/'data/derivatives.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(f'Gusu images: {len(assets)} original-photo derivatives + {len(crops)} explicit detail crops; originals untouched.')
if __name__=='__main__':prepare(Path(sys.argv[1]))
