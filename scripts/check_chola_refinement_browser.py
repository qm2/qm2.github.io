from playwright.sync_api import sync_playwright
from pathlib import Path
import sys
O=Path('/tmp/chola-refinement');O.mkdir(exist_ok=True)
url=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8765')+'/museum-notes/chola-bronzes/'
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,768,390]:
  page=b.new_page(viewport={'width':width,'height':1000});page.add_init_script("document.addEventListener('DOMContentLoaded',()=>document.documentElement.style.scrollBehavior='auto')")
  page.goto(url,wait_until='networkidle');page.screenshot(path=str(O/f'after-cover-{width}.png'))
  x=page.locator('#beyond');x.scroll_into_view_if_needed();x.locator('img').evaluate_all('(imgs)=>Promise.all(imgs.map(i=>i.decode()))');page.evaluate('document.activeElement.blur()');x.screenshot(path=str(O/f'after-sixth-{width}.png'))
  units=page.locator('.cb-faith-pair>section');boxes=[i.locator('h3').bounding_box() for i in units.all()]
  if width>650:assert abs(boxes[0]['y']-boxes[1]['y'])<1
  assert units.nth(0).locator('img').bounding_box()['width']<=164
  for i in units.all():
   a=i.locator('figure>a').bounding_box();cap=i.locator('figcaption').bounding_box();assert abs(a['x']-cap['x'])<1 and 0<=cap['y']-(a['y']+a['height'])<15
  units.nth(0).locator('a[data-photo]').click();page.locator('#large-photo').evaluate('(i)=>i.decode()');assert 'noma_three_buddhas_case.jpg' in page.locator('#large-photo').get_attribute('src');page.keyboard.press('Escape')
  for slug,selector in [('c37/','.cb-full'),('guide/#buddhist-port','#buddhist-port'),('atlas/?religion=%E4%BD%9B%E6%95%99#catalogue','#catalogue'),('c38/','.cb-section:has(.cb-grid)'),('guide/#tamil-map','#tamil-map')]:
   page.goto(url+slug,wait_until='networkidle');el=page.locator(selector).first;el.scroll_into_view_if_needed();el.locator('img:visible').evaluate_all('(imgs)=>Promise.all(imgs.map(i=>{i.loading="eager";return i.decode()}))');page.screenshot(path=str(O/f'{slug.split("/")[0]}-{selector.replace("#", "").replace(".", "").replace(":", "_").replace("(", "").replace(")", "")}-{width}.png'))
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
  for slug in ['saints/','dance/','afterlives/']:
   page.goto(url+slug,wait_until='domcontentloaded');assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1');page.locator('main img').first.evaluate('(i)=>i.decode()')
  page.goto(url+'guide/#place-nagapattinam');page.wait_for_function("document.getElementById('place-nagapattinam').open");assert page.locator('#place-nagapattinam a[href$="c37/"]').count()==1
  page.goto(url+'guide/#tamil-map');assert page.locator('.cb-history-map').evaluate('(e)=>e.scrollWidth<=e.clientWidth+1');mark=page.locator('.cb-history-map a[href="#place-thanjavur"]');mark.focus();page.keyboard.press('Enter');page.wait_for_function("document.getElementById('place-thanjavur').open");assert page.url.endswith('#place-thanjavur')
  print('PASS focused refinement',width,flush=True);page.close()
 b.close()
