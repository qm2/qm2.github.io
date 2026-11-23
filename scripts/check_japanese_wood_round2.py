"""Second-edition editorial and browser regressions: paired photographs and linked reading."""
from pathlib import Path
import json,re,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'museum-notes/japanese-buddhist-sculpture';BASE=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8774')+'/museum-notes/japanese-buddhist-sculpture/'
OUT=Path('/tmp/japanese-wood-round2');OUT.mkdir(exist_ok=True)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 for width in [1440,768,390]:
  ctx=browser.new_context(viewport={'width':width,'height':900},has_touch=width==390,is_mobile=width==390);page=ctx.new_page()
  page.add_init_script("document.addEventListener('DOMContentLoaded',()=>{document.documentElement.style.scrollBehavior='auto'})")
  page.goto(BASE+'compare/#c08');pairs=page.locator('#c08 .jw-front-back');assert pairs.count()==3
  for pair,nums in zip(pairs.all(),[[3161,3164],[3209,3210],[3250,3251]]):
   assert [next(n for n in nums if '_'+str(n)+'_'in a.get_attribute('href')) for a in pair.locator('a[data-photo]').all()]==nums
  pairs.first.scroll_into_view_if_needed();pairs.first.locator('img').first.evaluate('(i)=>i.decode()');page.screenshot(path=str(OUT/f'back-pairs-{width}.png'))
  pairs.first.locator('a[data-photo]').nth(1).click();assert '背面' in page.locator('#lightbox-caption').inner_text();page.keyboard.press('Escape')
  page.goto(BASE+'compare/#c04');page.locator('#c04 .jw-comparison-detail summary').first.click();crop=page.locator('#c04 .jw-crop').first;crop.scroll_into_view_if_needed();crop.locator('img').evaluate('(i)=>i.decode()');page.screenshot(path=str(OUT/f'comparison-detail-{width}.png'))
  assert '局部' in crop.inner_text();crop.locator('a').click();assert '3130' in page.locator('#large-photo').get_attribute('src');page.keyboard.press('Escape')
  page.goto(BASE+'j23/');imgs=page.locator('main a[data-photo]').all();assert '_3161_'in imgs[0].get_attribute('href') and '_3164_'in imgs[1].get_attribute('href')
  assert '康俊（Kōshun）'in page.locator('.jw-core').inner_text();assert 'Koshin、Joshun'in page.locator('.jw-core').inner_text()
  for route in ['01-crossing/','02-body/','03-pureland/','04-wrath/','05-people/','06-survival/','guide/']:
   page.goto(BASE+route);article=page.locator('article.jw-prose');assert article.locator('a[data-photo]').count()>=2,route
   assert not re.search(r'j\d{2}',article.inner_text()),route
   assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),(width,route)
  page.goto(BASE+'03-pureland/');assert '_3161_'in page.locator('main a[data-photo]').first.get_attribute('href')
  page.goto(BASE+'j12/');fig=page.locator('.jw-full').first;assert width<1100 or fig.bounding_box()['width']>900
  page.screenshot(path=str(OUT/f'wide-group-{width}.png'))
  page.goto(BASE+'guide/#maker-koshun');assert page.locator('#maker-koshun').get_attribute('open')is not None
  page.goto(BASE+'guide/#era-medieval');assert page.locator('#era-medieval').get_attribute('open')is not None
  page.locator('#era-medieval img').evaluate_all('(imgs)=>Promise.all(imgs.map(i=>i.decode()))');page.screenshot(path=str(OUT/f'history-{width}.png'))
  page.goto(BASE+'atlas/');page.wait_for_selector('#jw-map-box:not([hidden])');periods=page.locator('#jw-period option').all_text_contents();assert periods[1]=='8—10世纪',periods
  page.locator('#jw-museum').select_option('CMA');assert page.locator('#jw-count').inner_text().startswith('8 /');page.locator('[data-map=paris]').click();assert page.locator('#jw-map-empty').is_visible();assert '克利夫兰'in page.locator('#jw-map-status').inner_text()
  page.locator('#jw-map-clear').click();page.wait_for_function("document.querySelector('#jw-count').textContent.startsWith('62 /')");assert not page.locator('#jw-map-empty').is_visible();assert page.locator('#jw-map [role=button]').count()==2
  page.screenshot(path=str(OUT/f'map-paris-{width}.png'))
  page.locator('#jw-search').fill('没有这件作品');assert page.locator('#jw-empty').is_visible();assert page.locator('.jw-time-row:visible').count()==0;page.locator('button[type=reset]').click();page.wait_for_function("document.querySelector('#jw-count').textContent.startsWith('62 /')")
  scroll=page.locator('.jw-time-scroll');assert scroll.evaluate('(e)=>e.scrollHeight<=e.clientHeight+2')
  scroll.evaluate('(e)=>e.scrollIntoView({block:"start",behavior:"instant"})');page.evaluate('scrollBy(0,450)');axis=page.locator('.jw-time-axis-shell');assert abs(axis.bounding_box()['y'])<2
  scroll.evaluate('(e)=>{e.scrollLeft=420}');page.wait_for_timeout(50);assert page.locator('.jw-time-axis').evaluate('(e)=>new DOMMatrixReadOnly(getComputedStyle(e).transform).m41') == -scroll.evaluate('(e)=>e.scrollLeft')
  assert page.locator('.jw-version-range').count()==2;assert page.locator('.jw-period-range').count()==1
  if width==390:
   cdp=ctx.new_cdp_session(page);before=page.evaluate('scrollY');cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':280,'y':650}]})
   for y in [600,530,450,370,290]:cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':280,'y':y}]});page.wait_for_timeout(30)
   cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});page.wait_for_timeout(200);assert page.evaluate('scrollY')>before+100,'Vertical touch must escape no nested scroller'
  page.screenshot(path=str(OUT/f'timeline-{width}.png'))
  print('PASS round2',width,'grouped backs, crop labels, explicit order, chapter illustrations, maker/history anchors, map empty/reset, fixed axis and page scroll',flush=True);ctx.close()
 browser.close()
