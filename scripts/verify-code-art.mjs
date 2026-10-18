import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
const html = fs.readFileSync('dist/index.html', 'utf8');
assert(!/<(?:img|image)\b/i.test(html), 'The page must use inline vector artwork, not raster images.');
assert(!/reference\.(?:jpeg|webp|png)|data:image\/(?:png|jpeg|webp)/i.test(html), 'Reference screenshot found in rendered page.');
function checkTree(directory) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const file = path.join(directory, entry.name);
    if (entry.isDirectory()) checkTree(file);
    else assert(!/\.(?:png|jpe?g|webp|gif|avif)$/i.test(file), `Unexpected raster production asset: ${file}`);
  }
}
checkTree('dist');
assert((html.match(/<svg\b/g) || []).length >= 10, 'Console illustrations missing.');
assert((html.match(/<h1\b/g) || []).length === 1, 'Expected one page heading.');
console.log('PASS: editable inline SVG and CSS artwork; no raster production assets.');
