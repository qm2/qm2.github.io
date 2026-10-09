"""Optional Playwright browser regression checks; run against a local static server.
Usage: python3 scripts/check_xiangtangshan_browser.py [http://127.0.0.1:8765/museum-notes/]
"""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
d=json.loads((ROOT/'museum-notes/xiangtangshan/data/works.json').read_text())
url=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8765/museum-notes/'
works=d['works'];cropped=[w for w in works if 'display_crop' in w]
def decode(locator):
 for im in locator.all():
  im.evaluate('(i)=>{i.loading="eager";return Promise.race([i.decode(),new Promise((_,r)=>setTimeout(()=>r(new Error(i.src)),10000))])}')
def crop_geometry(locator,crop):
 g=locator.evaluate('e=>{const a=e.getBoundingClientRect(),b=e.querySelector("img").getBoundingClientRect();return {x:(a.x-b.x)/b.width,y:(a.y-b.y)/b.height,width:a.width/b.width,height:a.height/b.height}}')
 assert all(abs(g[k]-crop[k])<.0002 for k in crop),(g,crop)
with sync_playwright() as pw:
 launch=dict(channel='chromium',ignore_default_args=['--disable-dev-shm-usage'],args=['--no-sandbox','--disable-gpu','--no-zygote','--single-process'])
 b=pw.chromium.launch(**launch);p=b.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
 for width in [360,1440]:
  p.set_viewport_size({'width':width,'height':1000})
  for route in ['xiangtangshan/','xiangtangshan/compare/']+['xiangtangshan/'+w['slug']+'/' for w in works]:
   p.goto(url+route,wait_until='domcontentloaded');decode(p.locator('img[src]'))
   assert p.evaluate('document.documentElement.scrollWidth<=innerWidth'),(route,width)
  p.goto(url+'xiangtangshan/');assert p.locator('.art-card').count()==25
  assert p.locator('#art-count').inner_text()=='25条记录（24件归属作品＋1件待考）'
  p.locator('.car-hero a[data-photo]').click();assert p.locator('#lightbox-caption').inner_text().startswith('1 / 1');p.keyboard.press('Escape')
  seen={}
  for w in cropped:
   card=p.locator('#'+w['slug']);decode(card.locator('img'));crop_geometry(card.locator('.xts-view'),w['display_crop'])
   opening=card.locator('a[data-photo]');opening.click();decode(p.locator('#large-photo'))
   assert p.locator('#xts-lightbox-view').get_attribute('data-work-id')==w['id']
   crop_geometry(p.locator('#xts-lightbox-view'),w['display_crop']);seen[w['id']]=p.locator('#xts-lightbox-view').get_attribute('data-crop')
   # Crop persists at zoom, and a full-view switch restores the whole source.
   p.locator('#zoom-toggle').click();crop_geometry(p.locator('#xts-lightbox-view'),w['display_crop'])
   p.locator('#xts-full').click();assert p.locator('#xts-lightbox-view').get_attribute('data-crop')=='null'
   crop_geometry(p.locator('#xts-lightbox-view'),dict(x=0,y=0,width=1,height=1))
   p.locator('#xts-full').click();crop_geometry(p.locator('#xts-lightbox-view'),w['display_crop'])
   p.keyboard.press('ArrowRight');assert p.locator('#xts-lightbox-view').get_attribute('data-crop')=='null'
   p.keyboard.press('ArrowLeft');crop_geometry(p.locator('#xts-lightbox-view'),w['display_crop'])
   p.keyboard.press('Escape');assert opening.evaluate('(e)=>document.activeElement===e')
  assert seen['FSG-F1977.8']!=seen['FSG-F1953.86']
  assert len({seen[k] for k in ('PEN-C113','PEN-C151','PEN-C150')})==3
  for w in cropped:
   p.goto(url+'xiangtangshan/'+w['slug']+'/');decode(p.locator('.work-photo img'));crop_geometry(p.locator('.work-photo .xts-view'),w['display_crop'])
   p.locator('.work-photo>a[data-photo]').click();crop_geometry(p.locator('#xts-lightbox-view'),w['display_crop']);p.keyboard.press('Escape')
   p.locator('.xts-full-link a').click();assert p.locator('#xts-lightbox-view').get_attribute('data-crop')=='null';p.keyboard.press('Escape')
   assert p.locator('#context-photos img[src$="/'+str(w['hero'])+'.jpg"]').count()==1
   p.locator('.xts-labels summary').click();p.locator('.xts-labels a[data-photo]').first.click();assert ':label:' in p.locator('#xts-lightbox-view').get_attribute('data-view-id');p.keyboard.press('Escape')
  p.goto(url+'xiangtangshan/compare/');assert p.locator('#guardians>.comparison-grid>.comparison-work').count()==6
  assert p.locator('#guardians>.comparison-grid .xts-view').count()==4
  assert p.locator('#guardians .xts-context img').count()==2
  assert p.locator('#cave-two img[src$="/739.jpg"]').count()==1
  assert p.locator('#cave-two .xts-wide').count()==2
  assert p.locator('#faces .record-note').is_visible()
  print('PASS at',width,'px: 27 pages, 8 crop geometries, lightbox zoom/full/keyboard/focus, comparison groups',flush=True)
 p.goto(url+'xiangtangshan/')
 for query in ['C113','F1977.8','大势至']:
  p.locator('#art-search').fill(query);assert p.locator('.art-card:visible').count()==1;assert not p.locator('#art-empty').is_visible()
 p.locator('#art-reset').click();p.select_option('#art-museum','PEN');assert p.locator('.art-card:visible').count()==3
 p.select_option('#art-subject','NN');assert p.locator('#art-empty').is_visible();assert p.locator('.art-card:visible').count()==0
 p.locator('#art-reset').click();p.select_option('#art-subject','NN');assert p.locator('.art-card:visible').count()==8
 p.select_option('#art-museum','FSG');assert p.locator('.art-card:visible').count()==5
 p.locator('#art-search').fill('F1977.8');assert p.locator('.art-card:visible').count()==1
 p.locator('#art-search').fill('not-found');assert p.locator('#art-empty').is_visible()
 p.locator('#art-reset').click();assert p.locator('.art-card:visible').count()==25;assert not p.locator('#art-empty').is_visible()
 p.locator('#gallery-mode').click();assert p.locator('#gallery-mode').get_attribute('aria-pressed')=='true'
 # The original shared gallery remains untouched and still has working dialogs.
 for topic in ['caravaggio','leonardo','vermeer','monet-water-lilies','al-jazari']:
  p.goto(url+topic+'/');opening=p.locator('a[data-photo]').first;opening.click();assert p.locator('#art-lightbox').is_visible();p.keyboard.press('Escape')
 assert not errors,errors;b.close()
 b=pw.chromium.launch(**launch);ctx=b.new_context(java_script_enabled=False);p=ctx.new_page();p.goto(url+'xiangtangshan/');assert p.locator('.art-card:visible').count()==25;assert not p.locator('.art-controls').is_visible()
 p.goto(url+'xiangtangshan/pen-c113/');decode(p.locator('.work-photo img'));crop_geometry(p.locator('.xts-view').first,next(w['display_crop'] for w in works if w['id']=='PEN-C113'));b.close()
print('PASS: search, filters, empty/reset, gallery mode, other galleries, no-JavaScript crop rendering; no JS errors')
