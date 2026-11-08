"""Run against a local server; BASE_URL may override http://127.0.0.1:8791."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
BASE=os.environ.get('BASE_URL','http://127.0.0.1:8791')+'/museum-notes/roman-sarcophagi/'
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True,args=['--no-sandbox'])
  errors=[]; report=[]
  for width in [1440,390,320]:
   page=await browser.new_page(viewport={'width':width,'height':950},device_scale_factor=1)
   page.on('pageerror',lambda e:errors.append(str(e)))
   for slug in ['', 'r11/','r13/','r20/','r21/','r24/','atlas/','compare/','history/']:
    await page.goto(BASE+slug,wait_until='networkidle')
    overflow=await page.evaluate('document.documentElement.scrollWidth>innerWidth')
    assert not overflow,(width,slug,'horizontal overflow')
    if slug in ['', 'r13/','atlas/']:
     await page.evaluate('''async()=>{await Promise.all([...document.querySelectorAll('main img')].map(async i=>{i.loading='eager';await i.decode()}))}''')
     await page.screenshot(path=f'/tmp/roman-{width}-{slug.replace("/","") or "home"}.png',full_page=True)
    report.append({'width':width,'page':slug,'overflow':overflow})
   # Guide navigation, narrow-screen table, six questions, and the new comparison.
   await page.goto(BASE+'history/#field-card',wait_until='networkidle')
   assert await page.locator('#field-card li').count()==6
   await page.wait_for_function('Math.abs(document.getElementById("field-card").getBoundingClientRect().top)<100')
   await page.locator('.rs-documentation summary').click()
   assert await page.locator('.rs-documentation details').evaluate('(e)=>e.open')
   await page.locator('.rs-guide-table').focus()
   if width<600:
    assert await page.locator('.rs-guide-table').evaluate('(e)=>e.scrollWidth>e.clientWidth')
    await page.keyboard.press('ArrowRight');await page.wait_for_timeout(150)
    assert await page.locator('.rs-guide-table').evaluate('(e)=>e.scrollLeft>0')
   await page.goto(BASE+'compare/#battle-and-submission',wait_until='networkidle')
   group=page.locator('#battle-and-submission')
   images=group.locator('img');assert await images.count()==2
   for im in await images.all():
    await im.scroll_into_view_if_needed();await im.evaluate('(e)=>e.decode()')
    assert await im.evaluate('(e)=>Math.abs(e.clientWidth/e.clientHeight-e.naturalWidth/e.naturalHeight)<0.03')
   await group.locator('a[data-photo]').nth(1).click()
   assert 'panel-942' in await page.locator('#large-photo').get_attribute('src')
   assert '1930' in await page.locator('#original-photo').get_attribute('href')
   await page.locator('#zoom-toggle').click();assert await page.locator('#photo-stage').evaluate('(e)=>e.classList.contains("is-zoomed")')
   await page.keyboard.press('Escape')
   # Gallery switching plus show-all, captions and natural image proportions.
   await page.goto(BASE+'r07/',wait_until='networkidle')
   g=page.locator('[data-rs-gallery]');await g.locator('[data-next]').click();assert await g.locator('.rs-slide:not([hidden])').count()==1
   await g.locator('[data-all]').click();assert await g.locator('.rs-slide:not([hidden])').count()==2
   await g.locator('[data-all]').click()
   await page.locator('a[data-photo]').first.click();await page.locator('#large-photo').wait_for(state='visible');assert await page.locator('#art-lightbox').evaluate('(x)=>x.open')
   await page.locator('#zoom-toggle').click();assert await page.locator('#photo-stage').evaluate('(x)=>x.classList.contains("is-zoomed")')
   assert 'originals/' in await page.locator('#original-photo').get_attribute('href')
   await page.keyboard.press('Escape');assert not await page.locator('#art-lightbox').evaluate('(x)=>x.open')
   # Real rotated label opens upright, original preserved separately.
   await page.goto(BASE+'r06/');await page.locator('.rs-labels summary').click();label=page.locator('.rs-labels img');await label.scroll_into_view_if_needed();await label.evaluate('(x)=>x.decode()')
   assert await label.evaluate('(x)=>x.naturalHeight>x.naturalWidth')
   await page.locator('.rs-labels a[data-photo]').click();assert '1913' in await page.locator('#large-photo').get_attribute('src');await page.keyboard.press('Escape')
   # Filtering restores back/forward and drives chronology.
   await page.goto(BASE+'atlas/',wait_until='networkidle');assert await page.locator('[data-record]:not([hidden])').count()==24
   await page.locator('#rs-museum').select_option(label='休斯顿美术馆');assert await page.locator('[data-record]:not([hidden])').count()==3
   assert await page.locator('[data-time-record]:not([hidden])').count()==3
   await page.locator('#rs-clear').click();assert await page.locator('[data-record]:not([hidden])').count()==24
   await page.go_back();assert await page.locator('[data-record]:not([hidden])').count()==3
   await page.locator('#rs-clear').click();await page.locator('#rs-search').fill('缪斯');assert await page.locator('[data-record]:not([hidden])').count()>=4
   await page.locator('#rs-clear').click();await page.locator('.rs-museum-list [data-map-museum]').first.click();assert await page.locator('[data-record]:not([hidden])').count()==6
   await page.locator('.rs-timeline summary').click();assert await page.locator('.rs-timeline').evaluate('(x)=>x.open')
   await page.close()
  # Visit every work and decode all displayed resources (including lazy labels).
  page=await browser.new_page()
  for w in json.load(open(ROOT/'museum-notes/roman-sarcophagi/data/works.json')):
   await page.goto(BASE+w['id']+'/',wait_until='domcontentloaded')
   failures=await page.evaluate('''async()=>{const failures=[];await Promise.all([...document.querySelectorAll('main img')].map(async i=>{i.loading='eager';try{await i.decode()}catch(e){failures.push(i.src)}}));return failures}''')
   assert not failures,(w['id'],failures)
  await browser.close();assert not errors,errors
  Path('/tmp/roman-browser-report.json').write_text(json.dumps(report,indent=2));print('Desktop/mobile: home, 8 representative routes, history guide, field-card anchor, comparison proportions, gallery, zoom, original links, rotated label, filters/history/timeline passed. All 24 detail-page images decoded. No console errors.')
asyncio.run(main())
