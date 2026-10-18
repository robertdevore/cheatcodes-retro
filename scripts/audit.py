from pathlib import Path
from bs4 import BeautifulSoup
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
from urllib.parse import urljoin,urlparse
import csv,json,hashlib,datetime
A=Path('seo-audit/2026-10-18'); OLD='https://cheatcodes-retro-2001.robertdevore.chatgpt.site'; NEW='https://cheatcodes.robertdevore.com'; NA='NOT AVAILABLE — DATA ACCESS REQUIRED'
def write(name,rows):
 if not rows:return
 with (A/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def probe(u,agent='Mozilla/5.0'):
 try:
  with urlopen(Request(u,headers={'User-Agent':agent}),timeout=15) as r:return r.status,r.url,dict(r.headers)
 except HTTPError as e:return e.code,e.url,dict(e.headers)
 except Exception as e:return 'UNAVAILABLE',u,{'error':str(e)}
allrows=[];links=[];media=[];summaries={}
for phase,root,origin,local in [('baseline',A/'raw/before/dist',OLD,'http://localhost:8766'),('after',Path('dist'),NEW,'http://localhost:8765')]:
 rows=[];sitemap=(root/'sitemap.xml').read_text();production=probe(origin+'/')
 (A/f'raw/{phase}-production.json').write_text(json.dumps(production,indent=2))
 for file in sorted(root.rglob('*.html')):
  rel=str(file.relative_to(root));route='/' if rel=='index.html' else '/'+rel.removesuffix('index.html');url=origin+route;s=BeautifulSoup(file.read_text(),'html.parser');meta=s.find('meta',attrs={'name':'description'});can=s.find('link',rel='canonical');robot=s.find('meta',attrs={'name':'robots'});schemas=[]
  for j in s.find_all('script',type='application/ld+json'):
   try:schemas.append(json.loads(j.string)['@type'])
   except Exception:schemas.append('PARSE ERROR')
  broken=0;internal=external=0
  for link in s.find_all('a',href=True):
   href=link['href'];dest=urljoin(url,href);isext=urlparse(dest).netloc!=urlparse(url).netloc
   status='not requested';verification='same-page UI action' if href.startswith('#') else 'file checked';action='none'
   if not isext and not href.startswith('#'):
    path=root/urlparse(dest).path.lstrip('/');path=path/'index.html' if path.is_dir() else path
    if not path.exists():broken+=1;status=404;action='fix destination'
    else:status=200
   if isext:external+=1
   else:internal+=1
   links.append(dict(phase=phase,source_url=url,destination_url=dest,anchor_text=link.get_text(' ',strip=True) or link.get('aria-label',''),link_context='navigation/content/footer',http_status=status,final_url=dest,chain_length=0,verification=verification,rel=' '.join(link.get('rel',[])),recommended_action=action))
  title=s.title.get_text() if s.title else '';desc=meta.get('content','') if meta else '';canonical=can.get('href','') if can else '';h1=' | '.join(x.get_text(' ',strip=True) for x in s.find_all('h1'));indexable=rel!='404.html' and not (robot and 'noindex' in robot.get('content',''))
  row=dict(phase=phase,url=url,source_file=rel,page_type='homepage' if rel=='index.html' else 'generated utility',local_status=probe(local+route)[0],production_status=production[0] if rel=='index.html' else 'not requested',indexable=indexable,robots_directives=robot.get('content','') if robot else 'default',canonical=canonical,canonical_target_status=probe(canonical)[0] if canonical else '',title=title,title_length=len(title),meta_description=desc,description_length=len(desc),h1=h1,heading_structure=' '.join(h.name for h in s.find_all(['h1','h2','h3'])),word_count=len(s.get_text(' ',strip=True).split()),lang=s.html.get('lang','') if s.html else '',published_date='',modified_date='',author='Robert DeVore' if phase=='after' and rel=='index.html' else '',breadcrumbs='not applicable',schema_types=';'.join(schemas),internal_inbound_links='N/A single page',internal_outbound_links=internal,external_outbound_links=external,broken_internal_links=broken,broken_external_links='indeterminate pending live probes',image_count=len(s.find_all('img')),missing_alt=sum(not x.has_attr('alt') for x in s.find_all('img')),missing_dimensions=sum(not(x.has_attr('width') and x.has_attr('height')) for x in s.find_all('img')),page_depth=0 if rel=='index.html' else 'utility',orphan=rel not in ['index.html','404.html'],sitemap_included=url in sitemap,duplicate_title=False,duplicate_description=False,content_hash=hashlib.sha256(file.read_bytes()).hexdigest(),issues='missing canonical' if indexable and not canonical else '')
  rows.append(row)
 summary={'html_files':len(rows),'sitemap_urls':sitemap.count('<loc>'),'indexable_artifact_pages':sum(r['indexable'] for r in rows),'missing_canonicals':sum(r['indexable'] and not r['canonical'] for r in rows),'missing_descriptions':sum(r['indexable'] and not r['meta_description'] for r in rows),'missing_h1':sum(r['indexable'] and not r['h1'] for r in rows),'schema_pages':sum(bool(r['schema_types']) for r in rows),'broken_internal_links':sum(r['broken_internal_links'] for r in rows),'source_hero_bytes':sum(f.stat().st_size for f in (root/'assets').glob('reference.*')),'field_data':NA}
 summaries[phase]=summary;(A/f'{phase}-summary.json').write_text(json.dumps(summary,indent=2));write(phase+'.csv',rows);allrows+=rows
write('site-inventory.csv',allrows);write('internal-links.csv',[r for r in links if urlparse(r['destination_url']).netloc==urlparse(r['source_url']).netloc]);external=[]
for r in links:
 if urlparse(r['destination_url']).netloc==urlparse(r['source_url']).netloc:continue
 code,final,headers=probe(r['destination_url']);r.update(http_status=code,final_url=final,verification='verified' if code==200 else 'blocked/indeterminate' if code in [401,403,405,429,'UNAVAILABLE'] else 'response observed');external.append(r)
write('external-links.csv',external);write('broken-links.csv',[r for r in links if r['recommended_action']!='none'] or [{'status':'No broken internal file destinations; modal fragments are UI actions, not document routes.'}])
for name,fields in [('metadata-audit.csv',['phase','url','title','meta_description','h1','canonical','lang']),('schema-audit.csv',['phase','url','schema_types']),('indexability.csv',['phase','url','indexable','robots_directives','canonical','sitemap_included']),('content-audit.csv',['phase','url','page_type','word_count','h1','author','issues'])]:write(name,[{k:r[k] for k in fields} for r in allrows])
crawlers=[]
for agent in ['Googlebot','bingbot','OAI-SearchBot','ChatGPT-User','GPTBot']:
 for route in ['/','/robots.txt','/sitemap.xml']:
  code,final,headers=probe(NEW+route,agent);crawlers.append({'user_agent':agent,'url':NEW+route,'status':code,'final_url':final,'limitation':'User-agent probe only; not verified provider IP. Robots wildcard policy preserved.'})
write('crawler-access.csv',crawlers)
write('crawlability.csv',[{'url':NEW+'/robots.txt','policy':Path('dist/robots.txt').read_text(),'training_policy':'unchanged wildcard allow','note':'llms.txt experimental, not a ranking requirement'}])
redirects=[]
for url in [NEW+'/',NEW+'/?ref=audit','http://cheatcodes.robertdevore.com/','https://robertdevore.github.io/cheatcodes-retro/',NEW+'/missing-audit-route',NEW+'/robots.txt',NEW+'/sitemap.xml',NEW+'/blog/']:
 code,final,headers=probe(url);redirects.append({'phase':'after','source_url':url,'source_variant':'production','http_status':code,'target_url':final,'chain_length':'not enumerated','final_status':code,'canonical_target':NEW+'/','query_preserved':'ref=audit' in final if '?' in url else 'N/A','verification':'live urllib probe','issues':headers.get('error','')})
write('redirects.csv',redirects)
write('image-audit.csv',[{'phase':ph,'asset':'reference.jpeg' if ph=='baseline' else 'inline SVG and CSS','bytes':summaries[ph]['source_hero_bytes'],'use':'Historical sprite baseline' if ph=='baseline' else 'Editable SVG paths and CSS geometry; no raster assets','dimensions':'830x790 reference' if ph=='baseline' else 'SVG viewBox and CSS layout','loading':'inline document' if ph=='after' else 'CSS discovery'} for ph in summaries])
write('keyword-map.csv',[{'url':NEW+'/','topic':'2001 CheatCodes.com website design recreation','intent':'Explore historical gaming website design','primary':'CheatCodes 2001 recreation','secondary':'Kujo SSG SiteKit example','action':'Identify recreation truthfully; do not target active cheat-code database searches'}])
write('search-rankings.csv',[{'query':q,'search_engine':'Google/Bing','date':'2026-10-18','evidence':NA,'limitations':'No authorized rank or console dataset'} for q in ['CheatCodes 2001 recreation','Kujo SSG SiteKit example']])
write('ai-search-benchmark.csv',[{'question':q,'platform':'ChatGPT/Google AI/Bing','date':'2026-10-18','evidence':NA,'limitations':'No measured provider answer sessions; do not infer citations'} for q in ['Where can I view a recreation of the 2001 CheatCodes homepage?','Is the giveaway on cheatcodes.robertdevore.com active?','Where is the Kujo SSG source for this recreation?']])
print(json.dumps(summaries,indent=2))
