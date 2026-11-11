"""Browser regression: actual R2 images, catalogue state, gallery, captions and mobile."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'museum-notes/etruscans'
WORKS=json.loads((B/'data/objects.json').read_text());BASE=os.getenv('BASE_URL','http://127.0.0.1:8765')+'/museum-notes/etruscans/'
async def main():
 async with async_playwright() as pw:
  browser=await pw.chromium.launch(headless=True,args=['--no-sandbox']);errors=[];checks=[]
  for width in [1440,768,390,320]:
   page=await browser.new_page(viewport={'width':width,'height':950});page.on('pageerror',lambda e:errors.append(str(e)))
   routes=['','guide/','atlas/','compare/','sources/','photos/','e045/','e010/','e001/','e106/','e122/','e069/','e117/','e129/','e131/']
   if width==390:routes+= [w['id']+'/' for w in WORKS if w['id']+'/' not in routes]
   for route in routes:
    await page.goto(BASE+route,wait_until='domcontentloaded')
    # Decode visible figures plus cover. Collapsed archive photographs stay lazy.
    bad=await page.evaluate('''async()=>{const bad=[];await Promise.all([...document.querySelectorAll('main figure img')].filter(i=>i.getClientRects().length).map(async i=>{i.loading='eager';try{await i.decode()}catch(e){bad.push(i.src)}}));return bad}''')
    assert not bad,(width,route,bad)
    assert not await page.evaluate('document.documentElement.scrollWidth>innerWidth'),(width,route,'overflow')
    for fig in await page.locator('figure:visible').all():
     im=fig.locator('img');ca=fig.locator('figcaption');ib=await im.bounding_box();cb=await ca.bounding_box()
     assert abs(ib['x']-cb['x'])<2 and abs(ib['width']-cb['width'])<2,(width,route,'caption alignment',ib,cb)
     assert 0<=cb['y']-ib['y']-ib['height']<=17,(width,route,'caption gap',ib,cb)
     assert await im.evaluate('(i)=>Math.abs(i.clientWidth/i.clientHeight-i.naturalWidth/i.naturalHeight)<.025'),(width,route,'distorted')
    checks.append([width,route])
   # Guide captions follow actual photograph width, including expanded entries.
   await page.goto(BASE+'guide/')
   await page.locator('details').evaluate_all('(xs)=>xs.forEach(x=>x.open=true)')
   for mini in await page.locator('.et-mini-photo').all():
    await mini.locator('img').evaluate('(i)=>{i.loading="eager";return i.decode()}')
    ib=await mini.locator('img').bounding_box();cb=await mini.locator('.et-mini-caption').bounding_box()
    assert abs(ib['x']-cb['x'])<1 and abs(ib['width']-cb['width'])<1
    assert 0<=cb['y']-ib['y']-ib['height']<=9
   for fragment in ['ch01','ch04','ch09']:
    await page.goto(BASE+'#'+fragment)
    await page.locator('.et-favorites a[href$="/e045/"]').first.click()
    assert page.url==BASE+'e045/',page.url
   # All five favorites retain a complete first photograph, followed by a gallery.
   for wid,pid in [('e045','p153'),('e010','p038'),('e001','p001'),('e122','p346'),('e106','p296')]:
    await page.goto(BASE+wid+'/');assert pid in await page.locator('main figure a').first.get_attribute('data-original')
   await page.goto(BASE+'e045/');g=page.locator('[data-rs-gallery]');n=await g.locator('.rs-slide').count()
   for i in range(n):
    assert await g.locator('.rs-slide:not([hidden])').count()==1
    im=g.locator('.rs-slide:not([hidden]) img');await im.evaluate('(i)=>{i.loading="eager";return i.decode()}')
    if i<n-1:await g.locator('[data-next]').click()
   await g.locator('[data-all]').click();assert await g.locator('.rs-slide:not([hidden])').count()==n
   await page.locator('main a[data-photo]').first.click();await page.locator('#large-photo').evaluate('(i)=>i.decode()');before=await page.locator('#original-photo').get_attribute('href')
   await page.locator('#photo-next').click();await page.wait_for_timeout(80);assert await page.locator('#original-photo').get_attribute('href')!=before
   await page.locator('#zoom-toggle').click();assert await page.locator('#zoom-toggle').get_attribute('aria-pressed')=='true'
   await page.keyboard.press('Escape');assert not await page.locator('#art-lightbox').evaluate('(d)=>d.open')
   await page.goto(BASE+'e045/#labels');assert await page.locator('#labels').evaluate('(d)=>d.open');await page.locator('#labels a[data-photo]').first.click();assert '/originals/' in await page.locator('#original-photo').get_attribute('href');await page.keyboard.press('Escape')
   # Facets and date overlap are compared against the canonical dataset.
   await page.goto(BASE+'atlas/');assert await page.locator('[data-record]:visible').count()==131
   await page.locator('button[data-map-place="caere"]').click();expected=sum(w['place_id']=='caere' for w in WORKS);assert await page.locator('[data-record]:visible').count()==expected
   assert await page.locator('[data-place-preview="caere"]').is_visible()
   await page.locator('[data-filter="deep"]').select_option('yes');expected=sum(w['place_id']=='caere' and w['is_deep_reading'] for w in WORKS);assert await page.locator('[data-record]:visible').count()==expected
   await page.locator('#et-reset').click();assert await page.locator('[data-record]:visible').count()==131
   await page.go_back();assert await page.locator('[data-record]:visible').count()==expected
   await page.go_forward();assert await page.locator('[data-record]:visible').count()==131
   await page.locator('[data-filter="start"]').fill('-500');await page.locator('[data-filter="start"]').dispatch_event('change')
   await page.locator('[data-filter="end"]').fill('-475');await page.locator('[data-filter="end"]').dispatch_event('change')
   expected=sum(w['date_start']<=-475 and w['date_end']>=-500 for w in WORKS);assert await page.locator('[data-record]:visible').count()==expected
   await page.locator('#timeline summary').click();assert await page.locator('[data-time-record]:visible').count()==expected
   if width<650:
    await page.locator('.et-time-scroll').focus();await page.keyboard.press('ArrowRight');await page.wait_for_timeout(180);assert await page.locator('.et-time-scroll').evaluate('(e)=>e.scrollLeft>0')
   await page.locator('#et-reset').click();await page.locator('#et-search').fill('Cp5193');await page.wait_for_timeout(240);assert await page.locator('[data-record]:visible').count()==1
   await page.locator('#et-reset').click();await page.locator('#et-sort').select_option('date');starts=await page.locator('[data-record]').evaluate_all('(xs)=>xs.map(x=>Number(x.dataset.start))');assert starts==sorted(starts)
   await page.locator('[data-map-more]').click();assert await page.locator('.et-map-list button:visible').count()==18
   await page.locator('[data-map-zoom]').click();assert await page.locator('.et-map-scroll').evaluate('(e)=>e.scrollWidth>e.clientWidth')
   await page.goto(BASE+'atlas/?collection=GETTY#e001');assert await page.locator('#e001').is_visible();assert await page.locator('[data-filter="collection"]').input_value()=='all'
   await page.goto(BASE+'guide/#god-1');assert await page.locator('#god-1').evaluate('(e)=>e.open');await page.locator('#et-lookup').fill('bucchero');assert await page.locator('[data-lookup]:visible').count()==2
   await page.goto(BASE+'photos/?kind=label#p377');assert await page.locator('#p377').is_visible();assert await page.locator('#p377').evaluate('(e)=>e.open')
   await page.locator('#p377 img').evaluate('(i)=>{i.loading="eager";return i.decode()}')
   # Collect final views for visual review, not just DOM assertions.
   for route,name in [('', 'home'),('atlas/','atlas'),('compare/','compare'),('e045/','boy')]:
    await page.goto(BASE+route);await page.locator('main img').first.evaluate('(i)=>i.decode()');await page.screenshot(path=f'/tmp/etruscans-final-{name}-{width}.png')
   await page.close()
  assert not errors,errors;await browser.close()
  Path('/tmp/etruscans-browser-report.json').write_text(json.dumps({'page_viewports':checks,'errors':errors},indent=2));print(f'PASS: {len(checks)} page/viewport checks, actual R2 image decoding, figure alignment, all object pages at mobile width, viewer/zoom/original, labels, filters/map/timeline/history/hash and keyboard.')
asyncio.run(main())
