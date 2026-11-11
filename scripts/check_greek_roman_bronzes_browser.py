"""Exercise the real shared viewer, maps, URL state and responsive compositions."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
from museum_image_urls import HOSTS
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'museum-notes/greek-roman-bronzes/data';WORKS=json.loads((DATA/'works.json').read_text());BASE=os.environ.get('BASE_URL','http://127.0.0.1:8791')+'/museum-notes/greek-roman-bronzes/'
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True,args=['--no-sandbox']);errors=[];checks=[]
  for width in [1440,390,320]:
   page=await browser.new_page(viewport={'width':width,'height':950});page.on('pageerror',lambda err:errors.append(str(err)))
   for route in ['', 'history/','compare/','atlas/']+[w['id']+'/' for w in WORKS]:
    await page.goto(BASE+route,wait_until='domcontentloaded')
    failures=await page.evaluate('''async()=>{const failures=[];await Promise.all([...document.querySelectorAll('main img')].map(async i=>{i.loading='eager';try{await i.decode()}catch(e){failures.push(i.src)}}));return failures}''');assert not failures,(width,route,failures)
    image_host=HOSTS.get('museum-notes/greek-roman-bronzes/images/')
    if image_host:
     assert await page.locator('main img').evaluate_all('(images,host)=>images.every(i=>i.currentSrc.startsWith(host+"/museum-notes/greek-roman-bronzes/images/"))',image_host),(width,route,'image host')
    assert not await page.evaluate('document.documentElement.scrollWidth>innerWidth'),(width,route,'overflow')
    for fig in await page.locator('figure:visible').all():
     img=fig.locator('img');cap=fig.locator('figcaption');ib=await img.bounding_box();cb=await cap.bounding_box()
     assert abs(ib['x']-cb['x'])<2 and abs(ib['width']-cb['width'])<2,(width,route,'caption width')
     assert 0<=cb['y']-(ib['y']+ib['height'])<=15,(width,route,'caption gap')
     assert await img.evaluate('(i)=>Math.abs(i.clientWidth/i.clientHeight-i.naturalWidth/i.naturalHeight)<0.02'),(width,route,'image distorted')
    checks.append([width,route,'images + no overflow + figure alignment'])
   await page.goto(BASE+'b09/');g=page.locator('[data-rs-gallery]');assert await g.locator('.rs-slide:not([hidden])').count()==1
   await g.locator('[data-next]').click();assert '侧面' in await g.locator('.rs-slide:not([hidden]) figcaption').inner_text()
   await g.locator('[data-prev]').click();assert '正面' in await g.locator('.rs-slide:not([hidden]) figcaption').inner_text()
   await g.locator('[data-all]').click();assert await g.locator('.rs-slide:not([hidden])').count()==2
   await g.locator('.rs-slide:not([hidden]) a').first.click();assert '1979' in await page.locator('#original-photo').get_attribute('href')
   await page.locator('#photo-next').click();await page.wait_for_timeout(50);assert '1980' in await page.locator('#original-photo').get_attribute('href')
   await page.locator('#zoom-toggle').click();assert await page.locator('#zoom-toggle').get_attribute('aria-pressed')=='true'
   await page.keyboard.press('Escape');assert not await page.locator('#art-lightbox').evaluate('(e)=>e.open')
   await page.goto(BASE+'b13/#labels');assert await page.locator('#labels').evaluate('(e)=>e.open')
   im=page.locator('#labels img');await im.evaluate('(e)=>{e.loading="eager";return e.decode()}');assert await im.evaluate('(e)=>e.naturalWidth>e.naturalHeight')
   await page.locator('#labels a[data-photo]').click();assert '1992' in await page.locator('#original-photo').get_attribute('href');await page.keyboard.press('Escape')
   await page.goto(BASE+'b14/');await page.locator('.rs-gallery a[data-photo]').click();assert '1993' in await page.locator('#original-photo').get_attribute('href');await page.keyboard.press('Escape')
   await page.goto(BASE+'b16/');await page.locator('.rs-gallery a[data-photo]').click();assert '2001' in await page.locator('#large-photo').get_attribute('src');await page.keyboard.press('Escape')
   await page.goto(BASE+'atlas/',wait_until='networkidle');assert await page.locator('[data-record]:visible').count()==18
   await page.locator('.rs-maps [data-map-museum="capitoline"] circle').click();assert await page.locator('[data-record]:visible').count()==7
   assert await page.locator('[data-museum-preview="capitoline"]').is_visible();assert await page.locator('[data-time-record]:visible').count()==7
   await page.locator('#rs-theme').select_option('英雄与权力');assert await page.locator('[data-record]:visible').count()==2
   await page.locator('#rs-clear').click();assert await page.locator('[data-record]:visible').count()==18
   await page.go_back();assert await page.locator('[data-record]:visible').count()==2
   await page.go_forward();assert await page.locator('[data-record]:visible').count()==18
   await page.locator('#rs-search').fill('阿波罗');assert await page.locator('[data-record]:visible').count()==2
   await page.locator('#rs-clear').click();await page.locator('#rs-search').fill('no-such-title');assert await page.locator('#rs-empty').is_visible()
   await page.goto(BASE+'atlas/?museum=mfah#b18');assert await page.locator('#rs-museum').input_value()=='all';assert await page.locator('#b18').is_visible()
   assert await page.locator('.rs-time-scroll [data-time-record]').count()==17 and await page.locator('.rs-time-scroll [data-time-record="b06"]').count()==0
   assert await page.locator('[data-time-record="b09"] .rs-time-dot').count()==2
   assert await page.locator('[data-time-record="b17"] .gb-alternate').count()==1
   if width<600:
    await page.locator('.rs-time-scroll').focus();await page.keyboard.press('ArrowRight');await page.wait_for_timeout(200);assert await page.locator('.rs-time-scroll').evaluate('(e)=>e.scrollLeft>0')
   await page.locator('.rs-timeline summary').click();assert not await page.locator('.rs-timeline').evaluate('(e)=>e.open')
   await page.locator('.rs-timeline summary').focus();await page.keyboard.press('Enter');assert await page.locator('.rs-timeline').evaluate('(e)=>e.open')
   await page.goto(BASE+'compare/#heroic-body');await page.locator('#heroic-body a[data-photo]').first.click();assert '1962' in await page.locator('#original-photo').get_attribute('href');await page.keyboard.press('Escape')
   await page.goto(BASE+'history/#field-card');assert await page.locator('#field-card li').count()==6
   await page.goto(BASE)
   await page.locator('main img').first.evaluate('(i)=>i.decode()')
   await page.screenshot(path=f'/tmp/bronze-final-home-{width}.png')
   await page.close()
  await browser.close();assert not errors,errors
  Path('/tmp/bronze-browser-report.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2));print(f'PASS: {len(checks)} viewport/page checks; every image decoded, captions aligned, all gallery angles, label rotation, zoom/original, keyboard, map/filter/back-forward/deep links, date alternatives. No JS errors.')
asyncio.run(main())
