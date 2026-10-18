# CheatCodes.com 2001 recreation

Live: https://cheatcodes.robertdevore.com/
Source: https://github.com/robertdevore/cheatcodes-retro

## Build and publish

Requires Kujo SSG's compatible Kujo runtime (the vendored build.kujo identifies SSG 1.2.0), Node 22+, and npm.

```sh
npm ci
npm run build
npm run check
npm run howl
```

Commit the generated `dist/` with source changes, then push `main`. GitHub Actions publishes exactly the checked-in `dist/`. `scripts/finalize.mjs` reduces SiteKit CSS to used selectors, inlines critical styles, removes empty generated blog/feed routes, writes the canonical sitemap and CNAME, and preserves the SiteKit license. SiteKit 1.1.0 source and licenses remain under `assets/sitekit/`. Dependency versions are locked; `npm audit` passed with zero vulnerabilities.

## Design and behavior

The user-provided 830×790 reference supplies chrome and console artwork through CSS sprites. Main news copy is HTML. Desktop preserves the reference layout; mobile reflows text and controls for readable copy and usable tap targets. Dialogs render outside the scaled canvas, up to 830px wide with viewport margins, chrome controls, and themed native scrollbars.

Historical promotions, accounts, newsletter and game database are demonstrations. The newsletter neither stores nor sends email. This is an independent recreation, not the original CheatCodes service.

## Hosting

GitHub Pages uses the custom domain `cheatcodes.robertdevore.com`; Cloudflare DNS CNAME `cheatcodes` points to `robertdevore.github.io`, DNS only. HTTPS enforcement follows GitHub certificate provisioning. The old private ChatGPT Site is retained as a historical deployment, not the publishing target. Its `.openai/hosting.json` is legacy identity only.

## Evidence

`seo-audit/2026-10-18/` contains the immutable pre-change artifact, before/after crawl datasets, first-party guidance, performance receipts, and report. Reproduce the crawl with `python3 scripts/audit.py` (requires BeautifulSoup4 and local static servers on 8765 for dist and 8766 for the saved baseline). Do not overwrite original baseline files.

`howl.json`, `examples/recreation.kujo`, and generated `showcase/` contain the validated Howl card and share copy. Showcase artifacts are review materials, not extra indexable production pages.
