# Deploying www.lacavane.com

The site is one static HTML file (`index.html`, everything inlined). Any static host serves it. This repository is set up for **GitHub Pages** (free, custom domain, automatic HTTPS); `vercel.json` and `netlify.toml` are included if you prefer Vercel or Netlify.

## 0. Register the domain (one-time, paid)

`lacavane.com` was **not registered** on 18 November 2026 (checked against the .com registry's RDAP service: `https://rdap.verisign.com/com/v1/domain/lacavane.com` returns *not found*, whereas registered names return their record). Availability can change at any moment and some names are priced as "premium"; the registrar confirms the final price at checkout.

1. Pick a registrar that includes DNS management (for example Cloudflare Registrar, Namecheap, Porkbun, GoDaddy, or a Lebanese registrar). A standard `.com` costs roughly US$10–15 per year; nothing else in this setup costs money.
2. Buy `lacavane.com`. Use an e-mail address you can read: ICANN requires you to **confirm the registrant e-mail within 15 days**, otherwise the domain is suspended.
3. Open the domain's **DNS records** page. Delete any default "parking" A/CNAME records for `@` and `www`.

Nothing was purchased for you; do not buy until you are ready to run step 2 below.

## 1. Hosting on GitHub Pages (what this repository is configured for)

- Repository: `https://github.com/eliemahfouz03-debug/lacavane-website` (public — GitHub Pages is free only on public repositories).
- Branch `main`, folder `/` (root); `.nojekyll` disables Jekyll processing. Pages was enabled on 18 Nov 2026.
- Live address today: **`https://eliemahfouz03-debug.github.io/lacavane-website/`** (HTTPS). The Android app uses it automatically as long as `www.lacavane.com` does not answer.
- **Why `CNAME.pending` and not `CNAME`:** as soon as a custom domain is set, GitHub redirects the github.io address to that domain. With the domain not registered yet that would send every visitor — and the app's fallback — to a dead address, so the domain is deliberately *not* configured until the DNS records below exist. Connecting it later is one step (see "Then, in GitHub").

### DNS records to add at the registrar

| Host / name | Type | Value | Purpose |
|---|---|---|---|
| `www` | CNAME | `eliemahfouz03-debug.github.io` | serves www.lacavane.com |
| `@` (apex) | A | `185.199.108.153` | lacavane.com → redirects to www |
| `@` | A | `185.199.109.153` | |
| `@` | A | `185.199.110.153` | |
| `@` | A | `185.199.111.153` | |
| `@` | AAAA | `2606:50c0:8000::153` | IPv6 (optional but recommended) |
| `@` | AAAA | `2606:50c0:8001::153` | |
| `@` | AAAA | `2606:50c0:8002::153` | |
| `@` | AAAA | `2606:50c0:8003::153` | |

These are GitHub's published Pages addresses; confirm them against *docs.github.com → Pages → Managing a custom domain* before saving, in case GitHub changes them. If the registrar is Cloudflare, set the records to **DNS only** (grey cloud), not proxied, so GitHub can issue the certificate.

### Then, in GitHub

1. Rename `CNAME.pending` to `CNAME` and push (or type `www.lacavane.com` in Repository → **Settings → Pages → Custom domain** and **Save** — GitHub then creates the same file). Source is already *Deploy from a branch*, `main`, `/ (root)`.
2. Wait for the "DNS check successful" message (minutes to an hour after the records propagate; up to 24–48 h worst case).
3. Tick **Enforce HTTPS** once it becomes available (GitHub obtains a Let's Encrypt certificate automatically).
4. Optional, recommended: your GitHub account → Settings → Pages → *Add a domain* → `lacavane.com`, and add the TXT record GitHub shows. This "verified domain" prevents anyone else from pointing it at a Pages site.

Result: `https://www.lacavane.com` serves the site; `http://lacavane.com`, `https://lacavane.com` and `http://www.lacavane.com` redirect to it.

### Updating the site

Edit `index.html` (or `src/app.js`, then paste the script back into `index.html` as the original author did), commit, push to `main`. GitHub Pages redeploys within about a minute.

## 2. Alternative A — keep the original ChatGPT Site and connect the domain there

The current host is **ChatGPT Sites** (OpenAI). Its help page states that, where custom domains are available, the *Site owner* can connect a domain from the Site's settings: **Settings → Add domain → enter the apex or subdomain → copy the DNS records (including a verification TXT record) into the registrar → refresh the domain status**. Only the owner of the Site (the `rayhaddad99` account) can do this, and the feature depends on that account's plan ("where available"; not in Enterprise workspaces at launch).

Two things to fix on that side if you choose this route:
1. The Site currently answers **HTTP 401 "Sign in required — Continue with ChatGPT"** to visitors who are not signed in to ChatGPT. In **Share → Who has access**, choose **Anyone on the Internet**; otherwise visitors arriving from the app will hit a login wall whatever the domain.
2. Both `lacavane.com` and `www.lacavane.com` have to be added (the help page says to plan for `www` as well). The DNS values are generated per Site, so they cannot be listed here.

If you take this route, point the DNS at the values ChatGPT Sites shows instead of the GitHub table above; the Android app needs no further change because it only knows `https://www.lacavane.com`.

## 3. Alternative B — Vercel / Netlify / Cloudflare Pages

Import this repository (no build step, output directory `/`). Add the domain in the dashboard and follow its DNS instructions (typically `www` CNAME → the platform host and `@` A/ALIAS → the platform's apex address). `vercel.json` and `netlify.toml` already set long-lived caching for the single file and a redirect from the apex to www where the platform supports it.

## 4. Checks after DNS

- `https://www.lacavane.com` loads with a valid padlock; `https://lacavane.com` redirects to it.
- The page title is "La Cavane — A day among the vines"; the language toggle works; the estimator shows totals.
- From the Android app (3.2.0 or later): About → *Open the main website* and any stop sheet → *Main website* open `https://www.lacavane.com` in the phone's browser.
