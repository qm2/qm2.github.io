"""Actual Chromium checks of desktop/mobile reading, photo views and complete inscriptions."""
import functools,http.server,threading,json
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'museum-notes/images-and-vows'
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
 def copyfile(self,*args):
  try:super().copyfile(*args)
  except (BrokenPipeError,ConnectionResetError):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start();root=f'http://127.0.0.1:{server.server_port}/museum-notes/';url=root+'images-and-vows/'
works=json.loads((BASE/'data/works.json').read_text());errors=[];bad=[]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,args=['--no-sandbox']);page=b.new_page()
 page.on('pageerror',lambda err:errors.append(str(err)))
 page.on('response',lambda r:bad.append((r.status,r.url)) if r.status>=400 and r.url.startswith(root) else None)
 def overflow():assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),page.url
 def imagecheck(im):
  im.scroll_into_view_if_needed();im.evaluate('(im)=>Promise.race([im.decode(),new Promise((_,r)=>setTimeout(()=>r(new Error(im.src)),12000))])')
  box=im.bounding_box();cap=im.locator('xpath=ancestor::figure').locator('figcaption').bounding_box()
  assert abs(box['x']-cap['x'])<2 and abs(box['width']-cap['width'])<2,(page.url,box,cap)
  assert 0<=cap['y']-box['y']-box['height']<15
  ratio=im.evaluate('(im)=>im.naturalWidth/im.naturalHeight');assert abs(box['width']/box['height']-ratio)<.015
 def lightbox(a):
  a.click();expect(page.locator('#art-lightbox')).to_be_visible();page.locator('#large-photo').evaluate('(im)=>im.decode()')
  page.locator('#zoom-toggle').click();expect(page.locator('#zoom-toggle')).to_have_attribute('aria-pressed','true')
  page.keyboard.press('Escape');expect(page.locator('#art-lightbox')).not_to_be_visible();expect(a).to_be_focused()
 for width in [1440,390,320]:
  page.set_viewport_size({'width':width,'height':950});page.goto(url);overflow();imagecheck(page.locator('.iv-cover img'));page.evaluate('scrollTo(0,0)');page.screenshot(path=f'/tmp/vows-home-{width}.png')
  page.goto(url+'#catalogue');page.locator('#iv-region').select_option('成都');expect(page.locator('.iv-catalogue li:visible')).to_have_count(4)
  page.locator('#iv-text').select_option('full');expect(page.locator('.iv-catalogue li:visible')).to_have_count(4)
  page.locator('.iv-filters button[type=reset]').click();expect(page.locator('.iv-catalogue li:visible')).to_have_count(15)
  page.locator('#iv-search').fill('法兴');expect(page.locator('.iv-catalogue li:visible')).to_have_count(1)
  page.locator('.iv-catalogue li:visible>a').click();expect(page.locator('h1')).to_have_text('法兴造释迦三尊像');overflow()
  for slug in ['faxing-526','na-494-yin','cd-490-fahai','na-537-lotus','met-528-yiyi','met-543-yiyi','penn-575-c429']:
   print('Viewport',width,slug,flush=True);page.goto(url+slug+'/');overflow();gallery=page.locator('.iv-gallery');tabs=gallery.locator('.iv-gallery-tabs button')
   for tab in tabs.all():
    tab.press('Enter');imagecheck(gallery.locator('.iv-figure:visible img'));lightbox(gallery.locator('.iv-figure:visible a[data-photo]'));overflow()
   multiple=gallery.locator('.iv-figure').count()>1
   if multiple:
    gallery.locator('[data-all]').click();expect(gallery.locator('[data-all]')).to_have_attribute('aria-expanded','true')
   for im in gallery.locator('.iv-figure img').all():imagecheck(im)
   if multiple:gallery.locator('[data-all]').click()
   expect(gallery.locator('.iv-figure:visible')).to_have_count(1)
   for anchor in ['inscription-terms','inscription-variants']:
    if page.locator('#'+anchor).count():
     page.locator('.iv-reading-nav a[href="#'+anchor+'"]').click();expect(page.locator('#'+anchor)).to_have_attribute('open','');overflow()
   if page.locator('.iv-photo-links a').count():
    link=page.locator('.iv-photo-links a').last;target=link.get_attribute('href');link.click()
    expect(page.locator(target)).to_be_visible();imagecheck(page.locator(target+' img'))
    # Selecting another gallery view must not break a repeat link to the same hash.
    tabs.first.click();link.click();expect(page.locator(target)).to_be_visible()
   if slug=='na-494-yin':
    page.locator('#inscription-passage-1').scroll_into_view_if_needed();page.screenshot(path=f'/tmp/vows-passage-{width}.png')
   if page.locator('#full-inscription').count():
    page.goto(url+slug+'/#full-inscription');expect(page.locator('#full-inscription')).to_have_attribute('open','');page.wait_for_function('Math.abs(document.getElementById("full-inscription").getBoundingClientRect().top)<80');overflow()
    if slug=='met-543-yiyi':page.screenshot(path=f'/tmp/vows-transcription-{width}.png')
   if slug=='faxing-526':
    page.goto(url+slug+'/#photo-1841');expect(page.locator('#photo-1841')).to_be_visible();imagecheck(page.locator('#photo-1841 img'));page.screenshot(path=f'/tmp/vows-inscription-photo-{width}.png')
  page.goto(url+'#north-south');page.wait_for_function('Math.abs(document.getElementById("north-south").getBoundingClientRect().top)<80');overflow()
  for im in page.locator('#north-south .iv-figure img').all():imagecheck(im)
  page.locator('#north-south .iv-comparison').scroll_into_view_if_needed();page.screenshot(path=f'/tmp/vows-comparison-{width}.png')
 # All fifteen pages and every published artwork / label image decode, including rotated labels.
 page.set_viewport_size({'width':390,'height':844})
 for w in works:
  print('Checking',w['slug'],flush=True);page.goto(url+w['slug']+'/');overflow()
  if len(w['photos'])>1:page.locator('[data-all]').click()
  page.locator('.iv-facts summary').click()
  for im in page.locator('.iv-figure:visible img').all():imagecheck(im)
  for a in page.locator('.iv-facts a[data-photo]').all():lightbox(a)
 page.goto(root);page.locator('a[href="images-and-vows/"]').click();expect(page.locator('h1')).to_have_text('造像与发愿')
 page.goto(root+'chinese-buddhist-art/');page.locator('a.issue-link[href="../images-and-vows/"]').click();expect(page.locator('h1')).to_have_text('造像与发愿')
 page.goto(root+'xuzhou/x24/');page.locator('a[href="../../images-and-vows/faxing-526/"]').click();expect(page.locator('h1')).to_have_text('法兴造释迦三尊像')
 page.locator('.iv-crosslink a').click();assert page.url.endswith('/xuzhou/x24/')
 plain=b.new_page(java_script_enabled=False,viewport={'width':390,'height':844});plain.goto(url+'na-494-yin/');expect(plain.locator('.iv-gallery .iv-figure:visible')).to_have_count(5)
 if plain.locator('#full-inscription').get_attribute('open') is None:plain.locator('#full-inscription summary').click()
 expect(plain.locator('.iv-transcription')).to_be_visible()
 assert not errors,errors;assert not bad,bad;b.close()
server.shutdown()
print('PASS: desktop 1440, mobile 390/320; full photos and aligned captions, every view and label, full inscriptions, galleries, lightbox zoom/Escape/focus, filters, anchors, reciprocal navigation and no-JS reading.')
