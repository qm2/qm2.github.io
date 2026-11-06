"""Exercise the actual atlas in Chromium, including every public photo and label."""
import functools,http.server,threading,json
from pathlib import Path
from playwright.sync_api import sync_playwright,expect

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'museum-notes/images-and-vows/atlas'
data=json.loads((BASE/'catalogue.json').read_text())
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
 def copyfile(self,*args):
  try:super().copyfile(*args)
  except (BrokenPipeError,ConnectionResetError):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/museum-notes/images-and-vows/atlas/'
errors=[];bad=[]
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,args=['--no-sandbox'])
 page=browser.new_page()
 page.on('pageerror',lambda err:errors.append(str(err)))
 page.on('response',lambda r:bad.append((r.status,r.url)) if r.status>=400 and r.url.startswith('http://127.0.0.1') else None)
 def overflow():assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),page.url
 def decode(im):
  im.scroll_into_view_if_needed()
  im.evaluate('(im)=>Promise.race([im.decode(),new Promise((_,r)=>setTimeout(()=>r(new Error(im.src)),12000))])')
 def photo(im):
  decode(im);box=im.bounding_box();cap=im.locator('xpath=ancestor::figure').locator('figcaption').bounding_box()
  assert abs(box['x']-cap['x'])<2 and abs(box['width']-cap['width'])<2,(box,cap)
  assert 0<=cap['y']-box['y']-box['height']<15,(box,cap)
  assert abs(box['width']/box['height']-im.evaluate('(im)=>im.naturalWidth/im.naturalHeight'))<.015
 def lightbox(a):
  a.click();expect(page.locator('#art-lightbox')).to_be_visible();page.locator('#large-photo').evaluate('(im)=>im.decode()')
  page.locator('#zoom-toggle').click();expect(page.locator('#zoom-toggle')).to_have_attribute('aria-pressed','true')
  page.keyboard.press('Escape');expect(page.locator('#art-lightbox')).not_to_be_visible();expect(a).to_be_focused()
 for width in [1440,390,320]:
  print('Atlas viewport',width,flush=True)
  page.set_viewport_size({'width':width,'height':900});page.goto(url);expect(page.locator('.va-card:visible')).to_have_count(len(data['works']));overflow()
  page.screenshot(path=f'/tmp/vows-atlas-home-{width}.png')
  assert page.locator('.va-object>summary').first.evaluate('(el)=>getComputedStyle(el).display')=='block'
  page.locator('#map-canvas').scroll_into_view_if_needed();page.screenshot(path=f'/tmp/vows-atlas-map-{width}.png')
  for mode in ['america','asia','europe','world']:
   page.locator(f'[data-map-view="{mode}"]').click();expect(page.locator(f'[data-map-view="{mode}"]')).to_have_attribute('aria-pressed','true');overflow()
  page.locator('.va-map-key [data-map-museum="noma"]').click();expect(page.locator('#museum-noma')).to_have_attribute('open','')
  page.locator('#museum-noma .va-miniatures a').click();expect(page.locator('#work-mfa-1843>.va-object')).to_have_attribute('open','');photo(page.locator('#work-mfa-1843 .va-slides img:visible'))
  for field,value in [('museum_id','penn'),('period','北齐'),('region','南方／成都'),('form_group','造像碑'),('material_group','石雕')]:
   page.goto(url);page.locator(f'[name="{field}"]').select_option(value)
   expected=sum(w[field]==value for w in data['works']);expect(page.locator('.va-card:visible')).to_have_count(expected)
   expect(page.locator('.va-time-card')).to_have_count(expected)
   page.reload();expect(page.locator('.va-card:visible')).to_have_count(expected)
   page.locator('#filters button[type=reset]').click();expect(page.locator('.va-card:visible')).to_have_count(len(data['works']))
   page.go_back();expect(page.locator('.va-card:visible')).to_have_count(expected)
  page.goto(url);page.locator('[name=q]').fill('C404');expect(page.locator('.va-card:visible')).to_have_count(1)
  page.locator('[name=q]').fill('不存在的题名');expect(page.locator('#empty')).to_be_visible()
  page.locator('#filters button[type=reset]').click();expect(page.locator('.va-card:visible')).to_have_count(len(data['works']))
  page.locator('[name=sort]').select_option('year-desc')
  assert page.locator('.va-card:visible').first.get_attribute('data-work')==max(data['works'],key=lambda w:w['year_start'])['id']
  page.goto(url+'#timeline');overflow();page.screenshot(path=f'/tmp/vows-atlas-timeline-{width}.png')
  collisions=page.locator('.va-track').evaluate_all('els=>els.flatMap(el=>{const boxes=[...el.querySelectorAll(".va-time-card")].map(x=>x.getBoundingClientRect());return boxes.flatMap((a,i)=>boxes.slice(i+1).filter(b=>Math.min(a.right,b.right)-Math.max(a.left,b.left)>1&&Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top)>1))}).length')
  assert collisions==0,collisions
  for id in ['na-494-yin','mfah-526-faxing']:page.locator(f'[data-compare="{id}"]').check()
  page.locator('#compare-jump').click();expect(page.locator('[data-compare-work]')).to_have_count(2)
  for im in page.locator('#compare-pair img').all():photo(im)
  page.locator('[data-compare-view="na-494-yin"]').select_option(index=1);lightbox(page.locator('[data-compare-work="na-494-yin"] a[data-photo]'))
  page.screenshot(path=f'/tmp/vows-atlas-compare-{width}.png');overflow()
  page.locator('#compare-clear').click();expect(page.locator('[data-compare-work]')).to_have_count(0)
  page.goto(url+'?museum_id=penn#work-mfa-1843');expect(page.locator('#work-mfa-1843>.va-object')).to_have_attribute('open','');expect(page.locator('.va-card:visible')).to_have_count(len(data['works']))
  page.goto(url+'#work-museum-1848');g=page.locator('#work-museum-1848 .va-gallery')
  for tab in g.locator('[data-view]').all():
   tab.press('Enter');photo(g.locator('.va-photo:visible img'));lightbox(g.locator('.va-photo:visible a[data-photo]'));overflow()
  g.locator('[data-all]').click();expect(g.locator('.va-photo:visible')).to_have_count(5)
  for im in g.locator('.va-photo img').all():photo(im)
  g.locator('[data-all]').click();expect(g.locator('.va-photo:visible')).to_have_count(1)
  assert page.locator('.va-object[open]>summary span').evaluate_all('els=>els.every(el=>getComputedStyle(el).transform==="none")')
  page.goto(url+'#work-mfa-1843');page.locator('#work-mfa-1843 .va-slides img').scroll_into_view_if_needed();page.screenshot(path=f'/tmp/vows-atlas-detail-{width}.png')
  page.goto(url+'#catalogue');page.screenshot(path=f'/tmp/vows-atlas-catalogue-{width}.png')
 # Every object, original view and label at phone width.
 page.set_viewport_size({'width':390,'height':844})
 for w in data['works']:
  print('Photo audit',w['id'],flush=True);page.goto(url+'#work-'+w['id']);card=page.locator('#work-'+w['id']);g=card.locator('.va-gallery')
  if g.locator('.va-photo').count()>1:g.locator('[data-all]').click()
  card.locator('.va-labels>summary').click()
  for im in card.locator('.va-photo:visible img').all():photo(im)
  for a in card.locator('.va-labels a[data-photo]').all():lightbox(a)
  overflow()
 # Keyboard operation, deep reading link, entrance, and no-JS catalogue.
 page.goto(url+'#work-penn-551-c404');page.locator('#work-penn-551-c404>.va-object>summary').press('Enter');expect(page.locator('#work-penn-551-c404>.va-object')).not_to_have_attribute('open','')
 page.goto(url+'#work-mfah-526-faxing');page.locator('#work-mfah-526-faxing .va-reading').click();assert page.url.endswith('/faxing-526/')
 page.goto(url+'../');page.locator('a[href="atlas/"]').first.click();expect(page.locator('h1')).to_have_text('所见造像')
 plain=browser.new_page(java_script_enabled=False,viewport={'width':390,'height':844});plain.goto(url)
 expect(plain.locator('.va-card')).to_have_count(len(data['works']));plain.locator('#work-museum-1848>.va-object>summary').click();expect(plain.locator('#work-museum-1848 .va-slides img:visible')).to_have_count(5)
 assert not errors,errors
 assert not bad,bad
 browser.close()
server.shutdown()
print('PASS: desktop 1440 / mobile 390, 320; maps, linked filters, history, timeline non-overlap, compare views, all 103 photos, labels, natural proportions/captions, lightbox, anchors and no-JS catalogue.')
