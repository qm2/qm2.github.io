"""Exercise the published components at desktop, tablet and phone widths."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
ROOT=Path(__file__).resolve().parents[1];TOPIC=ROOT/'museum-notes/khmer-art'
ORIGIN=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8774').rstrip('/')
BASE=ORIGIN+'/museum-notes/khmer-art/';OUT=Path('/tmp/khmer-review');OUT.mkdir(exist_ok=True)
works=json.loads((TOPIC/'data/objects.json').read_text());total=len(works)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True);errors=[]
 for width in [1440,768,390]:
  page=browser.new_page(viewport={'width':width,'height':950},device_scale_factor=1)
  page.on('pageerror',lambda err:errors.append(str(err)))
  page.add_init_script("document.addEventListener('DOMContentLoaded',()=>document.documentElement.style.scrollBehavior='auto')")
  routes=['','west-mebon/','krishna/','guimet/','enthroned-buddha/','early-bronzes/','buddhist-images/','guide/','K03/','C09/','C10/','C11/','O06/','atlas/','catalogue/','sources/']
  if width==1440:routes=['' if f.parent==TOPIC else str(f.parent.relative_to(TOPIC))+'/' for f in TOPIC.rglob('index.html')]
  for slug in routes:
   r=page.goto(BASE+slug,wait_until='domcontentloaded');assert r.status==200,(slug,r.status)
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),(width,slug,'overflow')
   first=page.locator('main img:visible').first
   if first.count():first.evaluate('(i)=>i.decode()');assert first.evaluate('(i)=>i.naturalWidth>0')
   if slug in ['', 'K03/','west-mebon/','enthroned-buddha/','krishna/']:page.screenshot(path=str(OUT/f'{slug.strip("/") or "home"}-{width}.png'))
  page.goto(BASE);page.locator('.ka-routes').scroll_into_view_if_needed();page.locator('.ka-routes img').evaluate_all('(a)=>Promise.all(a.map(i=>i.decode()))');page.screenshot(path=str(OUT/f'five-{width}.png'))
  page.locator('.ka-route').first.click();assert page.url.endswith('/west-mebon/')
  page.goto(BASE+'K03/')
  image=page.locator('.ka-figure img').first;image.evaluate('(i)=>i.decode()');box=image.bounding_box();cap=page.locator('.ka-figure figcaption').first.bounding_box()
  assert abs(box['x']-cap['x'])<2 and abs(box['width']-cap['width'])<2,(box,cap)
  assert 0<=cap['y']-box['y']-box['height']<20
  assert image.evaluate('(i)=>Math.abs(i.width/i.height-i.naturalWidth/i.naturalHeight)<.01')
  page.locator('a[data-photo]').first.click();assert page.locator('#art-lightbox').is_visible();page.locator('#large-photo').evaluate('(i)=>i.decode()')
  assert 'd1162d7376874af2bf11cee843a4c5c7.jpg' in page.locator('#large-photo').get_attribute('src')
  page.locator('#zoom-toggle').click();assert page.locator('#zoom-toggle').get_attribute('aria-pressed')=='true';page.keyboard.press('Escape');assert not page.locator('#art-lightbox').is_visible()
  page.locator('#labels summary').click();page.locator('#labels img').evaluate('(i)=>i.decode()');page.locator('#labels a[data-photo]').click();page.locator('#large-photo').evaluate('(i)=>i.decode()');assert 'b813a861' in page.locator('#large-photo').get_attribute('src');page.keyboard.press('Escape')
  page.goto(BASE+'atlas/');page.wait_for_selector('#ka-filters:not([hidden])');page.wait_for_selector('#ka-map .ka-marker')
  assert page.locator('[data-record]:visible').count()==total
  page.locator('#ka-museum').select_option('kimbell');assert page.locator('[data-record]:visible').count()==3
  assert page.locator('[data-record=K03]').is_visible()
  page.locator('#ka-map').scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'kimbell-map-{width}.png'))
  page.locator('#ka-q').fill('AP 1988.01');assert page.locator('[data-record]:visible').count()==1
  page.locator('.ka-more-filters summary').click();page.locator('#ka-kind').select_option('historic_cast');assert page.locator('[data-record]:visible').count()==0
  page.go_back();assert page.locator('[data-record]:visible').count()==1
  page.reload();page.wait_for_selector('#ka-filters:not([hidden])');assert page.locator('[data-record]:visible').count()==1
  page.locator('button[type=reset]').click();page.wait_for_function(f'document.querySelector("#ka-count").textContent=="{total} / {total}条记录"')
  if not page.locator('.ka-more-filters').evaluate('(d)=>d.open'):page.locator('.ka-more-filters summary').click()
  page.locator('#ka-kind').select_option('historic_cast');assert page.locator('[data-record]:visible').count()==3
  page.locator('#ka-kind').select_option('label_only');assert page.locator('[data-record]:visible').count()==1
  page.locator('#ka-kind').select_option('pending');assert page.locator('[data-record]:visible').count()==1
  page.locator('button[type=reset]').click();page.wait_for_function(f'document.querySelector("#ka-count").textContent=="{total} / {total}条记录"')
  page.locator('[data-view=origins]').click();page.wait_for_selector('#ka-map .ka-marker');assert page.locator('#ka-map-legend').is_visible()
  page.locator('#ka-map').scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'origins-{width}.png'))
  page.locator('#ka-map .ka-marker').first.focus();page.keyboard.press('Enter');assert page.locator('#ka-map .ka-marker').count()>0
  page.get_by_text('原址、区域与关联地点',exact=True).click();page.locator('[data-site]').first.click();assert 'site=' in page.url and page.locator('#ka-clear-site').is_visible()
  assert page.locator('[data-record]:visible').count()>0
  page.locator('#ka-clear-site').click();assert page.locator('[data-record]:visible').count()==total
  page.goto(BASE+'atlas/?museum=guimet#map');page.wait_for_selector('#ka-map .ka-marker');assert page.locator('[data-region=paris]').get_attribute('aria-pressed')=='true'
  page.goto(BASE+'atlas/?q=K03#timeline');page.wait_for_selector('#ka-filters:not([hidden])');assert page.locator('[data-time-record]:visible').count()==1
  page.locator('#timeline').scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'timeline-{width}.png'))
  page.goto(BASE+'sources/#Pk03-label');page.wait_for_function("document.getElementById('Pk03-label').open");page.locator('#Pk03-label img').evaluate('(i)=>i.decode()');assert page.locator('#Pk03-label img').is_visible()
  for slug in ['krishna','early-bronzes','enthroned-buddha','guimet','K03']:
   page.goto(BASE+slug+'/');detail=page.locator('.ka-detail').first;detail.scroll_into_view_if_needed();detail.locator('img').evaluate('(i)=>i.decode()')
   assert detail.locator('img').evaluate("(i)=>i.width<=Number(i.getAttribute('width'))+1")
   detail.locator('a[data-photo]').first.click();page.locator('#large-photo').evaluate('(i)=>i.decode()');assert '/detail-' in page.locator('#large-photo').get_attribute('src');page.keyboard.press('Escape')
   detail.locator('figcaption a[data-photo]').click();page.locator('#large-photo').evaluate('(i)=>i.decode()');assert '/originals/' in page.locator('#large-photo').get_attribute('src');page.keyboard.press('Escape')
  page.goto(BASE+'atlas/?view=origins&region=angkor#map');page.wait_for_selector('.ka-marker')
  for name in ['西梅奔与西池','吴哥窟','巴戎寺','圣剑寺']:assert name in page.locator('.ka-map-label').all_text_contents()
  assert page.locator('.ka-marker').count()==4
  page.locator('.ka-marker').first.focus();page.keyboard.press('Enter');assert 'site=' in page.url;page.go_back();assert 'site=' not in page.url
  page.goto(BASE+'krishna/');page.get_by_role('link',name='在地图中看相关地点与作品').click();page.wait_for_selector('.ka-marker');assert 'site=phnom-da' in page.url and page.locator('[data-record=C02]').is_visible()
  page.goto(BASE+'catalogue/');page.wait_for_selector('#ka-filters:not([hidden])');assert page.locator('[data-record]').first.bounding_box()['y']<950
  print('PASS',width,'layout, full frames, captions, viewer, navigation, filters, map, URL history, source anchors',flush=True);page.close()
 ctx=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844});page=ctx.new_page();page.goto(BASE+'atlas/');assert page.locator('[data-record]').count()==total and page.locator('[data-museum]').count()==11;ctx.close()
 page=browser.new_page();page.route('**/ne_110m_land.geojson',lambda r:r.abort());page.goto(BASE+'atlas/');page.wait_for_selector('#ka-filters:not([hidden])');assert page.locator('[data-record]').count()==total;page.close()
 assert not errors,errors
 browser.close();print('PASS: no browser errors; no-JS and offline map fallbacks.')
