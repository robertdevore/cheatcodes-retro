# Methodology — 2026-10-18
Scope: the CheatCodes 2001 design recreation and its migration from an owner-private ChatGPT Site to public GitHub Pages at cheatcodes.robertdevore.com. The user authorized implementation, hosting, and DNS migration; the user set Cloudflare DNS directly.

Before editing, preserved dist and SHA256 under raw/before and built the unchanged Kujo source successfully. Crawl compares every generated HTML file plus sitemap, HTML destinations and assets. Baseline: four HTML artifacts, including empty blog and redirect utility. Final: one substantive homepage plus noindex 404. The empty blog and feed were intentionally removed.

Claims are separated into source evidence, generated evidence, HTTP probes, and lab measurements. The legacy live origin requires sign-in; it cannot supply an organic-search baseline. Automated user-agent requests test reachable endpoints, not verified Google/OpenAI network identity. Root RobertDeVore.com and its www host are outside this subdomain migration; their routing was not modified.

The site is a historical visual recreation, not an active gaming database. Competitive ranking and AI answer comparisons would be misleading without measured data; benchmark questions are saved for later measurement. No invented expertise, promotions, author dates, rankings, backlinks, or rich-result eligibility claims were added. WebPage schema reflects the visible provenance notice.

Python audit requires BeautifulSoup4. Browser QA uses the Codex browser; Lighthouse CLI supplies saved diagnostics, while PageSpeed web results are separately recorded. No automated test can certify accessibility or permanent 100 performance scores. Internal heuristic readiness scores were deliberately not assigned because search-platform and authority evidence is unavailable.
