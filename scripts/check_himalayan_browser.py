"""Actual desktop/mobile acceptance checks; screenshots remain in /tmp."""
import functools
import http.server
import json
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'museum-notes/himalayan-art'
data=json.loads((BASE/'data/navigation.json').read_text())
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/museum-notes/himalayan-art/'
errors=[];bad=[];requests=[]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1440,'height':1000})
    page.on('pageerror',lambda err:errors.append(str(err)))
    page.on('response',lambda r:bad.append(r.url) if r.status>=400 and r.url.startswith(url) else None)
    page.on('request',lambda r:requests.append(r.url))
    def home(query=''):
        page.goto(url+query); page.wait_for_selector('.ha-filters:not([hidden])')
    def decoded(selector):
        page.locator(selector).first.evaluate('(img)=>img.decode()')
    def screenshot(name):
        page.screenshot(path=f'/tmp/himalayan-{name}.png')
    def overflow():
        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'), page.url
    def lightbox(link):
        link.click();expect(page.locator('#art-lightbox')).to_be_visible();decoded('#large-photo')
        page.locator('#zoom-toggle').click();expect(page.locator('#zoom-toggle')).to_have_attribute('aria-pressed','true')
        page.keyboard.press('Escape');expect(page.locator('#art-lightbox')).not_to_be_visible()
        expect(link).to_be_focused()
    home();decoded('.ha-cover img');screenshot('desktop-cover');overflow()
    assert page.locator('.ha-cover img').evaluate('(im)=>im.naturalWidth')>=400
    assert not any('/originals/' in r for r in requests)
    initial_images={r for r in requests if '/images/' in r}
    assert len(initial_images)<40, len(initial_images)
    assert not page.locator('#ha-catalogue').evaluate('(d)=>d.open')
    lightbox(page.locator('.ha-cover [data-photo]'))
    page.locator('#places').scroll_into_view_if_needed();screenshot('desktop-map')
    link=page.locator('nav [data-region="kashmir-tradition"]')
    link.focus();page.keyboard.press('Enter')
    expected=[w for w in data['works'] if any(x in w['region_ids'] for x in next(g['members'] for g in data['groups'] if g['id']=='kashmir-tradition'))]
    expect(page.locator('#ha-count')).to_have_text(f'{len(expected)} / {len(data["works"])} 条记录')
    museum=next(w['display_museum_id'] for w in expected if w['display_museum_id'])
    page.select_option('#ha-museum',museum)
    page.select_option('#ha-period','800,1199')
    selected=[w for w in expected if w['display_museum_id']==museum and (w['date_start'] is None or w['date_end'] is None or (w['date_start']<=1199 and w['date_end']>=800))]
    expect(page.locator('#ha-count')).to_contain_text(f'{len(selected)} /')
    page.go_back();expect(page.locator('#ha-period')).to_have_value('')
    page.locator('[data-reset]').first.click();expect(page.locator('#ha-region')).to_have_value('')
    page.fill('#ha-search','a-query-with-no-matches');expect(page.locator('#ha-count')).to_contain_text('0 /')
    page.locator('[data-reset]').first.click();page.select_option('#ha-period','unknown')
    unknown=sum(w['date_start'] is None or w['date_end'] is None for w in data['works'])
    expect(page.locator('#ha-count')).to_contain_text(f'{unknown} /')
    home('?work=w1526#places')
    assert page.locator('[data-map]:not([hidden]) [data-region][aria-current]').count()>=2
    home('?work=w1664#places');expect(page.locator('#ha-extended')).to_be_checked()
    home('?work=w1689#places')
    assert page.locator('[data-map]:not([hidden]) [aria-current]').count()==0
    expect(page.locator('#ha-map-status')).to_contain_text('暂不在地图落点')
    home('?collection=rubin&view=collections#places');expect(page.locator('#ha-count')).to_contain_text('3 /')
    expect(page.locator('.ha-map-fold')).to_be_hidden()
    page.locator('[data-reset]').first.click();page.locator('[data-view="museums"]').click()
    assert page.locator('[data-map="museums"] [data-museum="rubin"]').count()==0
    screenshot('desktop-museums')
    page.locator('[data-reset]').first.click();page.locator('#ha-catalogue summary').click()
    expect(page.locator('#w1664')).to_be_visible();page.locator('#w1664 [data-focus]').click()
    expect(page.locator('#ha-map-status')).to_contain_text('旅行佛龛')
    for width in [390,360]:
        page.set_viewport_size({'width':width,'height':844});home();decoded('.ha-cover img')
        page.locator('.ha-cover figure').scroll_into_view_if_needed();screenshot(f'mobile-{width}-cover');overflow()
        fig=page.locator('.ha-cover figure');image=fig.locator('img').bounding_box();cap=fig.locator('figcaption').bounding_box()
        assert abs(image['x']-cap['x'])<2 and abs(image['width']-cap['width'])<2 and 0<=cap['y']-image['y']-image['height']<20
        lightbox(fig.locator('[data-photo]'))
        page.locator('.ha-map-fold').scroll_into_view_if_needed();screenshot(f'mobile-{width}-map')
        page.locator('nav [data-region="kashmir-tradition"]').click();overflow()
        page.locator('#c1').scroll_into_view_if_needed();screenshot(f'mobile-{width}-chapter')
        page.goto(url+'u15/');decoded('[data-plate-panel="0"] img')
        for i,photo in enumerate(['h1692','h1693','h1694','h1695','h1696']):
            page.locator(f'[data-plate="{i}"]').click()
            pane=page.locator(f'[data-plate-panel="{i}"]');expect(pane).to_be_visible()
            assert page.locator('[data-plate-panel]:visible').count()==1
            decoded(f'[data-plate-panel="{i}"] img')
            assert photo in pane.locator('[data-photo]').get_attribute('href')
            lightbox(pane.locator('[data-photo]'));overflow()
        page.locator('[data-plate="0"]').click();page.locator('.ha-detail-view').scroll_into_view_if_needed();screenshot(f'mobile-{width}-mandala')
        page.locator('.ha-comparison summary').click();expect(page.locator('.ha-comparison-grid')).to_be_visible();overflow()
        page.goto(url+'w1700/');decoded('main>figure img');overflow()
        assert page.locator('.ha-details figure').count()==3
        for figure in page.locator('.ha-details figure').all():
            lightbox(figure.locator('[data-photo]'))
    for width in [1440,390]:
        page.set_viewport_size({'width':width,'height':950 if width==1440 else 844})
        for unit in data['units']:
            page.goto(url+unit['id']+'/');overflow()
    plain=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844}).new_page()
    plain.goto(url);assert plain.locator('.ha-reading').count()==len(data['units'])
    plain.locator('#ha-catalogue summary').click();assert plain.locator('.ha-record:visible').count()==len(data['works'])
    assert not errors, errors
    assert not bad, bad
    browser.close()
server.shutdown()
print(f'PASS: desktop/390/360px; {len(data["units"])} readings at two widths; filters, history, keyboard, loans, unknown geography, catalogue, mandala, lightboxes, no-JS. Initial image requests: {len(initial_images)}. No runtime/HTTP errors.')
