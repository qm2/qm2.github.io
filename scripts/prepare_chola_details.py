"""Small honest crops from the author's originals; never enlarge or alter colour."""
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import hashlib,json,sys
BASE=Path(__file__).resolve().parents[1]/'museum-notes/chola-bronzes'
SPECS=[
 ('dance-face','c03',3316,[.24,.16,.76,.51],1,'面容与横过胸前的手臂：剧烈舞姿中保留安定'),
 ('saint-cymbals','c10',3332,[.19,.05,.78,.52],1,'面容、肋骨与手中小钹：身体衰瘦，伴奏的动作仍在'),
 ('half-body','c17',3346,[.27,.22,.65,.77],0,'冠饰、胸部与衣裙：左右两侧呈现不同身体特征'),
 ('hanuman-hand-v2','c23',3358,[.18,.015,.82,.61],0,'靠近嘴边的手与前倾肩膀：英雄主动收起力量'),
 ('uma-face-v2','c27',3366,[.25,.015,.77,.55],0,'从高冠、面容到缓缓下垂的肩线'),
 ('sambandar-v2','c28',3368,[.025,.12,.995,.68],0,'指向上方的手与展开的另一臂：赞歌成为舞姿')]
def prepare(pack,out):
 paths={int(p.name.split('_')[-2]):p for p in pack.rglob('Image_*.jpg')};ds=[];manifest=json.loads((out/'upload-manifest.json').read_text());manifest=[r for r in manifest if '/details/' not in r['key']]
 board=Image.new('RGB',(1200,800),'#eee8de');draw=ImageDraw.Draw(board)
 for i,(id,work,n,box,after,caption) in enumerate(SPECS):
  im=ImageOps.exif_transpose(Image.open(paths[n])).convert('RGB');w,h=im.size;b=tuple(round(v*(w if j%2==0 else h)) for j,v in enumerate(box));im=im.crop(b);w,h=im.size;vs=[]
  for width in sorted({min(w,x) for x in [360,900]}):
   dest=out/'images/details'/f'{id}-{width}.webp';dest.parent.mkdir(exist_ok=True,parents=True);height=round(h*width/w);im.resize((width,height),Image.Resampling.LANCZOS).save(dest,'WEBP',quality=89,method=4);key='museum-notes/chola-bronzes/'+dest.relative_to(out).as_posix()
   vs.append(dict(url='https://images.mertonmuseum.com/'+key,width=width,height=height));manifest.append(dict(source=str(dest),key=key,size=dest.stat().st_size,sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),content_type='image/webp'))
  ds.append(dict(id=id,work=work,photo=n,box_pixels=list(b),after_section=after,caption=caption,width=w,height=h,variants=vs))
  im.thumbnail((380,350));x=i%3*400;y=i//3*400;board.paste(im,(x+(380-im.width)//2,y+28));draw.text((x+10,y+6),id,fill='black')
 (BASE/'data/details.json').write_text(json.dumps(ds,ensure_ascii=False,indent=2)+'\n');(out/'upload-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');board.save('/tmp/chola-detail-review.jpg');print(len(ds),'crops; no upscaling')
if __name__=='__main__':prepare(Path(sys.argv[1]),Path(sys.argv[2]))
