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
    def copyfile(self,*args):
        try: super().copyfile(*args)
        except (BrokenPipeError,ConnectionResetError): pass
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
        expect(page.locator('body')).not_to_have_class('ha-page photo-open')
        expect(link).to_be_focused()
    home();decoded('.ha-cover img');screenshot('desktop-cover');overflow()
    assert page.locator('.ha-cover img').evaluate('(im)=>im.naturalWidth')>=400
    assert not any('/originals/' in r for r in requests)
    initial_images={r for r in requests if '/images/' in r}
    assert len(initial_images)<40, len(initial_images)
    assert not page.locator('#ha-catalogue').evaluate('(d)=>d.open')
    lightbox(page.locator('.ha-cover [data-photo]'))
    expect(page.locator('.ha-personal-text p')).to_have_count(3)
    expect(page.locator('.ha-epigraph cite')).to_contain_text('曾缄译')
    page.locator('#preface').scroll_into_view_if_needed();screenshot('desktop-preface')
    published=[u for u in json.loads((BASE/'data/updates.json').read_text()) if u.get('public',False)]
    expect(page.locator('[data-update]')).to_have_count(min(3,len(published)))
    # The old region query remains valid; only the controls now have two levels.
    home('?region=ngor#places')
    expect(page.locator('#ha-region')).to_have_value('tibet')
    expect(page.locator('#ha-place')).to_have_value('ngor')
    expect(page.locator('[data-map="regions"] [data-region="tibet"]')).to_have_attribute('aria-current','true')
    ngor=sum('ngor' in w['region_ids'] for w in data['works'])
    expect(page.locator('#ha-count')).to_contain_text(f'{ngor} /')
    page.select_option('#ha-place','densatil')
    assert 'region=densatil' in page.url
    page.go_back();expect(page.locator('#ha-place')).to_have_value('ngor')
    page.select_option('#ha-place','');expect(page.locator('#ha-region')).to_have_value('tibet')
    assert 'region=tibet' in page.url
    page.select_option('#ha-region','east-tibet');expect(page.locator('#ha-place-label')).to_be_hidden()
    options=page.locator('#ha-region option').evaluate_all('(items)=>items.map(o=>o.value)')
    assert len(options)==len(set(options)) and 'eastern-tibet' not in options
    home('?region=eastern-tibet#places');expect(page.locator('#ha-region')).to_have_value('east-tibet')
    page.locator('[data-reset]').first.click();expect(page.locator('#ha-place-label')).to_be_hidden()
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
    expect(page.locator('#ha-map-status')).to_contain_text('史密森尼国立亚洲艺术博物馆')
    home('?museum=nmaa&work=w1689#places')
    expect(page.locator('#ha-matches a[href="w1689/"]')).to_be_visible()
    expect(page.locator('[data-map="museums"] [data-museum="nmaa"]')).to_have_attribute('aria-current','true')
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
        page.locator('#preface').scroll_into_view_if_needed();screenshot(f'mobile-{width}-preface');overflow()
        assert page.locator('.ha-personal-text').bounding_box()['width'] <= width-30
        page.select_option('#ha-region','tibet');page.select_option('#ha-place','ngor')
        page.locator('.ha-filters').scroll_into_view_if_needed();screenshot(f'mobile-{width}-hierarchy');overflow()
        page.locator('[data-reset]').first.click()
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
        for uid in ['u04','u16','u18','u19']:
            unit=next(u for u in data['units'] if u['id']==uid)
            page.goto(url+uid+'/')
            preview=page.locator('.ha-comparison-preview')
            preview.scroll_into_view_if_needed();decoded('.ha-comparison-preview img');overflow()
            assert not page.locator('.ha-comparison').evaluate('(el)=>el.open')
            assert page.locator('.ha-comparison-preview article:visible').count()>=1
            for article in page.locator('.ha-comparison-preview article').all():
                assert article.locator('h3 a').get_attribute('href').startswith('../w')
                assert article.locator('.ha-note').first.inner_text()
                assert article.locator('img').bounding_box()['width']>=110
            screenshot(f'{width}-{uid}-comparison')
            first=preview.locator('[data-photo]').first;lightbox(first)
            page.locator('.ha-comparison summary').focus();page.keyboard.press('Enter')
            expect(page.locator('.ha-comparison-grid')).to_be_visible()
            lightbox(page.locator('.ha-comparison-grid [data-photo]').first)
            href=preview.locator('h3 a').first.get_attribute('href')
            preview.locator('h3 a').first.click();assert page.url.endswith(href.removeprefix('../'))
        for unit in data['units']:
            page.goto(url+unit['id']+'/');overflow()
    print('PASS: existing catalogue, map, comparison and mandala interactions',flush=True)
    # Expanded readings, parallel periods, and reciprocal object links.
    for width in [1440,390,360]:
        page.set_viewport_size({'width':width,'height':1000 if width==1440 else 844})
        home();page.locator('#history-entry').scroll_into_view_if_needed();overflow()
        screenshot(f'{width}-history-entry')
        page.locator('#history-entry h2 a').click()
        expect(page.locator('.ha-period')).to_have_count(8)
        assert not page.locator('.ha-period[open]').count()
        screenshot(f'{width}-history-closed');overflow()
        for track in page.locator('.ha-track-title').all(): assert track.is_visible()
        for period in page.locator('.ha-period').all():
            period.locator('summary').focus();page.keyboard.press('Enter')
            assert period.evaluate('(d)=>d.open');overflow()
            assert period.locator('summary > span').evaluate_all('(els)=>els.every(el=>getComputedStyle(el).transform === "none")'), 'Expanded period text must not rotate'
            period.locator('summary').click()
            assert not period.evaluate('(d)=>d.open')
            assert period.locator('summary > span').evaluate_all('(els)=>els.every(el=>getComputedStyle(el).transform === "none")')
            period.locator('summary').click()
            period.locator('.ha-mini img').first.scroll_into_view_if_needed()
            period.locator('.ha-mini img').first.evaluate('(im)=>im.decode()')
            expect(period.locator('.ha-period-body')).to_be_visible()
        page.locator('#nepal-malla').scroll_into_view_if_needed();screenshot(f'{width}-history-open')
        for node in [n for t in json.loads((BASE/'data/history.json').read_text())['tracks'] for n in t['nodes']]:
            page.goto(url+'history/#'+node['id'])
            target=page.locator('#'+node['id'])
            expect(target).to_have_attribute('open','')
            page.wait_for_function('(id)=>document.getElementById(id).getBoundingClientRect().top < innerHeight', arg=node['id'])
            assert target.locator('summary>span').evaluate_all('(els)=>els.every(el=>getComputedStyle(el).transform === "none")')
        page.goto(url+'w1552/')
        page.locator('.ha-history-return a[href="../history/#nepal-malla"]').click()
        assert page.url.endswith('/history/#nepal-malla')
        expect(page.locator('#nepal-malla')).to_have_attribute('open','')
        page.wait_for_function("document.querySelector('#nepal-malla').getBoundingClientRect().top < innerHeight")
        page.go_back();assert page.url.endswith('/w1552/')
        page.locator('a[href="../u25/"]').click()
        for uid in ['u25','u10']:
            page.goto(url+uid+'/');decoded('main>figure img');overflow()
            screenshot(f'{width}-{uid}-opening')
            lightbox(page.locator('main>figure [data-photo]'))
            first=page.locator('.ha-prose>section').first
            first.scroll_into_view_if_needed();screenshot(f'{width}-{uid}-reading');overflow()
            page.locator('.ha-research-notes summary').click()
            expect(page.locator('.ha-research-notes>section')).to_be_visible();overflow()
            page.locator('.ha-research-notes').scroll_into_view_if_needed();screenshot(f'{width}-{uid}-notes')
            for crop in page.locator('.ha-crop').all():
                crop.scroll_into_view_if_needed();crop.locator('img').evaluate('(im)=>im.decode()');overflow()
                assert crop.evaluate('(f)=>{const i=f.querySelector("img"),c=f.querySelector("figcaption");return Math.abs(i.getBoundingClientRect().left-c.getBoundingClientRect().left)<1 && i.clientWidth<=i.naturalWidth && c.getBoundingClientRect().top-i.getBoundingClientRect().bottom<14}')
                lightbox(crop.locator('a[data-photo]').first)
                lightbox(crop.locator('a[data-photo]').last)
            page.locator('.ha-crop-grid').first.scroll_into_view_if_needed();screenshot(f'{width}-{uid}-crops')
            if uid=='u10':
                page.locator('.ha-comparison-preview').scroll_into_view_if_needed()
                lightbox(page.locator('.ha-comparison-preview [data-photo]').first)
        print(f'PASS: {width}px periods, anchors, crops and lightboxes',flush=True)
        home('?work=w1552#places');expect(page.locator('#ha-readings-result')).to_contain_text('四臂之间')
        expect(page.locator('#c3 [data-reading="u25"]')).to_have_class('ha-reading ha-featured ha-associated')
    plain=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844}).new_page()
    plain.goto(url);assert plain.locator('.ha-reading').count()==len(data['units'])
    plain.locator('#ha-catalogue summary').click();assert plain.locator('.ha-record:visible').count()==len(data['works'])
    plain.goto(url+'history/');plain.locator('#nepal-malla summary').click()
    expect(plain.locator('#nepal-malla .ha-history-works')).to_be_visible()
    assert not errors, errors
    assert not bad, bad
    browser.close()
server.shutdown()
print(f'PASS: desktop/390/360px; {len(data["units"])} readings at two widths; filters, history, keyboard, loans, unknown geography, catalogue, mandala, lightboxes, no-JS. Initial image requests: {len(initial_images)}. No runtime/HTTP errors.')
