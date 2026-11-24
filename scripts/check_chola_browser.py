"""Real desktop/tablet/phone checks of navigation, images and map enhancement."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import sys
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'museum-notes/chola-bronzes'
BASE=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8765')+'/museum-notes/chola-bronzes/'
OUT=Path('/tmp/chola-browser');OUT.mkdir(exist_ok=True)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True);errors=[]
 for width in [1440,768,390]:
  page=browser.new_page(viewport={'width':width,'height':950});page.on('pageerror',lambda error:errors.append(str(error)))
  page.add_init_script("document.addEventListener('DOMContentLoaded',()=>{document.documentElement.style.scrollBehavior='auto'})")
  page.goto(BASE.replace('chola-bronzes/','south-asian-art/'))
  assert page.locator('.notebook-index > .issue-link').count()==4
  for sel in ['', ' > img', ' > div']:
   boxes=[el.bounding_box() for el in page.locator('.notebook-index > .issue-link'+sel).all()]
   assert max(v['x'] for v in boxes)-min(v['x'] for v in boxes)<1
   assert max(v['width'] for v in boxes)-min(v['width'] for v in boxes)<1
  routes=['','atlas/','guide/','compare/','stories/','c20/','c27/','c10/','c23/','c29/','c33/','c37/','c38/']
  if width==1440:routes=['' if f.parent==B else str(f.parent.relative_to(B))+'/' for f in B.rglob('index.html')]
  for slug in routes:
   response=page.goto(BASE+slug,wait_until='domcontentloaded');assert response.status==200
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),(width,slug)
   image=page.locator('main img').first
   if image.count():image.evaluate('(i)=>i.decode()');assert image.evaluate('(i)=>i.naturalWidth>0')
   if slug in ['','c20/','c23/','c27/','c37/','c38/']:page.screenshot(path=str(OUT/f'{slug.strip("/") or "home"}-{width}.png'))
  page.goto(BASE+'c37/');im=page.locator('.cb-full img');im.evaluate('(i)=>i.decode()');assert im.bounding_box()['width']<=164
  page.locator('.cb-full a[data-photo]').click();page.locator('#large-photo').evaluate('(i)=>i.decode()');assert 'noma_three_buddhas_case.jpg' in page.locator('#large-photo').get_attribute('src');page.keyboard.press('Escape')
  page.locator('#record summary').click();page.locator('#record img').evaluate('(i)=>i.decode()');page.locator('#record a[data-photo]').click();page.locator('#large-photo').evaluate('(i)=>i.decode()');page.keyboard.press('Escape')
  page.goto(BASE+'guide/#buddhist-port');page.wait_for_timeout(400);page.screenshot(path=str(OUT/f'buddhist-port-{width}.png'))
  page.goto(BASE);page.locator('.cb-picks').scroll_into_view_if_needed();page.locator('.cb-picks img').evaluate_all('(imgs)=>Promise.all(imgs.map(i=>i.decode()))');page.screenshot(path=str(OUT/f'five-{width}.png'));page.locator('.cb-picks a').first.click();assert page.url.endswith('/c20/')
  page.locator('a[data-photo]').first.click();assert page.locator('#art-lightbox').is_visible();page.locator('#large-photo').evaluate('(i)=>i.decode()');page.locator('#zoom-toggle').click();assert page.locator('#zoom-toggle').get_attribute('aria-pressed')=='true';page.locator('#zoom-toggle').click();page.locator('#photo-next').click();page.locator('#large-photo').evaluate('(i)=>i.decode()');page.keyboard.press('Escape');assert not page.locator('#art-lightbox').is_visible()
  page.locator('#record summary').click();page.locator('#record a[data-photo]').click();page.locator('#large-photo').evaluate('(i)=>i.decode()');page.keyboard.press('Escape')
  page.goto(BASE+'c23/');im=page.locator('.cb-full img');im.evaluate('(i)=>i.decode()');box=im.bounding_box();cap=page.locator('.cb-full figcaption').bounding_box();assert abs(box['x']-cap['x'])<2 and abs(box['width']-cap['width'])<2 and 0<=cap['y']-box['y']-box['height']<20
  page.locator('.cb-detail a').first.click();page.locator('#large-photo').evaluate('(i)=>i.decode()');assert '局部' in page.locator('#lightbox-caption').inner_text();page.keyboard.press('Escape')
  page.goto(BASE+'atlas/');page.wait_for_selector('[data-map-box]:not([hidden])');assert page.locator('[data-record-id]:visible').count()==38
  page.locator('#cb-search').fill('1961.94');page.wait_for_function("document.querySelector('#cb-result-count').textContent.startsWith('当前1组')");assert page.locator('[data-record-id]:visible').count()==1
  page.locator('button[type=reset]').click();page.wait_for_function("document.querySelector('#cb-result-count').textContent.startsWith('当前38组')")
  page.locator('#cb-museum').select_option('noma');assert page.locator('[data-record-id]:visible').count()==5
  page.locator('#cb-religion').select_option('佛教');assert page.locator('[data-record-id]:visible').count()==2
  page.locator('#cb-religion').select_option('');page.locator('#cb-religion').select_option('耆那教');assert page.locator('[data-record-id]:visible').count()==1
  page.go_back();assert page.locator('[data-record-id]:visible').count()==5;assert page.locator('#cb-religion').input_value()==''
  page.reload();page.wait_for_selector('[data-map-box]:not([hidden])');assert page.locator('#cb-museum').input_value()=='noma'
  page.locator('button[type=reset]').click();page.wait_for_function("document.querySelector('#cb-result-count').textContent.startsWith('当前38组')")
  page.locator('#cb-group').select_option('extension');assert page.locator('[data-record-id]:visible').count()==2
  page.locator('button[type=reset]').click();page.wait_for_function("document.querySelector('#cb-result-count').textContent.startsWith('当前38组')")
  page.locator('#cb-sort').select_option('date');assert page.locator('[data-record-id]').first.get_attribute('data-record-id')=='c38'
  page.locator('[data-map-box]').scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'map-{width}.png'))
  page.locator('#cb-map [data-museum=seattle]').focus();page.keyboard.press('Enter');assert page.locator('#cb-museum').input_value()=='seattle';assert page.locator('[data-record-id]:visible').count()==1
  page.locator('button[type=reset]').click();page.wait_for_function("document.querySelector('#cb-result-count').textContent.startsWith('当前38组')")
  clusters=page.locator('#cb-map [data-cluster]:not([data-museum])')
  if clusters.count():clusters.first.focus();page.keyboard.press('Enter');assert page.locator('#cb-map [data-museum]').count()>0
  page.goto(BASE+'sources/#PORTRAIT');page.wait_for_function("document.getElementById('PORTRAIT').open")
  page.goto(BASE+'guide/#timeline');page.wait_for_selector('.cb-time-navigation:not([hidden])');page.wait_for_timeout(350);page.emulate_media(reduced_motion='reduce')
  page.evaluate("window.scrollTo(0,document.getElementById('cb-time-track').getBoundingClientRect().top+scrollY+350)");page.wait_for_timeout(150)
  assert abs(page.locator('.cb-time-navigation').bounding_box()['y'])<2
  y=page.evaluate('scrollY');bb=page.locator('#cb-time-next').bounding_box();page.mouse.click(bb['x']+bb['width']/2,bb['y']+bb['height']/2);page.wait_for_function("document.getElementById('cb-time-track').scrollLeft>0");assert abs(page.evaluate('scrollY')-y)<2
  page.locator('#cb-time-period').evaluate('(el)=>el.focus({preventScroll:true})');page.keyboard.press('End');page.keyboard.press('Enter');page.wait_for_function("document.getElementById('cb-time-next').disabled");assert abs(page.evaluate('scrollY')-y)<2
  page.screenshot(path=str(OUT/f'timeline-{width}.png'));page.locator('#cb-time-period').select_option('0');page.wait_for_function("document.getElementById('cb-time-prev').disabled")
  print('PASS',width,'layouts, captions, viewer, map, filters/history, timeline, navigation',flush=True);page.close()
 ctx=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844});page=ctx.new_page();page.goto(BASE+'atlas/');assert page.locator('[data-record-id]').count()==38 and page.locator('.cb-museum-buttons a').count()==12;ctx.close()
 page=browser.new_page();page.route('**/ne_110m_land.geojson',lambda route:route.abort());page.goto(BASE+'atlas/');page.wait_for_selector('#cb-filters:not([hidden])');assert page.locator('[data-record-id]').count()==38;page.close()
 assert not errors,errors;browser.close();print('PASS: no browser exceptions; no-JS and map failure fallbacks.')
