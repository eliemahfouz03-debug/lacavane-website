# Verification checklist — actual results

Legend: ✅ passed · ⏳ pending (needs the public repository / the domain) · ❌ failed · — not possible from this environment

## A. Website (the file served from this repository)

Run: `python3 tests/verify.py http://localhost:8080/ review` on 18 Nov 2026, Chrome via Playwright, viewports 1440×900 (desktop) and 390×844 (mobile, touch). **37 / 37 checks passed.** Screenshots in `review/`.

| # | Check | Desktop | Mobile |
|---|---|---|---|
| 1 | Page loads, HTTP 200 | ✅ | ✅ |
| 2 | Title "La Cavane — A day among the vines" | ✅ | ✅ |
| 3 | Hero image decodes (2200 px wide) | ✅ | ✅ |
| 4 | All seven sections present (experiences, table, estate, events, boutique, visit, faq) | ✅ | ✅ |
| 5 | Hamburger menu opens | n/a | ✅ |
| 6 | Estimator: 2 adults, meal + tasting each → **$79.92** | ✅ | ✅ |
| 7 | EN → FR keeps the planner values; total shown as "79,92 $US"; h1 "Ralentir. Entre les vignes." | ✅ | ✅ |
| 8 | FR → EN | ✅ | ✅ |
| 9 | Tastings > adults rejected ("Tastings cannot exceed the number of adults.", total "—") | ✅ | ✅ |
| 10 | Event, 30 guests → **$1,398.60**, deposit **$419.58** | ✅ | ✅ |
| 11 | Event, 20 guests → "Quote required" + tailored-quote notice | ✅ | ✅ |
| 12 | Estate-plan dialog opens with a decoded image | ✅ | ✅ |
| 13 | Floor-plan dialog opens with a decoded image | ✅ | ✅ |
| 14 | Experience dialog opens | ✅ | ✅ |
| 15 | Submit is blocked until the 18+ box is ticked (HTML validation) | ✅ | ✅ |
| 16 | Demo receipt opens; text says "Nothing sent. No booking or payment." and carries $79.92 | ✅ | ✅ |
| 17 | No console errors | ✅ | ✅ |
| 18 | No failed network requests (everything is inlined) | ✅ | ✅ |
| 19 | No `chatgpt.site` / `openai` anywhere in the served page | ✅ | ✅ |

Other: `index.html` is the owner's export with three `<head>` additions only (canonical, Open Graph, favicon) — verified by diff; the only external link in the page is the Google Maps search for Khenchara.

## B. Hosting and HTTPS

| Check | Result |
|---|---|
| Live address `https://eliemahfouz03-debug.github.io/lacavane-website/` serves the site over HTTPS | ✅ 18 Nov 2026, 21:15 Beirut — opened in Chrome: `location.protocol` = `https:`, `isSecureContext` = true, title "La Cavane — A day among the vines" |
| Served file identical to the repository file | ✅ SHA-256 of the served bytes (fetched in the browser, 928,605 bytes) = `18b3a301…2a12` = SHA-256 of `index.html`; body byte-identical to the owner's export (only `<head>` differs) |
| Functional checks on the live address (run in the page) | ✅ seven sections present · 2 adults meal+tasting **$79.92** · event 30 → **$1,398.60**, deposit **$419.58** · event 20 → "Quote required" · FR switch: lang `fr`, "79,92 $US", h1 "Ralentir. Entre les vignes." · plan dialog image 834 px, floor-plan image 990 px · no `chatgpt`/`openai` in the served HTML |
| Desktop and mobile layouts on the live address | ✅ same file as the local run (hash-identical); screenshots in `review/` are from that run |
| Custom domain in Settings → Pages | ⏳ deliberately **not set yet** (GitHub would redirect the github.io address to the unregistered domain); `CNAME.pending` holds the value — see DEPLOY.md |
| `https://www.lacavane.com` with a valid certificate | ⏳ needs the domain registered, the DNS records in DEPLOY.md, then `CNAME.pending` → `CNAME` |
| `lacavane.com` → `www.lacavane.com` redirect | ⏳ same |
| Domain availability | ✅ `lacavane.com` not registered on 18 Nov 2026 (registry RDAP: not found; control `example.com`: found) |

## C. Original site

| Check | Result |
|---|---|
| `https://la-cavane-experience-ray.rayhaddad99.chatgpt.site/` | ❌ HTTP 401, "Sign in required — Continue with ChatGPT" (18 Nov 2026) — not publicly reachable |
| Side-by-side comparison with the replica | — not possible without a ChatGPT sign-in; the replica is the owner's export from the redesign package |
| Hosting platform identified | ✅ ChatGPT Sites (OpenAI); custom domains supported where available, owner-only |

## D. Android app 3.2.0 (versionCode 5) and 3.2.1 (versionCode 6)

3.2.1 adds `src/website.js`: the website buttons check that `https://www.lacavane.com` answers (HEAD, 3.5 s) and otherwise open the same site at `https://eliemahfouz03-debug.github.io/lacavane-website/`; with no connection at all they show a message.

| Check (3.2.1) | Result |
|---|---|
| Fallback behaviour, web build with the primary host unreachable | ✅ opens `https://eliemahfouz03-debug.github.io/lacavane-website/` (requests seen: primary HEAD → fallback HEAD → fallback GET) |
| Primary host reachable | ✅ opens `https://www.lacavane.com/` (primary HEAD → GET) |
| Compiled bundle | ✅ contains both addresses once each, `chatgpt.site` 0 times |
| APK identity / signature | ✅ `com.lacavane.visitor`, versionCode 6, 3.2.1; v2, certificate `93de3b21…bd9d` (update over 3.0–3.2.0) |
| SHA-256 | `d9e2bb7590ede24004be645ef7089fb6a36e8cbc0d0cd7bee4b31de88a53920c` (matches CI) |
| Tests | ✅ 23 / 23 |


| Check | Result |
|---|---|
| Old address in source, docs, download page | ✅ none (`grep`), enforced by a new test |
| `config.website === 'https://www.lacavane.com'` | ✅ test |
| Unit tests (`node --test`) | ✅ 23 / 23 |
| About screen shows "Open the main website" (web render `review/web-renders/32-about.png`) | ✅ |
| Compiled bundle inside the APK contains `https://www.lacavane.com` and **0** occurrences of `chatgpt.site` | ✅ (strings extracted from `assets/index.android.bundle`) |
| APK identity: `com.lacavane.visitor`, versionCode 5, versionName 3.2.0 | ✅ `aapt2 dump badging` (CI) |
| Signature: v2, certificate SHA-256 `93de3b21…bd9d` (same as 3.0.0 / 3.1.0 → installs as update) | ✅ `apksigner verify` (CI) |
| SHA-256 of `La-Cavane-Visitor.apk` | `db417e1c8dee7711a07e10514389fe7908960b6281ce242290e00d5350210b35` (matches CI `SHA256SUMS.txt`) |
| Tapping the website button on a phone | — no Android device/emulator here; the button hands the URL to the system browser, which will show an error until DNS is live |
| Original 1.x/2.x signing key | — never available; 3.x installs next to a 2.x app, not over it |
