# La Cavane — public website

The promotional website of **La Cavane — Vineyard and Wine Experience Center**, a university entrepreneurship project (Lebanese University, Faculty of Engineering – Branch 2, Roumieh, 2026–2027) for a proposed vineyard, Lebanese restaurant and boutique in Khenchara, Metn.

- Live address once the domain is connected: **https://www.lacavane.com**
- Temporary address: https://eliemahfouz03-debug.github.io/lacavane-website/
- Previous address (ChatGPT Sites, sign-in required): `la-cavane-experience-ray.rayhaddad99.chatgpt.site` — replaced by this deployment.

## What is in the repository

| File | Purpose |
|---|---|
| `index.html` | The whole site: styles, script, three embedded images (WebP data URIs), both languages (EN/FR). This is the owner's own export of the ChatGPT Site (`03_Website_Reference/dist/index.html` in the redesign package), unchanged except for the `<head>` additions listed below. |
| `src/app.js` | The readable interaction script, as shipped with the export. Edit it, then paste it back into the inline `<script>` of `index.html`. |
| `404.html` | Copy of the site so that unknown paths still show it (GitHub Pages serves this file for 404s). |
| `CNAME` | `www.lacavane.com` — tells GitHub Pages which domain serves the site. |
| `.nojekyll`, `robots.txt`, `sitemap.xml` | Hosting hygiene. |
| `vercel.json`, `netlify.toml` | Equivalent configuration if the site is moved to Vercel or Netlify. |
| `DEPLOY.md` | Domain registration, DNS records, HTTPS, the ChatGPT-Sites alternative. |
| `tests/verify.py` | Playwright checks used for the verification record (`VERIFICATION.md`). |

## Changes made to the original file

Only inside `<head>`: a canonical link to `https://www.lacavane.com/`, Open Graph title/description/url/site name, and a 64 px favicon (the La Cavane bottle-and-vine mark used by the Android app). No text, style, image, script or behaviour was changed. The site has no backend: the booking estimator and the "demo receipt" run entirely in the browser and transmit nothing, exactly as before.

## Running locally

Open `index.html` in a browser, or `python3 -m http.server 8080` in this folder and visit http://localhost:8080/.

## Licence / content

Content and imagery belong to the La Cavane project team (Charbel El Hachem, Ray Haddad, Elie Mahfouz). Estate imagery, menus and product illustrations are conceptual, as the site itself states.
