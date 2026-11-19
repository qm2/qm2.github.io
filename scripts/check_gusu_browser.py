"""Exercise generated pages at desktop, tablet and mobile widths; screenshots stay in /tmp."""
from pathlib import Path
import json,threading,functools
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=Path('/tmp/gusu-browser-check');OUT.mkdir(exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
 def copyfile(self,source,output):
  try:super().copyfile(source,output)
  except (BrokenPipeError,ConnectionResetError):pass
srv=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=srv.serve_forever,daemon=True).start();url=f'http://127.0.0.1:{srv.server_port}/museum-notes/gusu-prints/'
works=json.loads((ROOT/'museum-notes/gusu-prints/data/works.json').read_text());slugs=['','guide','collection','catalogue','sources']+[w['id'] for w in works];errors=[];report=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
 for width in [1440,768,390]:
  page=browser.new_page(viewport={'width':width,'height':1000},device_scale_factor=1)
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('response',lambda r:errors.append(f'{r.status} {r.url}') if r.status>=400 else None)
  for slug in slugs:
   page.goto(url+(slug+'/' if slug else ''),wait_until='networkidle')
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,slug,'overflow')
   assert page.locator('h1').count()==1
   if slug in ['', 'g03','g26','g29','g30','b02','guide','collection','catalogue']:
    page.locator('img[loading=lazy]').evaluate_all('(nodes)=>nodes.forEach(n=>n.loading="eager")')
    page.wait_for_function('Array.from(document.querySelectorAll("main img")).every(i=>i.complete&&i.naturalWidth>0)')
    checks=page.locator('.gs-figure').evaluate_all('els=>els.filter(f=>f.getClientRects().length).map(f=>{const a=f.querySelector("a"),c=f.querySelector("figcaption"),im=f.querySelector("img");const r=a.getBoundingClientRect(),t=c.getBoundingClientRect();return {left:Math.abs(t.left-r.left),gap:t.top-r.bottom,distortion:Math.abs(im.width/im.height-im.naturalWidth/im.naturalHeight)}})')
    assert all(x['left']<1 and 0<=x['gap']<=15 and x['distortion']<.02 for x in checks),(width,slug,checks)
   if slug=='':
    page.screenshot(path=str(OUT/f'home-{width}.png'))
    page.locator('#first-look').screenshot(path=str(OUT/f'details-{width}.png'))
    page.locator('#first-look a').nth(1).click();assert '/g30/' in page.url
   if slug in ['g03','g26','g29','g30','b02']:
    page.screenshot(path=str(OUT/f'{slug}-{width}.png'))
    page.locator('a[data-photo]').first.click();assert page.locator('#art-lightbox').is_visible()
    page.wait_for_function('document.querySelector("#large-photo").complete&&document.querySelector("#large-photo").naturalWidth>0')
    page.locator('#zoom-toggle').click();assert page.locator('#photo-stage').evaluate('e=>e.classList.contains("is-zoomed")')
    page.keyboard.press('Escape');page.wait_for_function('!document.body.classList.contains("photo-open")')
    page.locator('#labels summary').click();page.locator('#labels a[data-photo]').first.click();assert page.locator('#art-lightbox').is_visible();page.keyboard.press('Escape');page.wait_for_function('!document.body.classList.contains("photo-open")')
   if slug=='g26':page.locator('#compare-seasons').screenshot(path=str(OUT/f'spring-summer-{width}.png'))
   if slug=='g29':page.locator('.gs-four-leaves').screenshot(path=str(OUT/f'westlake-{width}.png'))
   if slug=='b02':
    for button in page.locator('[data-open-page]').all():
     button.focus();page.keyboard.press('Enter');assert button.get_attribute('aria-pressed')=='true';assert page.locator('[data-book-page]:visible').count()==1
     page.locator('[data-book-page]:visible a').click();page.keyboard.press('Escape');page.wait_for_function('!document.body.classList.contains("photo-open")')
   if slug=='catalogue':
    page.locator('#gs-query').fill('2025.46');page.wait_for_timeout(250);assert page.locator('.gs-card:visible').count()==1
    assert page.locator('.gs-card:visible').inner_text().startswith('四季')
    page.locator('#gs-reset').click();assert page.locator('.gs-card:visible').count()==32
    page.go_back();page.wait_for_timeout(200);assert page.locator('.gs-card:visible').count()==1
    page.locator('#gs-reset').click();page.locator('#gs-chapter').select_option('flowers');assert 1<page.locator('.gs-card:visible').count()<32
    page.locator('#gs-query').fill('no-match-zz');page.wait_for_timeout(250);assert page.locator('#gs-empty').is_visible()
    page.locator('#gs-reset').click()
   if slug in ['guide','collection','catalogue']:page.screenshot(path=str(OUT/f'{slug}-{width}.png'))
  for anchor in ['L3054','L2998','S02']:
   page.goto(url+'sources/#'+anchor,wait_until='networkidle');assert page.locator('#'+anchor).is_visible()
   if anchor.startswith('L'):assert page.locator('#'+anchor).get_attribute('open') is not None
  page.goto(url+'#place-suzhou',wait_until='networkidle');assert page.locator('#place-suzhou').get_attribute('open') is not None
  page.locator('#place-suzhou summary').focus();page.keyboard.press('Enter');assert page.locator('#place-suzhou').get_attribute('open') is None
  report.append({'width':width,'pages':len(slugs),'overflow':False,'figcaption_alignment':'passed','lightbox':'image / zoom / Escape / labels passed','book':'all13pages keyboard/lightbox passed','filters':'search/theme/reset/history passed','anchors':'evidence and place expansion passed'})
  page.close()
 page=browser.new_page(java_script_enabled=False,viewport={'width':390,'height':800});page.goto(url+'catalogue/');assert page.locator('.gs-card:visible').count()==32
 page.goto(url+'b02/');assert page.locator('[data-book-page]:visible').count()==13
 browser.close()
srv.shutdown();assert not errors,errors
(OUT/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
