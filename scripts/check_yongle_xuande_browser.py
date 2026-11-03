"""Real desktop/mobile checks for the court-art topic and cross-topic entries."""
import functools,http.server,threading
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
root=f'http://127.0.0.1:{server.server_port}/museum-notes/';url=root+'yongle-xuande/'
errors=[];bad=[]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,args=['--no-sandbox']);page=b.new_page()
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('response',lambda r:bad.append(r.url) if r.status>=400 and r.url.startswith(root) else None)
 def overflow():assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),page.url
 def decode(im):im.evaluate('(im)=>im.decode()')
 for width in [1440,390,320]:
  page.set_viewport_size({'width':width,'height':950});page.goto(url);overflow()
  expect(page.locator('.yx-core .yx-work')).to_have_count(4)
  decode(page.locator('.yx-cover img'))
  page.screenshot(path=f'/tmp/yongle-cover-{width}.png')
  for wid in ['w1643','w1512','w1516','w1567','w1486','w1571','w1572']:
   page.goto(url+'#'+wid);node=page.locator('#'+wid);node.scroll_into_view_if_needed();overflow()
   for im in node.locator('img').all():
    if not im.is_visible():continue
    decode(im)
    assert im.evaluate('(im)=>Math.abs(im.width/im.height-im.naturalWidth/im.naturalHeight)<.01')
    figure=im.locator('xpath=ancestor::figure');caption=figure.locator('figcaption')
    ib=im.bounding_box();cb=caption.bounding_box()
    assert abs(ib['x']-cb['x'])<2 and abs(ib['width']-cb['width'])<2
    assert 0<=cb['y']-(ib['y']+ib['height'])<18
   if wid in ['w1516','w1486','w1571']:page.screenshot(path=f'/tmp/yongle-{wid}-{width}.png')
   for summary in node.locator('details>summary').all():
    summary.focus();page.keyboard.press('Enter');assert summary.locator('..').evaluate('(d)=>d.open');overflow()
   link=node.locator('[data-photo]').first;link.click();expect(page.locator('#art-lightbox')).to_be_visible();decode(page.locator('#large-photo'))
   page.locator('#zoom-toggle').click();expect(page.locator('#zoom-toggle')).to_have_attribute('aria-pressed','true')
   page.keyboard.press('Escape');expect(page.locator('#art-lightbox')).not_to_be_visible();expect(link).to_be_focused()
  page.goto(url+'#w1643');detail=page.locator('a[href$="h1658.jpg"]');detail.click();decode(page.locator('#large-photo'));page.keyboard.press('Escape')
  page.goto(root+'himalayan-art/#topic-studies');page.locator('#topic-studies').scroll_into_view_if_needed();overflow()
  page.screenshot(path=f'/tmp/yongle-topic-entries-{width}.png')
  page.locator('#topic-studies a[href="../yongle-xuande/"]').click();expect(page.locator('h1')).to_have_text('永宣宫廷造像')
  page.goto(root+'himalayan-art/u23/');page.locator('.ha-topic-return a').click();assert page.url==url
  page.goto(root+'densatil/#related-background');page.locator('#related-background a[href$="#phagmodrupa"]').click();expect(page.locator('#phagmodrupa')).to_have_attribute('open','')
  for old in [root+'himalayan-art/w1514/',url+'w1514/',root+'himalayan-art/?work=w1514#places',url+'#w1514']:
   page.goto(old);page.wait_for_url(lambda u:'w1486' in u);overflow()
  page.goto(root+'himalayan-art/?museum=met#places');page.wait_for_selector('.ha-filters:not([hidden])')
  expect(page.locator('#ha-matches a[href="w1512/"]')).to_be_visible();expect(page.locator('#ha-matches a[href="w1516/"]')).to_be_visible()
  assert page.locator('#ha-museum option[value="british"]').count()==0
  assert page.locator('#ha-museum option[value="berlin"]').count()==0
  page.locator('[data-reset]').first.click();assert 'museum=' not in page.url
  page.go_back();expect(page.locator('#ha-museum')).to_have_value('met')
 plain=b.new_page(java_script_enabled=False,viewport={'width':390,'height':844});plain.goto(url)
 plain.locator('#w1512 .yx-record summary').click();expect(plain.locator('#w1512 .yx-record dl')).to_be_visible()
 assert not errors,errors
 assert not bad,bad
 b.close()
server.shutdown()
print('PASS: desktop 1440px / mobile 390px and 320px; full photos and aligned captions, record disclosures, lightbox/zoom/Escape, entries/returns, aliases, Met map and Back, no-JS fallback. Screenshots /tmp/yongle-*.png.')
