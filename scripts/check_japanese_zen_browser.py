"""Real browser checks, natural photo proportions, disclosure/search and lightbox."""
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
root=f'http://127.0.0.1:{server.server_port}/museum-notes/';url=root+'japanese-zen/'
errors=[];bad=[]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,args=['--no-sandbox']);page=b.new_page()
 page.on('pageerror',lambda x:errors.append(str(x)))
 page.on('response',lambda r:bad.append(r.url) if r.status>=400 and r.url.startswith(root) else None)
 def overflow():assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),page.url
 for width in [1440,390,320]:
  page.set_viewport_size({'width':width,'height':950});page.goto(url);overflow()
  expect(page.locator('.jz-card')).to_have_count(19)
  page.screenshot(path=f'/tmp/zen-home-{width}.png')
  page.locator('#few-strokes').scroll_into_view_if_needed();page.screenshot(path=f'/tmp/zen-gallery-{width}.png')
  page.goto(url+'#catalogue');expect(page.locator('#catalogue details')).to_have_attribute('open','')
  page.locator('#zen-search').fill('波特兰');expect(page.locator('.jz-directory li:visible')).to_have_count(3)
  page.locator('#zen-search').fill('即非');expect(page.locator('.jz-directory li:visible')).to_have_count(1)
  page.locator('#zen-search').fill('');expect(page.locator('.jz-directory li:visible')).to_have_count(19)
  for wid in ['j03','j06','j07','j11','j13','j16','j19']:
   page.goto(url+wid+'/');overflow()
   for im in page.locator('.jz-figure img').all():
    if not im.is_visible():continue
    im.scroll_into_view_if_needed();im.evaluate('(im)=>Promise.race([im.decode(),new Promise((_,reject)=>setTimeout(()=>reject(new Error(im.currentSrc || im.src)),10000))])')
    assert im.evaluate('(im)=>Math.abs(im.width/im.height-im.naturalWidth/im.naturalHeight)<.01')
    box=im.bounding_box();cap=im.locator('xpath=ancestor::figure').locator('figcaption').bounding_box()
    assert abs(box['x']-cap['x'])<2 and abs(box['width']-cap['width'])<2
    assert 0<=cap['y']-box['y']-box['height']<18
   page.locator('#labels>summary').focus();page.keyboard.press('Enter');expect(page.locator('#labels')).to_have_attribute('open','');overflow()
   im=page.locator('#labels img');im.evaluate('(im)=>Promise.race([im.decode(),new Promise((_,reject)=>setTimeout(()=>reject(new Error(im.currentSrc || im.src)),10000))])')
   if wid=='j03':page.locator('#labels').scroll_into_view_if_needed();page.screenshot(path=f'/tmp/zen-label-{width}.png')
   links=page.locator('a[data-photo]')
   for link in links.all():
    link.click();expect(page.locator('#art-lightbox')).to_be_visible();page.locator('#large-photo').evaluate('(im)=>Promise.race([im.decode(),new Promise((_,reject)=>setTimeout(()=>reject(new Error(im.currentSrc || im.src)),10000))])')
    page.locator('#zoom-toggle').click();expect(page.locator('#zoom-toggle')).to_have_attribute('aria-pressed','true')
    page.keyboard.press('Escape');expect(page.locator('#art-lightbox')).not_to_be_visible();expect(link).to_be_focused()
   if wid in ['j06','j16','j19']:
    page.evaluate('scrollTo(0,0)');page.screenshot(path=f'/tmp/zen-{wid}-{width}.png')
  page.goto(url+'j04/');page.locator('.jz-inscription').scroll_into_view_if_needed();page.screenshot(path=f'/tmp/zen-text-{width}.png');overflow()
  page.goto(url+'j16/#labels');expect(page.locator('#labels')).to_have_attribute('open','')
  page.goto(root+'japanese-art/');page.locator('.issue-link').click();expect(page.locator('h1')).to_have_text('日本禅宗书画')
  page.goto(root);page.locator('a.issue-link[href="japanese-art/"]').click();expect(page.locator('h1')).to_have_text('日本艺术')
 # All remaining detail pages load, with no missing images or browser errors.
 for n in range(1,20):
  print('Checking detail',n,flush=True)
  page.goto(url+f'j{n:02}/');overflow()
  page.locator('#labels>summary').click()
  for im in page.locator('.jz-figure img').all():
   im.scroll_into_view_if_needed();im.evaluate('(im)=>Promise.race([im.decode(),new Promise((_,reject)=>setTimeout(()=>reject(new Error(im.currentSrc || im.src)),10000))])')
 plain=b.new_page(java_script_enabled=False,viewport={'width':390,'height':844});plain.goto(url+'j19/');plain.locator('#labels>summary').click();expect(plain.locator('#labels img')).to_be_visible()
 assert not errors,errors;assert not bad,bad
 b.close()
server.shutdown()
print('PASS: desktop 1440px, mobile 390/320px; natural photos/aligned captions, 19 detail pages, label orientation, all gallery lightboxes, zoom/Escape/focus, search, anchors, entrances and no-JS labels. Screenshots /tmp/zen-*.png.')
