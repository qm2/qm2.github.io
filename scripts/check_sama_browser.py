"""Exercise SAMA additions at desktop/mobile widths; screenshots stay outside Git."""
import functools,http.server,threading,json
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
 def copyfile(self,*args):
  try:super().copyfile(*args)
  except (BrokenPipeError,ConnectionResetError):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/museum-notes/'
errors=[];bad=[]
with sync_playwright() as p:
 browser=p.chromium.launch(args=['--no-sandbox'])
 page=browser.new_page()
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('response',lambda r:bad.append((r.status,r.url)) if r.status>=400 and (r.url.startswith(base) or 'images.mertonmuseum.com' in r.url) else None)
 def go(path):
  page.goto(base+path,wait_until='networkidle');assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),page.url
 def lightbox(a):
  a.click();expect(page.locator('#art-lightbox')).to_be_visible();page.locator('#large-photo').evaluate('(im)=>im.decode()');page.keyboard.press('Escape');expect(page.locator('#art-lightbox')).not_to_be_visible()
 for width in [1440,390]:
  page.set_viewport_size({'width':width,'height':950})
  for n in range(7,26):
   go(f'himalayan-art/sama-{n:02d}/')
   page.locator('main img').first.evaluate('(im)=>im.decode()')
   lightbox(page.locator('main a[data-photo]').first)
   page.locator('#labels summary').click();page.locator('#labels img').first.evaluate('(im)=>im.decode()');lightbox(page.locator('#labels a[data-photo]').first)
   if n in [8,9,14]:
    page.evaluate('scrollTo(0,0)');page.screenshot(path=f'/tmp/sama-{n}-{width}.png')
  go('himalayan-art/?museum=sama#places')
  expect(page.locator('#ha-museum')).to_have_value('sama');expect(page.locator('#ha-count')).to_contain_text('19 /');assert page.locator('.ha-record:not([hidden])').count()==19
  page.locator('#ha-matches img').first.evaluate('(im)=>im.decode()')
  page.locator('[data-view="museums"]').click();page.screenshot(path=f'/tmp/sama-map-{width}.png')
  page.locator('[data-reset]').first.click();page.go_back();expect(page.locator('#ha-museum')).to_have_value('sama')
  go('early-buddhist-art/#museum-sama')
  expect(page.locator('#eb-map-result')).to_contain_text('4 条作品记录');assert page.locator('#eb-map-result img').count()==4
  page.locator('#eb-map-result img').first.evaluate('(im)=>im.decode()')
  for uid in ['u01','u05','u06','u12']:
   go(f'early-buddhist-art/{uid}/')
   imgs=page.locator('a[data-photo][href*="sama-2026"]')
   assert imgs.count();lightbox(imgs.first)
  go('roman-sarcophagi/r28/')
  page.locator('main img').first.evaluate('(im)=>im.decode()');lightbox(page.locator('main a[data-photo]').first)
  page.locator('#labels summary').click();lightbox(page.locator('#labels a[data-photo]').first)
  page.screenshot(path=f'/tmp/sama-roman-{width}.png')
  go('roman-sarcophagi/atlas/?museum=sama#catalogue');assert page.locator('[data-record]:not([hidden])').count()==1;assert page.locator('[data-time-record]:not([hidden])').count()==1
  go('images-and-vows/atlas/?museum_id=sama#catalogue');assert page.locator('.va-card:not([hidden])').count()==1
  page.locator('#work-sama-eastern-wei-maitreya summary').first.click();lightbox(page.locator('#work-sama-eastern-wei-maitreya a[data-photo]').first)
  go('yuan-blue-and-white/#sama-duck-dish');page.locator('#sama-duck-dish img').first.evaluate('(im)=>im.decode()');page.screenshot(path=f'/tmp/sama-yuan-{width}.png')
  go('yuan-blue-and-white/compare/')
  assert page.locator('img[src*="sama-2026"]').count()>=3
  for topic,anchor in [('nimrud-guardians','sama-head'),('densatil','sama-goddesses'),('song-liao-jin-wood','object-2455')]:
   go(f'{topic}/#{anchor}');panel=page.locator('#'+anchor);panel.locator('img').first.evaluate('(im)=>im.decode()');panel.screenshot(path=f'/tmp/sama-{topic}-{width}.png')
   # Legacy shared viewer uses .lightbox rather than the newer dialog.
   link=panel.locator('a.photo-open, a.photo-link, a.lightbox-link, a[data-photo]').first
   if link.count():
    link.click();expect(page.locator('dialog[open]')).to_be_visible();page.locator('dialog[open] img').evaluate('(im)=>im.decode()');page.keyboard.press('Escape')
  print('PASS SAMA viewport',width,flush=True)
 assert not errors,errors;assert not bad,bad
 browser.close()
server.shutdown()
print('PASS: all 19 new Himalayan detail pages, labels/lightboxes; 4 early readings; map filters and Back; Roman/Vows time filters; all topic anchors; desktop and 390px.')
