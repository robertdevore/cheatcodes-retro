import fs from 'node:fs';import {PurgeCSS} from 'purgecss';import CleanCSS from 'clean-css';
const result=await new PurgeCSS().purge({content:['dist/index.html','assets/app.js'],css:['assets/sitekit/sitekit.css'],safelist:['sk-card','sk-button','chrome-button'],fontFace:true});
const css=new CleanCSS({level:1}).minify(result[0].css+'\n'+fs.readFileSync('assets/style.css','utf8')).styles;
let html=fs.readFileSync('dist/index.html','utf8').replace('<!-- CRITICAL_CSS -->','<style>'+css+'</style>');fs.writeFileSync('dist/index.html',html);
for(const path of ['dist/blog','dist/blog.html','dist/feed','dist/assets/sitekit'])fs.rmSync(path,{recursive:true,force:true});
fs.writeFileSync('dist/CNAME','cheatcodes.robertdevore.com\n');fs.writeFileSync('dist/.nojekyll','');
fs.writeFileSync('dist/sitemap.xml','<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://cheatcodes.robertdevore.com/</loc></url></urlset>');
fs.writeFileSync('dist/404.html','<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Page not found</title><style>body{background:#282d43;color:#fff;font:18px Arial;padding:10vw}a{color:#c5d9ff}</style><h1>Page not found</h1><p><a href="/">Return to the CheatCodes recreation</a></p></html>');
console.log('Finalized GitHub Pages artifact; inline CSS bytes:',Buffer.byteLength(css));

fs.writeFileSync('dist/llms.txt','# CheatCodes.com 2001 recreation\n\n> An independent historical design recreation by Robert DeVore, built with Kujo SSG and SiteKit. Not the original service. Promotions and accounts are demonstrations.\n\n## Pages\n- [Homepage](https://cheatcodes.robertdevore.com/): Interactive 2001 website design recreation.\n- [Source](https://github.com/robertdevore/cheatcodes-retro): Implementation and build instructions.\n');
