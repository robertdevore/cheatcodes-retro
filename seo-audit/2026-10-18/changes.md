# Changes

- Increased native dialog width to the site's 830px canvas with safe viewport margins and bounded scrollable height.
- Applied silver/navy chrome theme to SiteKit buttons, focus rings, form controls and native scrollbars; kept dialogs outside the scaled desktop canvas.
- Added mobile reflow with legible text and larger touch controls, preserving desktop artwork.
- Added canonical, Open Graph, Twitter metadata, favicon, preload, visible provenance and truthful WebPage JSON-LD.
- Inlined 18,583 bytes of used/minified SiteKit plus theme CSS instead of loading the complete stylesheet and font. Converted the original JPEG sprite to WebP (150,732 → 128,792 bytes) while retaining the reference source.
- Removed unused blog, blog alias and feed; sitemap contains exactly the canonical homepage. Added correct noindex 404 and useful experimental llms.txt.
- Added locked build dependencies, patched selector-parser dependency, zero-vulnerability npm audit, source-license preservation, reproducible finalization and GitHub Pages workflow.
- Added validated Howl manifest, real Kujo example and generated social SVG, HTML, Markdown and gallery; these review artifacts are outside production dist.
