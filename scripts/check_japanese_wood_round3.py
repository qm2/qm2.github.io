"""Third editorial reading: cited dimensions, notes and continuous chapter navigation."""
from pathlib import Path
import json,re,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
B=ROOT/'museum-notes/japanese-buddhist-sculpture'
BASE=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8774')+'/museum-notes/japanese-buddhist-sculpture/'
OUT=Path('/tmp/japanese-wood-round3');OUT.mkdir(exist_ok=True)
chapters=json.loads((B/'data/chapters.json').read_text())[1:7]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 for width in [1440,768,390]:
  context=browser.new_context(viewport={'width':width,'height':900},is_mobile=width==390,has_touch=width==390)
  page=context.new_page();errors=[];page.on('pageerror',lambda x:errors.append(str(x)))
  page.add_init_script("document.addEventListener('DOMContentLoaded',()=>document.documentElement.style.scrollBehavior='auto')")
  for i,ch in enumerate(chapters):
   page.goto(BASE+ch['id']+'/');nav=page.locator('.jw-chapter-nav')
   assert nav.locator('a[rel=prev]').count()==int(i>0)
   assert nav.locator('a[rel=next]').count()==int(i<5)
   if i<5:
    assert nav.locator('a[rel=next]').get_attribute('href').endswith(chapters[i+1]['id']+'/')
    nav.locator('a[rel=next]').click();assert page.url.endswith(chapters[i+1]['id']+'/')
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  page.goto(BASE+'04-wrath/');assert '信仰的关联地与某尊实物的原供寺院仍是两回事' not in page.locator('main').inner_text()
  article=page.locator('article.jw-prose');article.locator('h2').last.scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'zao-reading-{width}.png'))
  page.goto(BASE+'j23/');assert '33日' in page.locator('main').inner_text();assert '工序日志' not in page.locator('main').inner_text()
  assert '94.6' in page.locator('.jw-dimensions').inner_text();page.locator('.jw-prose').first.scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'koshun-reading-{width}.png'))
  page.goto(BASE+'j61/');assert all(x in page.locator('main').inner_text() for x in ['1472','Daisan-ji','七条佛所','53.3'])
  page.locator('.jw-research-note summary').click();assert '英文释文' in page.locator('.jw-research-note').inner_text();page.locator('.jw-research-note').scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'koei-notes-{width}.png'))
  page.goto(BASE+'j22/');assert page.locator('.jw-research-note').get_attribute('open') is None
  page.locator('.jw-research-note summary').focus();page.keyboard.press('Enter');assert page.locator('.jw-research-note').get_attribute('open') is not None
  assert '15份样本' in page.locator('.jw-research-note').inner_text()
  page.goto(BASE+'j13/');assert '92.4' in page.locator('.jw-dimensions').inner_text() and '218.4' in page.locator('.jw-dimensions').inner_text()
  page.goto(BASE+'sources/#S-CMA-AMIDA-PAPER');assert page.locator('#S-CMA-AMIDA-PAPER').get_attribute('open') is not None
  assert '延伸阅读：已核书目，未阅全文' in page.locator('#S-CMA-AMIDA-PAPER').inner_text()
  # Include closed details, not only currently visible text.
  source_text=page.locator('main').text_content();assert not re.search('403|超时|本轮|上一轮',source_text)
  page.goto(BASE+'compare/#c10');group=page.locator('#c10');assert '279.4' in group.inner_text() and '440' in group.inner_text()
  group.locator('img').evaluate_all('(imgs)=>Promise.all(imgs.map(i=>i.decode()))');group.scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'wood-bronze-{width}.png'))
  group.locator('a[data-photo]').first.click();assert page.locator('#art-lightbox').is_visible();page.keyboard.press('Escape')
  page.goto(BASE+'compare/#c08');assert page.locator('#c08 .jw-front-back').count()==3
  page.goto(BASE+'atlas/?museum=CMA');page.wait_for_selector('#jw-filters:not([hidden])');assert page.locator('#jw-count').inner_text().startswith('8 /')
  assert page.locator('[data-record-id]:visible').count()==8 and page.locator('.jw-time-row:visible').count()==8
  assert not errors,errors
  print('PASS round3',width,'chapter links, prose, citations, dimensions, folded notes, viewer and CMA count',flush=True)
  context.close()
 browser.close()
