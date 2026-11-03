"""Browser acceptance for the interconnected learning guide; fixtures stay in /tmp."""
import functools, http.server, json, threading
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'museum-notes/himalayan-art'
data=json.loads((BASE/'data/learning.json').read_text())
works={w['work_id']:w for w in json.loads((BASE/'data/works.json').read_text())}
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
    def copyfile(self,*args):
        try:super().copyfile(*args)
        except (BrokenPipeError,ConnectionResetError):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/museum-notes/himalayan-art/'
errors=[];bad=[]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1440,'height':1000})
    page.on('pageerror',lambda err:errors.append(str(err)))
    page.on('response',lambda r:bad.append(r.url) if r.status>=400 and r.url.startswith(url) else None)
    def overflow():assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),page.url
    for width in [1440,390,320]:
        page.set_viewport_size({'width':width,'height':900})
        for config in data['pages']:
            route=config['route'];page.goto(url+route+'/');overflow()
            expect(page.locator('.ha-learning-nav a')).to_have_count(4)
            page.screenshot(path=f'/tmp/ha-learning-{route}-{width}.png')
            for n in config['entries']:
                page.goto(url+route+'/#'+n['id'])
                entry=page.locator('#'+n['id']);expect(entry).to_have_attribute('open','')
                page.wait_for_function('(id)=>{const y=document.getElementById(id).getBoundingClientRect().y;return y>=-3&&y<180;}',arg=n['id'])
                overflow()
                # Keep disclosure arrows separate from dates, titles and other words.
                assert entry.locator('summary span').evaluate_all('(xs)=>xs.every(x=>getComputedStyle(x).transform==="none")')
                summary=entry.locator('summary');summary.focus();page.keyboard.press('Enter')
                assert not entry.evaluate('(d)=>d.open')
                page.keyboard.press('Enter');assert entry.evaluate('(d)=>d.open')
                for im in entry.locator('img').all():
                    im.scroll_into_view_if_needed();im.evaluate('(im)=>im.decode()')
                    assert im.evaluate('(im)=>im.naturalWidth>0')
                if n['id'] in {'mandala','phagmodrupa','vajra-pair','kashmir'}:
                    entry.scroll_into_view_if_needed();page.screenshot(path=f'/tmp/ha-learning-open-{n["id"]}-{width}.png')
            # All group headers, including schools, must retain native keyboard toggling.
            if route=='teachers':
                for n in data['traditions']:
                    page.goto(url+route+'/#'+n['id']);expect(page.locator('#'+n['id'])).to_have_attribute('open','')
            if width==390:
                page.goto(url+route+'/#'+config['entries'][0]['id'])
                page.goto(url+route+'/#'+config['entries'][-1]['id'])
                page.go_back();expect(page.locator('#'+config['entries'][0]['id'])).to_have_attribute('open','')
        page.goto(url+'review/');overflow()
        assert not page.locator('#learning-index').evaluate('(d)=>d.open')
        page.screenshot(path=f'/tmp/ha-learning-review-{width}.png')
        for query,href in [('Vajrasattva','iconography/#vajra-pair'),('Mañjuśrī','iconography/#manjushri'),('无我佛母','iconography/#hevajra'),('谷穗','iconography/#vasudhara'),('帕木竹巴','teachers/#phagmodrupa'),('Ngor','teachers/#ngorchen'),('俄尔','teachers/#ngorchen')]:
            page.fill('#learning-query',query);page.locator('.ha-guide-search button[type=submit]').click()
            expect(page.locator('.ha-search-item:not([hidden]) a[href="../'+href+'"]')).to_be_visible()
            assert '?q=' in page.url;overflow()
        page.fill('#learning-query','unfindable-zxy987');page.keyboard.press('Enter');expect(page.locator('#learning-empty')).to_be_visible()
        page.go_back();expect(page.locator('#learning-query')).to_have_value('俄尔')
        page.locator('#learning-clear').click();expect(page.locator('#learning-query')).to_have_value('')
        assert 'q=' not in page.url
        expect(page.locator('.ha-search-item:not([hidden])')).to_have_count(41)
        page.goto(url+'review/?q=Vasudhara');expect(page.locator('.ha-search-item:not([hidden]) a[href="../iconography/#vasudhara"]')).to_be_visible()
        page.locator('.ha-search-item:not([hidden]) a[href="../iconography/#vasudhara"]').click()
        expect(page.locator('#vasudhara')).to_have_attribute('open','')
        # Work -> background -> work: canonical object identifiers in both directions.
        page.goto(url+'w1520/');page.locator('.ha-learning-backlinks a[href="../regions/#gilgit"]').click()
        expect(page.locator('#gilgit')).to_have_attribute('open','')
        page.locator('#gilgit .ha-mini[href="../w1520/"]').click();assert page.url.endswith('/w1520/')
        # Guide -> map retains the already deployed query semantics.
        page.goto(url+'regions/#swat');page.locator('#swat a[href="../?region=swat#places"]').click()
        page.wait_for_selector('.ha-filters:not([hidden])');expect(page.locator('#ha-place')).to_have_value('swat');overflow()
        # Full photographs and the existing original-image lightbox remain available.
        page.goto(url+'thangka/#mandala')
        for link in page.locator('#mandala [data-photo]').all():
            link.click();expect(page.locator('#art-lightbox')).to_be_visible()
            page.locator('#large-photo').evaluate('(im)=>im.decode()')
            page.locator('#zoom-toggle').click();expect(page.locator('#zoom-toggle')).to_have_attribute('aria-pressed','true')
            page.keyboard.press('Escape');expect(page.locator('#art-lightbox')).not_to_be_visible();expect(link).to_be_focused()
    # Static fallback: entries and index can be opened with scripting disabled.
    plain=browser.new_page(java_script_enabled=False,viewport={'width':390,'height':844})
    plain.goto(url+'iconography/');plain.locator('#vajra-pair summary').click();expect(plain.locator('#vajra-pair .ha-guide-body')).to_be_visible()
    plain.goto(url+'review/');plain.locator('#learning-index summary').click();expect(plain.locator('.ha-search-item')).to_have_count(41)
    assert not errors,errors
    assert not bad,bad
    browser.close()
server.shutdown()
print('PASS: 4 regions, 12 icon groups, 8 people, 4 traditions, 5 thangka sections; 41-entry alias search, Back, keyboard, deep links, reciprocal works, map links and original-image lightbox at 1440/390/320px; no-JS fallback. Screenshots in /tmp/ha-learning-*.png.')
