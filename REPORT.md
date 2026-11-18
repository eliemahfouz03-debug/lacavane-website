# La Cavane — website domain migration & Android app update: technical report

Date: 18 November 2026. Scope: make the La Cavane website reachable at **https://www.lacavane.com** without the `rayhaddad99.chatgpt.site` address, and update the Android app accordingly.

## 1. What was found

| Question | Finding | How it was checked |
|---|---|---|
| How does the app open the website? | A single setting, `config.website` in `src/content.js`, used by two buttons: *About → Open the main website* and the stop sheets' *Main website*. Both call Android's `Linking.openURL`, i.e. they hand the address to the phone's browser. There is **no WebView** and no other reference to the old address in the app. | Source of the 3.x app (`grep` across source, docs, download page). |
| What is the current host? | **ChatGPT Sites** (OpenAI). The address pattern `<site>.<username>.chatgpt.site` is the default URL ChatGPT Sites assigns. | OpenAI help article *Creating and using ChatGPT Sites*, read on 18 Nov 2026. |
| Is the site reachable today? | **No, not publicly.** The address answers HTTP **401** with a page titled *"Sign in required — Log in to access — Continue with ChatGPT"*. Its audience is therefore not "Anyone on the Internet"; visitors coming from the app without a ChatGPT account are blocked. | Opened in the browser pane on 18 Nov 2026. |
| Can ChatGPT Sites take a custom domain? | **Yes, where the feature is available on the owner's plan** (Plus/Pro/Business; off by default or unavailable in some workspaces). The *Site owner* opens Settings → *Add domain*, enters the apex or subdomain, adds the DNS records ChatGPT shows (including a verification TXT), and refreshes the status. Only the `rayhaddad99` account can do this; I have no access to it, and the DNS values are generated per Site. | OpenAI help article, section *Use a custom domain*. |
| Can the source be exported? | Yes — and it already was: `03_Website_Reference/dist/index.html` in the redesign package is the owner's self-contained export (one HTML file, 924 KB, styles, script and three WebP images inlined, EN/FR). Its README describes it as the *"actual promotional website source"*. | Package `START_HERE.txt` and `03_Website_Reference/README.md`. |
| Is lacavane.com available? | **Not registered** on 18 Nov 2026: the .com registry's RDAP service returns *not found* for `lacavane.com` while returning records for registered names. Availability and price are only final at a registrar's checkout. | `https://rdap.verisign.com/com/v1/domain/lacavane.com` → 404; control query `example.com` → 200. |

## 2. Decision

The original hosting *can* technically carry the domain, but (a) only Ray can configure it, (b) it depends on his plan, and (c) the site is currently behind a ChatGPT login, which no domain change fixes. To deliver something that works and that can be verified, the site was deployed from the owner's own export on **GitHub Pages** (free, public repository, custom domain with automatic HTTPS), with the domain pre-configured. The ChatGPT-Sites route is documented in `DEPLOY.md §2` as an alternative: if Ray connects the domain there instead, the app needs no change because it only knows `https://www.lacavane.com`.

This is a *redeployment of the original file*, not a rebuild: no text, style, image, script or behaviour was changed. The only additions are in `<head>` — a canonical link, Open Graph tags and a favicon.

## 3. What was changed

### Website (repository `lacavane-website`)
- `index.html` — the export, plus `<head>` additions above. `404.html` is a copy so unknown paths still show the site.
- `CNAME` (`www.lacavane.com`), `.nojekyll`, `robots.txt`, `sitemap.xml`.
- `vercel.json`, `netlify.toml` — ready configuration for the alternative hosts named in the brief.
- `DEPLOY.md` — domain purchase, DNS records (table), HTTPS enforcement, the ChatGPT-Sites alternative.
- `tests/verify.py` — the Playwright checks behind `VERIFICATION.md`.

### Android app (repository `la-cavane-visitor-app`, version 3.2.0, versionCode 5)
- `src/content.js`: `website: 'https://www.lacavane.com'`.
- `tests/native.test.mjs`: new test — the config holds the new address and nothing visitor-facing (`src/`, `App.js`, `distribution/`, `app.json`) contains `chatgpt.site`; version test updated.
- `CHANGES.md`, `README.md`, `TESTING.md`, `RELEASE_STATUS.md` updated; About-screen render regenerated.
- Built and signed by the existing GitHub Actions workflow with the same CI key as 3.0.0/3.1.0, so the APK **installs as an update** over those versions (same application ID `com.lacavane.visitor`). The original 1.x/2.x key was never available, so 3.x remains a separate install next to a 2.x app.

## 4. What the owner still has to do (and costs)

1. **Register `lacavane.com`** at a registrar (≈ US$10–15/year — the only cost). Confirm the ICANN e-mail.
2. **Add the DNS records** in `DEPLOY.md §1` (www CNAME → `eliemahfouz03-debug.github.io`; apex A/AAAA → GitHub Pages).
3. In the repository's *Settings → Pages*, confirm the custom domain and tick **Enforce HTTPS** once the certificate is issued.

Until step 2 propagates, the site is reachable at the temporary address `https://eliemahfouz03-debug.github.io/lacavane-website/` and the app's website button opens a browser error page.

## 5. Original vs. final — honest comparison

| Aspect | Original (ChatGPT Site) | Final (GitHub Pages) |
|---|---|---|
| Content, design, languages, interactions | The owner's export (`dist/index.html`) | The same file, byte-identical outside `<head>` |
| Reachability | 401 sign-in wall for anyone not logged into ChatGPT | Public; HTTPS by GitHub/Let's Encrypt |
| Address | `la-cavane-experience-ray.rayhaddad99.chatgpt.site` | `www.lacavane.com` (after DNS); `lacavane.com` redirects to it |
| Backend | None (estimator and "demo receipt" run in the browser; nothing is sent) | Identical |
| Editing | Chat with ChatGPT, publish | Edit `index.html` (or `src/app.js`) and push |
| Limits | Plan-dependent hosting usage | GitHub Pages soft limits: 1 GB site, 100 GB/month bandwidth — far above this 1 MB site |

**Limit of the comparison:** the live ChatGPT Site could not be opened for a side-by-side check because it requires a ChatGPT sign-in; the export in the package (early November 2026) is the reference. If the Site was edited after the export, those edits are not in the replica. Signing into ChatGPT in the browser pane would allow a direct comparison — offered, not done.

## 6. Verification

See `VERIFICATION.md` for the itemised results (37 automated checks on desktop and mobile, live HTTPS checks on the temporary address, app tests and build verification).
