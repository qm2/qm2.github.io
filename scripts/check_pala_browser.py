"""Actual browser acceptance at desktop/tablet/mobile widths, including map and shared viewer."""
from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'museum-notes/pala-stone';BASE=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8774')+'/museum-notes/pala-stone/'
OUT=Path('/tmp/pala-refine/acceptance');OUT.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True);errors=[]
 for width in [1440,768,390]:
  page=browser.new_page(viewport={'width':width,'height':950});page.on('pageerror',lambda error:errors.append(str(error)))
  page.add_init_script("document.addEventListener('DOMContentLoaded',()=>{document.documentElement.style.scrollBehavior='auto'})")
  page.goto(BASE.replace('pala-stone/','south-asian-art/'))
  assert page.locator('.notebook-index > .issue-link').count()==4
  for selector in ['', ' > img', ' > div']:
   boxes=[el.bounding_box() for el in page.locator('.notebook-index > .issue-link'+selector).all()]
   assert max(v['x'] for v in boxes)-min(v['x'] for v in boxes)<1
   assert max(v['width'] for v in boxes)-min(v['width'] for v in boxes)<1
  routes=['','atlas/','compare/','guide/','journeys/','w1698/','w1510/','w1508/','stories/','p3280/','p3308/','p3294/']
  if width==1440:routes=[str(f.parent.relative_to(B))+'/' for f in B.rglob('index.html')];routes=[''if s=='./'else s for s in routes]
  for slug in routes:
   r=page.goto(BASE+slug,wait_until='domcontentloaded');assert r.status==200,(slug,r.status)
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),(width,slug)
   if page.locator('main img').count():
    im=page.locator('main img').first;im.evaluate('(i)=>i.decode()');assert im.evaluate('(i)=>i.naturalWidth>0')
   if slug in ['','p3280/','p3308/']:
    page.screenshot(path=str(OUT/f'{slug.strip("/") or "home"}-{width}.png'))
  page.goto(BASE+'p3308/');page.locator('a[data-photo]').first.click();assert page.locator('#art-lightbox').is_visible();page.locator('#large-photo').evaluate('(i)=>i.decode()');page.locator('#zoom-toggle').click();assert page.locator('#zoom-toggle').get_attribute('aria-pressed')=='true';page.locator('#zoom-toggle').click();page.locator('#photo-next').click();assert '局部' in page.locator('#lightbox-caption').inner_text();page.keyboard.press('Escape');assert not page.locator('#art-lightbox').is_visible()
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
  page.goto(BASE+'guide/#place-nalanda');page.wait_for_function("document.getElementById('place-nalanda').open")
  page.locator('.ps-history-map a').first.focus();page.keyboard.press('Enter');page.wait_for_function("document.querySelector('.ps-place').open")
  page.locator('[data-time="印度教"]').click();assert 0<page.locator('[data-time-work]:visible').count()<24
  assert 'faith=' in page.url;page.reload();assert page.locator('[data-time="印度教"]').get_attribute('aria-pressed')=='true'
  page.locator('[data-time="佛教"]').click();page.go_back();assert page.locator('[data-time="印度教"]').get_attribute('aria-pressed')=='true'
  page.locator('[data-time=""]').click();assert page.locator('[data-time-work]:visible').count()==24
  page.goto(BASE+'guide/')
  track=page.locator('.ps-timeline')
  page.emulate_media(reduced_motion='reduce')
  page.evaluate("window.scrollTo(0,document.getElementById('ps-time-track').getBoundingClientRect().top+scrollY+350)")
  page.evaluate('()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))')
  nav=page.locator('.ps-time-navigation');assert abs(nav.bounding_box()['y'])<2
  y=page.evaluate('scrollY');button=page.locator('#ps-time-next').bounding_box();page.mouse.click(button['x']+button['width']/2,button['y']+button['height']/2)
  page.wait_for_function("document.getElementById('ps-time-track').scrollLeft>0")
  assert abs(page.evaluate('scrollY')-y)<2
  page.locator('#ps-time-period').evaluate('(el)=>el.focus({preventScroll:true})');page.keyboard.press('End');page.keyboard.press('Enter')
  page.wait_for_function("document.getElementById('ps-time-next').disabled")
  assert abs(page.evaluate('scrollY')-y)<2
  page.screenshot(path=str(OUT/f'timeline-sticky-{width}.png'))
  page.locator('#ps-time-period').select_option('0')
  page.wait_for_function("document.getElementById('ps-time-prev').disabled")
  page.locator('#ps-time-next').focus();page.keyboard.press('Enter')
  page.wait_for_function("document.getElementById('ps-time-track').scrollLeft>0")
  page.locator('#ps-time-prev').click();page.wait_for_function("document.getElementById('ps-time-prev').disabled")
  track.evaluate('(el)=>el.scrollLeft=el.scrollWidth');assert track.evaluate('(el)=>el.scrollLeft>0')
  assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
  page.goto(BASE+'w1698/');page.locator('.ps-detail a[data-photo]').first.click();page.locator('#large-photo').evaluate('(i)=>i.decode()');assert '局部' in page.locator('#lightbox-caption').inner_text();page.keyboard.press('Escape')
  page.locator('.ps-detail figcaption a').first.click();page.locator('#large-photo').evaluate('(i)=>i.decode()');assert 'originals/' in page.locator('#large-photo').get_attribute('src');page.keyboard.press('Escape')
  page.goto(BASE+'w1510/#boston');page.locator('.ps-research-comparison').scroll_into_view_if_needed()
  for im in page.locator('.ps-research-comparison img').all():im.evaluate('(i)=>i.decode()')
  for f in page.locator('.ps-research-comparison figure').all():
   box=f.locator('img').bounding_box();cap=f.locator('figcaption').bounding_box()
   assert abs(box['x']-cap['x'])<2 and abs(box['width']-cap['width'])<2
   assert 0<=cap['y']-box['y']-box['height']<20
  page.screenshot(path=str(OUT/f'w1510-history-{width}.png'))
  page.locator('.ps-historical a[data-photo]').click();page.locator('#large-photo').evaluate('(i)=>i.decode()')
  assert '1922' in page.locator('#lightbox-caption').inner_text() and '非本站现场摄影' in page.locator('#lightbox-caption').inner_text()
  page.locator('#zoom-toggle').click();assert page.locator('#zoom-toggle').get_attribute('aria-pressed')=='true';page.keyboard.press('Escape')
  page.goto(BASE+'w1510/#provenance');page.wait_for_function("document.getElementById('provenance').open")
  assert page.locator('#provenance li').count()==10
  page.locator('#record summary').click();assert '原馆藏号' in page.locator('#record').inner_text() and '147.4' in page.locator('#record').inner_text()
  page.goto(BASE+'w1510/');page.locator('.ps-full img').evaluate('(i)=>i.decode()');page.screenshot(path=str(OUT/f'w1510-opening-{width}.png'))
  page.locator('.ps-detail-row').scroll_into_view_if_needed();page.locator('.ps-detail img').evaluate('(i)=>i.decode()');page.screenshot(path=str(OUT/f'w1510-detail-{width}.png'))
  page.goto(BASE+'compare/#lokanatha');assert page.locator('#lokanatha .ps-figure').count()==2
  page.goto(BASE+'atlas/');page.locator('#ps-search').fill('22.381');page.wait_for_function("document.querySelector('#ps-result-count').textContent.startsWith('当前1件')");assert page.locator('[data-record-id]:visible').get_attribute('data-record-id')=='w1510'
  print('PASS',width,'layouts, map/cluster, filter/back/reload, sort, original/label lightbox, captions and sources',flush=True);page.close()
 ctx=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844});page=ctx.new_page();page.goto(BASE+'atlas/');assert page.locator('[data-record-id]').count()==24;assert page.locator('.ps-museum-buttons a').count()==12;ctx.close()
 page=browser.new_page();page.route('**/ne_110m_land.geojson',lambda route:route.abort());page.goto(BASE+'atlas/');page.wait_for_selector('#ps-filters:not([hidden])');assert page.locator('[data-record-id]').count()==24;assert page.locator('.ps-museum-buttons a').count()==12;page.close()
 assert not errors,errors;browser.close();print('PASS fallback without JS/basemap; no browser exceptions.')
