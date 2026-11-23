"""Actual browser acceptance at desktop/tablet/mobile widths, including map and shared viewer."""
from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'museum-notes/pala-stone';BASE=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8774')+'/museum-notes/pala-stone/'
OUT=Path('/tmp/pala-browser');OUT.mkdir(exist_ok=True)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True);errors=[]
 for width in [1440,768,390]:
  page=browser.new_page(viewport={'width':width,'height':950});page.on('pageerror',lambda error:errors.append(str(error)))
  page.add_init_script("document.addEventListener('DOMContentLoaded',()=>{document.documentElement.style.scrollBehavior='auto'})")
  routes=['','atlas/','compare/','guide/','stories/','p3280/','p3308/','p3294/']
  if width==1440:routes=[str(f.parent.relative_to(B))+'/' for f in B.rglob('index.html')];routes=[''if s=='./'else s for s in routes]
  for slug in routes:
   r=page.goto(BASE+slug,wait_until='domcontentloaded');assert r.status==200,(slug,r.status)
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),(width,slug)
   if page.locator('main img').count():
    im=page.locator('main img').first;im.evaluate('(i)=>i.decode()');assert im.evaluate('(i)=>i.naturalWidth>0')
   if slug in ['','p3280/','p3308/']:
    page.screenshot(path=str(OUT/f'{slug.strip("/") or "home"}-{width}.png'))
  page.goto(BASE+'p3308/');page.locator('a[data-photo]').first.click();assert page.locator('#art-lightbox').is_visible();page.locator('#large-photo').evaluate('(i)=>i.decode()');page.locator('#zoom-toggle').click();assert page.locator('#zoom-toggle').get_attribute('aria-pressed')=='true';page.locator('#zoom-toggle').click();page.locator('#photo-next').click();assert '展签' in page.locator('#lightbox-caption').inner_text();page.keyboard.press('Escape');assert not page.locator('#art-lightbox').is_visible()
  page.locator('#record summary').click();page.locator('#record a[data-photo]').click();page.locator('#large-photo').evaluate('(i)=>i.decode()');page.keyboard.press('Escape')
  page.goto(BASE+'atlas/');page.wait_for_selector('[data-map-box]:not([hidden])');assert page.locator('[data-record-id]:visible').count()==24
  page.locator('#ps-search').fill('25.263');page.wait_for_function("document.querySelector('#ps-result-count').textContent.startsWith('当前1件')");assert page.locator('[data-record-id]:visible').count()==1
  page.locator('button[type=reset]').click();page.wait_for_function("document.querySelector('#ps-result-count').textContent.startsWith('当前24件')")
  page.locator('#ps-museum').select_option('mfah');assert page.locator('[data-record-id]:visible').count()==4
  page.locator('#ps-religion').select_option('印度教');assert page.locator('[data-record-id]:visible').count()==1
  page.go_back();assert page.locator('[data-record-id]:visible').count()==4;assert page.locator('#ps-religion').input_value()==''
  page.reload();assert page.locator('#ps-museum').input_value()=='mfah';page.wait_for_selector('[data-map-box]:not([hidden])')
  page.locator('button[type=reset]').click();page.wait_for_function("document.querySelector('#ps-result-count').textContent.startsWith('当前24件')")
  page.locator('#ps-sort').select_option('date');assert page.locator('[data-record-id]').first.get_attribute('data-record-id')=='p3288'
  page.locator('[data-map=hawaii]').click();assert page.locator('#ps-map [role=button]').count()==1;page.locator('#ps-map [role=button]').focus();page.keyboard.press('Enter');assert page.locator('#ps-museum').input_value()=='honolulu';assert page.locator('[data-record-id]:visible').count()==1
  page.locator('button[type=reset]').click();page.wait_for_function("document.querySelector('#ps-result-count').textContent.startsWith('当前24件')")
  page.locator('[data-map=mainland]').click();page.locator('[data-map-box]').scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'map-{width}.png'))
  # A grouped marker can be expanded by keyboard to resolve nearby museums.
  clusters=page.locator('#ps-map [data-cluster]:not([data-museum])')
  if clusters.count():clusters.first.focus();page.keyboard.press('Enter');assert page.locator('#ps-map [data-museum]').count()>=1
  page.goto(BASE+'sources/#O3308');page.wait_for_function("document.getElementById('O3308').open");assert page.locator('#O3308').is_visible()
  page.goto(BASE+'p3294/');im=page.locator('.ps-full img');im.evaluate('(i)=>i.decode()');box=im.bounding_box();cap=page.locator('.ps-full figcaption').bounding_box();assert abs(box['x']-cap['x'])<2 and abs(box['width']-cap['width'])<2;assert 0<=cap['y']-(box['y']+box['height'])<20
  print('PASS',width,'layouts, map/cluster, filter/back/reload, sort, original/label lightbox, captions and sources',flush=True);page.close()
 ctx=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844});page=ctx.new_page();page.goto(BASE+'atlas/');assert page.locator('[data-record-id]').count()==24;assert page.locator('.ps-museum-buttons a').count()==12;ctx.close()
 page=browser.new_page();page.route('**/ne_110m_land.geojson',lambda route:route.abort());page.goto(BASE+'atlas/');page.wait_for_selector('#ps-filters:not([hidden])');assert page.locator('[data-record-id]').count()==24;assert page.locator('.ps-museum-buttons a').count()==12;page.close()
 assert not errors,errors;browser.close();print('PASS fallback without JS/basemap; no browser exceptions.')
