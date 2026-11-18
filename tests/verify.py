"""Verification of the La Cavane website.

Usage:  python3 tests/verify.py <base-url> [out-dir]
e.g.    python3 tests/verify.py http://localhost:8080/ review
        python3 tests/verify.py https://www.lacavane.com/ review-live

Checks (each printed as PASS/FAIL):
  - HTTPS (for https URLs: no certificate error, status 200)
  - desktop (1440×900) and mobile (390×844) screenshots, top of page and visit planner
  - no console errors, no failed network requests
  - the three embedded images decode (naturalWidth > 0)
  - language toggle switches to French and back, keeping the planner values
  - estimator: 2 adults, meal + tasting each  -> $79.92 (the export's own documented figure)
  - estimator: event, 30 guests              -> $1,398.60 total, $419.58 deposit (30 %)
  - event, 20 guests                         -> individual-quote notice, no total
  - tastings > adults                        -> validation message
  - estate plan and floor-plan dialogs open with an image; experience dialog opens
  - demo receipt dialog opens on submit (date 2028-06-15) and says nothing is sent
  - page source contains no reference to chatgpt.site / openai
"""
import asyncio, sys, os, json, re
from playwright.async_api import async_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8080/'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'review'
os.makedirs(OUT, exist_ok=True)
results = []
def rec(name, ok, detail=''):
    results.append((name, ok, detail)); print(('PASS ' if ok else 'FAIL ') + name + (' — ' + detail if detail else ''))

async def main():
    async with async_playwright() as p:
        exe = '/usr/bin/google-chrome' if os.path.exists('/usr/bin/google-chrome') else None
        b = await p.chromium.launch(executable_path=exe, args=['--no-sandbox'])
        for label, vp, mobile in [('desktop', {'width': 1440, 'height': 900}, False), ('mobile', {'width': 390, 'height': 844}, True)]:
            ctx = await b.new_context(viewport=vp, device_scale_factor=2 if mobile else 1, is_mobile=mobile, has_touch=mobile, ignore_https_errors=False)
            pg = await ctx.new_page()
            errs, failed = [], []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
            pg.on('requestfailed', lambda r: failed.append(r.url))
            resp = await pg.goto(BASE, wait_until='load')
            rec(f'{label}: page loads', resp is not None and resp.status == 200, f'status {resp.status if resp else "none"}' + (' over HTTPS' if BASE.startswith('https') else ''))
            await pg.wait_for_timeout(800)
            await pg.screenshot(path=f'{OUT}/{label}-top.png')
            title = await pg.title()
            rec(f'{label}: title', title == 'La Cavane — A day among the vines', title)
            imgs = await pg.evaluate("[...document.images].map(i => [i.currentSrc.slice(0,30), i.naturalWidth])")
            rec(f'{label}: hero image decodes (plan/floor images are checked in their dialogs)', len(imgs) >= 1 and all(w > 0 for _, w in imgs), f'{len(imgs)} image(s) in the page, widths {[w for _, w in imgs]}')
            # navigation anchors exist
            secs = await pg.evaluate("['experiences','table','estate','events','boutique','visit','faq'].every(id => !!document.getElementById(id))")
            rec(f'{label}: all seven sections present', secs)
            if mobile:
                await pg.click('#menuToggle'); await pg.wait_for_timeout(300)
                opened = await pg.evaluate("document.getElementById('navlinks').classList.contains('open')")
                rec('mobile: hamburger menu opens', opened)
                await pg.screenshot(path=f'{OUT}/mobile-menu.png')
                await pg.click('#menuToggle'); await pg.wait_for_timeout(200)
            # planner: 2 adults, tasting + meal each
            await pg.evaluate("document.getElementById('visit').scrollIntoView()")
            await pg.fill('#adults', '2'); await pg.fill('#children', '0'); await pg.fill('#tastings', '2'); await pg.fill('#meals', '2'); await pg.fill('#bottles', '0'); await pg.fill('#baskets', '0')
            await pg.wait_for_timeout(200)
            total = await pg.inner_text('#total')
            rec(f'{label}: estimate 2 adults meal+tasting = $79.92', total.strip() == '$79.92', total.strip())
            await pg.screenshot(path=f'{OUT}/{label}-planner.png')
            # language toggle keeps values
            await pg.click('#language'); await pg.wait_for_timeout(300)
            fr_lang = await pg.evaluate("document.documentElement.lang")
            fr_total = await pg.inner_text('#total')
            adults_kept = await pg.input_value('#adults')
            fr_heading = await pg.inner_text('#home h1') if await pg.locator('#home h1').count() else ''
            rec(f'{label}: French switch keeps selections', fr_lang == 'fr' and adults_kept == '2' and ('79,92' in fr_total), f'lang={fr_lang} total={fr_total.strip()} h1={fr_heading[:40]!r}')
            await pg.screenshot(path=f'{OUT}/{label}-french.png')
            await pg.click('#language'); await pg.wait_for_timeout(300)
            rec(f'{label}: back to English', (await pg.evaluate("document.documentElement.lang")) == 'en')
            # validation: tastings > adults
            await pg.fill('#tastings', '3'); await pg.wait_for_timeout(200)
            err = await pg.inner_text('#quoteNotice'); err_total = await pg.inner_text('#total')
            rec(f'{label}: tastings > adults is rejected', 'exceed' in err.lower() and err_total.strip() == '—', f'{err.strip()} | total {err_total.strip()}')
            await pg.fill('#tastings', '2')
            # event mode
            await pg.click('#eventTab'); await pg.wait_for_timeout(200)
            await pg.fill('#eventGuests', '30'); await pg.wait_for_timeout(200)
            ev_total = await pg.inner_text('#total'); dep = await pg.inner_text('#deposit')
            rec(f'{label}: event 30 guests = $1,398.60 / deposit $419.58', ev_total.strip() == '$1,398.60' and '419.58' in dep, f'{ev_total.strip()} | {dep.strip()[:60]}')
            await pg.fill('#eventGuests', '20'); await pg.wait_for_timeout(200)
            notice = await pg.inner_text('#quoteNotice'); q_total = await pg.inner_text('#total')
            rec(f'{label}: event 20 guests needs individual quote', 'quote' in notice.lower() and q_total.strip() == 'Quote required', f'notice={notice.strip()[:60]!r} total={q_total.strip()!r}')
            await pg.fill('#eventGuests', '30')
            # dialogs
            for btn, nm in [('#showPlan', 'estate plan dialog'), ('#showFloor', 'floor plan dialog')]:
                await pg.evaluate(f"document.querySelector('{btn}').scrollIntoView()")
                await pg.click(btn); await pg.wait_for_timeout(400)
                open_ = await pg.evaluate("document.getElementById('detailDialog').open")
                has_img = await pg.evaluate("!!document.querySelector('#detailDialog img') && document.querySelector('#detailDialog img').naturalWidth > 0")
                rec(f'{label}: {nm} opens with image', open_ and has_img)
                if nm.startswith('estate'): await pg.screenshot(path=f'{OUT}/{label}-plan-dialog.png')
                await pg.keyboard.press('Escape'); await pg.wait_for_timeout(200)
            exp = pg.locator('[data-experience]').first
            await exp.scroll_into_view_if_needed(); await exp.click(); await pg.wait_for_timeout(300)
            rec(f'{label}: experience dialog opens', await pg.evaluate("document.getElementById('detailDialog').open"))
            await pg.keyboard.press('Escape')
            # receipt
            await pg.click('#dayTab'); await pg.fill('#date', '2028-06-15'); await pg.fill('#name', 'Test Visitor'); await pg.fill('#email', 'test@example.com')
            # the 18+ confirmation is required by the form whenever tastings > 0 (HTML validation blocks submit otherwise)
            blocked = await pg.evaluate("document.getElementById('visitForm').checkValidity()")
            rec(f'{label}: submit blocked until the 18+ box is ticked', blocked is False)
            await pg.check('#age')
            await pg.evaluate("document.getElementById('visitForm').requestSubmit()"); await pg.wait_for_timeout(500)
            r_open = await pg.evaluate("document.getElementById('receiptDialog').open")
            r_text = await pg.inner_text('#receiptText') if r_open else ''
            rec(f'{label}: demo receipt opens and says nothing is sent', r_open and 'Nothing sent' in r_text and '$79.92' in r_text, r_text.replace('\n', ' | ')[:120])
            if not mobile: await pg.screenshot(path=f'{OUT}/{label}-receipt.png')
            await pg.keyboard.press('Escape')
            rec(f'{label}: no console errors', not errs, '; '.join(errs)[:200])
            rec(f'{label}: no failed network requests', not failed, '; '.join(failed)[:200])
            html = await pg.content()
            rec(f'{label}: no chatgpt.site / openai in the page', 'chatgpt' not in html.lower() and 'openai' not in html.lower())
            await ctx.close()
        await b.close()
    ok = sum(1 for _, k, _ in results if k); print(f'\n{ok}/{len(results)} checks passed')
    json.dump([{'check': n, 'pass': k, 'detail': d} for n, k, d in results], open(f'{OUT}/results.json', 'w'), indent=1, ensure_ascii=False)
    sys.exit(0 if ok == len(results) else 1)

asyncio.run(main())
