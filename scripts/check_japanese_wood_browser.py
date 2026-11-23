"""Browser acceptance for notebook, map, dates, source anchors and photo viewer."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'museum-notes/japanese-buddhist-sculpture';BASE=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8774')+'/museum-notes/japanese-buddhist-sculpture/'
OUT=Path('/tmp/japanese-wood');OUT.mkdir(exist_ok=True)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True);errors=[]
 for width in [1440,768,390]:
  page=browser.new_page(viewport={'width':width,'height':1000});page.on('pageerror',lambda error:errors.append(str(error)))
  page.add_init_script("document.addEventListener('DOMContentLoaded',()=>{document.documentElement.style.scrollBehavior='auto'})")
  routes=['','atlas/','compare/','guide/','j12/','j19/','j23/','j40/','j41/','j58/','j59/','j62/']
  if width==1440:routes=[str(f.parent.relative_to(B))+'/' for f in B.rglob('index.html')];routes=[''if s=='./'else s for s in routes]
  for slug in routes:
   r=page.goto(BASE+slug,wait_until='domcontentloaded');assert r.status==200,(slug,r.status)
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),(width,slug)
   if slug in ['','j23/','j40/','j58/']:
    first=page.locator('main img').first;first.scroll_into_view_if_needed();first.evaluate('(img)=>img.decode()');assert first.evaluate('(img)=>img.naturalWidth>0')
    page.screenshot(path=str(OUT/f'final-{slug.strip("/") or "home"}-{width}.png'))
  page.goto(BASE+'j23/');a=page.locator('a[data-photo]').first;a.click();assert page.locator('#art-lightbox').is_visible();page.locator('#large-photo').evaluate('(i)=>i.decode()');page.locator('#zoom-toggle').click();assert page.locator('#zoom-toggle').get_attribute('aria-pressed')=='true';page.locator('#zoom-toggle').click();page.locator('#photo-next').click();assert '衣纹' in page.locator('#lightbox-caption').inner_text();page.keyboard.press('Escape');assert not page.locator('#art-lightbox').is_visible()
  page.locator('#label summary').click();page.locator('#label a[data-photo]').first.click();page.locator('#large-photo').evaluate('(i)=>i.decode()');assert '展签' in page.locator('#lightbox-caption').inner_text();page.keyboard.press('Escape')
  page.goto(BASE+'atlas/');page.wait_for_selector('#jw-map-box:not([hidden])');assert page.locator('#jw-count').inner_text().startswith('62 /')
  page.locator('#jw-search').fill('1960.197');assert page.locator('#jw-count').inner_text().startswith('1 /');assert page.locator('[data-record-id]:visible').count()==1;assert page.locator('.jw-time-row:visible').count()==1
  page.locator('button[type=reset]').click();page.wait_for_function("document.querySelector('#jw-count').textContent.startsWith('62 /')")
  page.locator('#jw-reading').select_option('personal');assert page.locator('[data-record-id]:visible').count()==16
  page.locator('#jw-reading').select_option('essay');assert page.locator('[data-record-id]:visible').count()==25
  page.go_back();assert page.locator('#jw-reading').input_value()=='personal';assert page.locator('[data-record-id]:visible').count()==16
  page.locator('button[type=reset]').click();page.wait_for_function("document.querySelector('#jw-count').textContent.startsWith('62 /')")
  page.locator('#jw-museum').select_option('MFAH');assert page.locator('[data-record-id]:visible').count()==4;assert page.locator('#museum-MFAH').get_attribute('open') is not None
  page.locator('button[type=reset]').click();page.wait_for_function("document.querySelector('#jw-count').textContent.startsWith('62 /')")
  page.locator('[data-map=paris]').click();assert page.locator('#jw-map [role=button]').count()==2
  page.locator('#jw-map [role=button]').first.focus();page.keyboard.press('Enter');assert page.locator('#jw-museum').input_value() in ['GUIMET','CERNUSCHI']
  page.locator('button[type=reset]').click();page.wait_for_function("document.querySelector('#jw-count').textContent.startsWith('62 /')")
  page.locator('[data-map=hawaii]').click();assert '檀香山' in page.locator('#jw-map [role=button]').first.get_attribute('aria-label')
  page.locator('[data-map=all]').click();page.locator('#jw-map-box').evaluate('(e)=>e.scrollIntoView({block:"start",behavior:"instant"})');page.screenshot(path=str(OUT/f'final-map-{width}.png'))
  page.locator('#jw-context-map').evaluate('(e)=>e.scrollIntoView({block:"start",behavior:"instant"})');page.screenshot(path=str(OUT/f'final-context-{width}.png'))
  page.goto(BASE+'sources/#S-CMA-AMIDA');assert page.locator('#S-CMA-AMIDA').get_attribute('open') is not None
  print('PASS',width,'layout, navigation, photo viewer, labels, filters, history, Paris/Hawaii map, source anchors',flush=True);page.close()
 # No script and deliberate map-data failure both retain every record.
 ctx=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844});page=ctx.new_page();page.goto(BASE+'atlas/');assert page.locator('[data-record-id]').count()==62;page.locator('#museum-MFAH summary').click();assert page.locator('#museum-MFAH a.jw-card').count()==4;ctx.close()
 page=browser.new_page();page.route('**/ne_110m_land.geojson',lambda route:route.abort());page.goto(BASE+'atlas/');page.wait_for_selector('#jw-filters:not([hidden])');assert page.locator('[data-record-id]').count()==62;assert page.locator('.jw-museums details').count()==15;page.close()
 assert not errors,errors;browser.close();print('PASS no-JS / failed basemap fallback; no browser errors.')
