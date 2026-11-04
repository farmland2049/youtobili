#!/usr/bin/env python3
"""Standard-library-only, resumable metadata → candidate → confirmed-public pipeline."""
import argparse, collections, datetime, hashlib, html, http.cookiejar, json, os, re, time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse, parse_qs
from urllib.request import Request, build_opener, HTTPCookieProcessor

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'data/source'
WORK = ROOT / 'data/work'
STATES = {'confirmed', 'review', 'unmatched', 'invalid'}
LANG_RANK = {'official_zh': 0, 'sub_zh': 1, 'dub_zh': 2, 'official_original': 3, 'original': 4}

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(path, default=None):
    return json.loads(path.read_text()) if path.exists() else default

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    tmp.replace(path)

def corpus():
    rows = [json.loads(s) for s in (SOURCE / 'videos.jsonl').read_text().splitlines() if s.strip()]
    assert len({x['vid'] for x in rows}) == len(rows), 'duplicate source ID'
    return rows

def youtube_id(url):
    u = urlparse(url)
    if u.hostname in ('youtu.be', 'www.youtu.be'): return u.path.strip('/').split('/')[0]
    if u.hostname in ('youtube.com','www.youtube.com','m.youtube.com','youtube-nocookie.com','www.youtube-nocookie.com'):
        return parse_qs(u.query).get('v', [''])[0] or (u.path.split('/')[2] if re.match(r'^/(shorts|embed|live)/',u.path) else '')
    return ''

def norm(s): return re.sub(r'[^a-z0-9\u4e00-\u9fff]', '', s.lower())
def title_overlap(a, b):
    words = set(re.findall(r'[a-z0-9]{3,}', a.lower())) - {'the','and','with','for','what','how','part','lecture'}
    return len(words & set(re.findall(r'[a-z0-9]{3,}', b.lower()))) / max(1, len(words))

def identity_ids(text):
    return set(re.findall(r'(?:youtu\.be/|youtube\.com/(?:watch\?[^\s]*?v=|embed/|shorts/|live/))([A-Za-z0-9_-]{11})(?![A-Za-z0-9_-])', text))

class Blocked(Exception): pass
class ApiError(Exception): pass

class Client:
    def __init__(self, delay=1.3):
        self.delay = max(1.2, delay)
        self.last = 0
        self.opener = build_opener(HTTPCookieProcessor(http.cookiejar.CookieJar()))
        self.cache = WORK / 'http'
        self.cache.mkdir(parents=True, exist_ok=True)
    def get(self, url, refresh=False):
        file = self.cache / (hashlib.sha256(url.encode()).hexdigest() + '.json')
        cached = read(file)
        # Refresh availability after seven days. A cached error is never evidence.
        if cached and not refresh and time.time() - file.stat().st_mtime < 7*86400:
            return cached['body']
        time.sleep(max(0, self.delay - (time.monotonic() - self.last)))
        self.last = time.monotonic()
        req = Request(url, headers={'User-Agent':'Mozilla/5.0', 'Referer':'https://www.bilibili.com/'})
        try:
            with self.opener.open(req, timeout=25) as r: b = json.load(r)
        except HTTPError as e:
            if e.code in (401,403,412,429): raise Blocked(f'HTTP {e.code}: batch stopped') from None
            raise ApiError(f'HTTP {e.code}') from None
        except (URLError, TimeoutError, json.JSONDecodeError) as e:
            raise ApiError(type(e).__name__) from None
        if isinstance(b,dict) and b.get('code',0) in (-101,-111,-352,-412,-509):
            raise Blocked(f"API {b['code']}: authentication/risk control; batch stopped")
        if isinstance(b,dict) and b.get('code',0) not in (0,-404):
            raise ApiError(f"API {b.get('code')}")
        write(file, {'url':url,'fetched_at':now(),'body':b})
        return b

def import_legacy():
    rows = corpus(); known = {x['vid']:x for x in rows}
    lib = read(WORK/'library.json')
    if lib is None: lib = read(ROOT/'data/confirmed.json', {}).get('entries', {})
    legacy = read(WORK/'legacy.json')
    if legacy is None:
        import subprocess
        legacy = json.loads(subprocess.check_output(['git','show','65dfbd6e285e8f793f369b4107281cdc11ef6a03:data.json'], cwd=ROOT))
    orphan = []
    for x in legacy:
        vid = youtube_id(x.get('src_url',''))
        if vid not in known:
            orphan.append({'vid':vid,'bvid':x.get('bv'),'reason':'not in source corpus'})
            continue
        entry = lib.setdefault(vid, {'vid':vid,'status':'review','candidates':[]})
        if not any(c['bvid']==x['bv'] for c in entry['candidates']):
            entry['candidates'].append({'bvid':x['bv'],'status':'review','legacy_title':x['t'],
                'legacy_confidence':x.get('confidence'), 'origin':'legacy','reason':'legacy confidence is not approval'})
    write(WORK/'library.json',lib); write(WORK/'orphans.json',orphan)
    return lib

def lang_kind(title, owner, original):
    official = norm(owner) == norm(original) and bool(norm(original))
    # "官方" in a title alone does not prove account ownership.
    sub = bool(re.search(r'字幕|双语|中英|中字|中文翻译|汉化',title))
    dub = bool(re.search(r'配音|中配|中文讲解|中文配',title))
    return 'official_zh' if official and (sub or dub) else 'sub_zh' if sub else 'dub_zh' if dub else 'official_original' if official else 'original'

def assess(original, detail, page, duration):
    """Conservative auto approval: explicit original URL, full segment, no contradictions."""
    title = detail.get('title','')
    desc = detail.get('desc','')
    ids = identity_ids(desc)
    evidence = []
    flags = []
    pages = detail.get('pages',[])
    selected = next((p for p in pages if p.get('page') == page), None)
    if not selected: flags.append('missing segment')
    segment_title = selected.get('part','') if selected else ''
    actual = selected.get('duration',0) if selected else 0
    if original['vid'] in ids: evidence.append('explicit original URL in Bilibili description')
    else: flags.append('no explicit original URL; manual identity review required')
    a = set(re.findall(r'\b(?:19|20)\d{2}\b',original['title']))
    b = set(re.findall(r'\b(?:19|20)\d{2}\b',title+' '+segment_title))
    if a and b and not (a & b): flags.append('conflicting years')
    episode = lambda s: re.findall(r'(?:lecture|chapter|part|lesson|第)\s*(\d+)',s,re.I)
    oa,ba=episode(original['title']),episode(segment_title if len(pages)>1 else title)
    if oa and ba and oa != ba: flags.append('conflicting episode')
    if re.search(r'删减|片段|节选|精华|cut\s*version|highlights',title+' '+segment_title,re.I): flags.append('possibly abridged')
    if not duration: flags.append('original duration unavailable')
    elif abs(actual-duration)>max(60,0.08*duration): flags.append('duration outside tolerance')
    if len(pages)>1:
        if title_overlap(original['title'],segment_title)<0.65 or len(ids)>1:
            flags.append('collection segment identity requires review')
    elif len(ids)>1: flags.append('description links multiple originals')
    if actual<=0: flags.append('missing segment duration')
    return {'status':'review' if flags else 'confirmed','evidence':evidence,'flags':flags,
        'reason':'; '.join(flags) if flags else 'explicit source URL, segment and duration verified'}

def evaluate(client, original, c):
    detail = client.get('https://api.bilibili.com/x/web-interface/view?'+urlencode({'bvid':c['bvid']}))
    if detail.get('code') == -404:
        return {**c,'status':'invalid','reason':'view API explicitly returned -404','checked_at':now()}
    d = detail['data']
    meta = client.get('https://hackertube.org/api/video?'+urlencode({'vid':original['vid']}))
    metadata = meta.get('video', meta) if isinstance(meta,dict) else {}
    duration = (metadata or {}).get('duration_s')
    pages = d.get('pages',[])
    # A review decision can explicitly select a segment; never infer a collection from total duration.
    page = c.get('page')
    if not page:
        ranked = sorted(pages,key=lambda p:title_overlap(original['title'],p.get('part','')),reverse=True)
        page = ranked[0]['page'] if ranked else 1
    result = assess(original,d,page,duration)
    p = next((p for p in pages if p['page']==page),{})
    kind = lang_kind(d['title'],d['owner']['name'],original.get('channel',''))
    fresh = {**c,**result,'page':page,'title':d['title'],'up':d['owner']['name'],
        'duration':p.get('duration',0),'original_duration':duration,'cid':p.get('cid'),
        'segment_title':p.get('part',''),'page_count':len(pages), 'kind':kind,
        'views':d.get('stat',{}).get('view',0),'pic':d.get('pic','').replace('http://','https://'),
        'checked_at':now(),'availability':'available'}
    fresh.pop('error',None)
    if c.get('manual_review') and c.get('status')=='confirmed':
        # Explicit reviews survive rechecks only if availability and segment ID are unchanged.
        if c.get('cid')==fresh['cid'] and not any(f in fresh['flags'] for f in ['conflicting years','conflicting episode','possibly abridged','missing segment','missing segment duration']):
            fresh['status']='confirmed';fresh['reason']='manual content review; availability rechecked'
    return fresh

def entry_status(candidates):
    if any(c['status']=='confirmed' for c in candidates): return 'confirmed'
    if any(c['status']=='review' for c in candidates): return 'review'
    return 'invalid' if candidates else 'unmatched'

def report(lib, batch=None):
    rows=corpus(); statuses=collections.Counter(e['status'] for e in lib.values())
    if batch is None: batch=read(ROOT/'reports/summary.json',{}).get('batch')
    if batch:
        attempted=set(batch['originals'])|{e['vid'] for e in batch['errors']}
        batch['attempted']=len(attempted);batch['unattempted']=batch['selected']-len(attempted)
        batch['statuses']=dict(collections.Counter(lib[vid]['status'] for vid in attempted if vid in lib))
    done=[e for e in lib.values() if e.get('completed_at')]
    confirmed=sum(e['status']=='confirmed' for e in lib.values())
    summary={'updated_at':now(),'corpus':len(rows),'processed':len(done),'confirmed':confirmed,
        'coverage':confirmed/len(rows),'processed_match_rate':sum(e['status']=='confirmed' for e in done)/len(done) if done else 0,
        'statuses':dict(statuses),'not_processed':len(rows)-len(done),
        'candidates':sum(len(e['candidates']) for e in lib.values()),'batch':batch if batch is not None else read(ROOT/'reports/summary.json',{}).get('batch'),
        'review_reasons':dict(collections.Counter(c.get('reason','') for e in lib.values() for c in e['candidates'] if c['status']!='confirmed'))}
    write(ROOT/'reports/summary.json',summary)
    text=f"# 匹配进展\n\n更新时间：{summary['updated_at']}\n\n- 原片库：{len(rows)}\n- 完成处理：{len(done)}\n- 已确认原片：{confirmed}\n- 全库覆盖率：{summary['coverage']:.2%}\n- 已处理原片匹配率：{summary['processed_match_rate']:.2%}\n- 状态：{dict(statuses)}\n\n"
    if summary['batch']: text+='## 最近批次\n\n```json\n'+json.dumps(summary['batch'],ensure_ascii=False,indent=2)+'\n```\n'
    (ROOT/'reports/STATUS.md').write_text(text)
    return summary

def run_match(args):
    if not 1 <= args.limit <= 50: raise ValueError('batch limit must be 1–50')
    client=Client(args.delay);lib=import_legacy(); rows=corpus()
    ordered=sorted(rows,key=lambda x:(not bool(lib.get(x['vid'],{}).get('candidates')), -x.get('score',0)))
    if args.existing_only:ordered=[x for x in ordered if lib.get(x['vid'],{}).get('candidates')]
    if not args.recheck:ordered=[x for x in ordered if not lib.get(x['vid'],{}).get('completed_at')]
    selected=ordered[:args.limit]
    batch={'id':datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ'),'selected':len(selected),'completed':0,'errors':[],'stopped':False,'originals':[]}
    for original in selected:
        vid=original['vid'];entry=lib.setdefault(vid,{'vid':vid,'status':'unmatched','candidates':[]})
        entry.pop('last_error',None)
        try:
            if not args.existing_only and not entry.get('searched_at'):
                queries=[original['title'],original.get('channel','')+' '+original['title']]
                for q in dict.fromkeys(queries):
                    response=client.get('https://api.bilibili.com/x/web-interface/search/type?'+urlencode({'search_type':'video','keyword':q,'page':1}))
                    for item in response.get('data',{}).get('result',[])[:5]:
                        bv=item.get('bvid','')
                        if re.fullmatch(r'BV[A-Za-z0-9]{10}',bv) and not any(c['bvid']==bv for c in entry['candidates']):
                            entry['candidates'].append({'bvid':bv,'status':'review','origin':'search','query':q})
                entry['searched_at']=now()
            # Persist every candidate: interruption resumes without discarding successful checks.
            for i,c in enumerate(entry['candidates']):
                if not args.recheck and c.get('checked_at') and not c.get('error'):continue
                try:
                    entry['candidates'][i]=evaluate(client,original,c)
                except ApiError as e:
                    entry['candidates'][i]={**c,'status':'review','error':str(e),'reason':'request failed; availability unknown'}
                    raise
                write(WORK/'library.json',lib)
            entry['status']=entry_status(entry['candidates']);entry['completed_at']=now()
            batch['completed']+=1;batch['originals'].append(vid)
            print(f"{batch['completed']}/{len(selected)} {vid}: {entry['status']}",flush=True)
        except (Blocked,ApiError) as e:
            entry['last_error']=str(e);entry['status']=entry_status(entry['candidates']) if entry['candidates'] else 'review'
            batch['errors'].append({'vid':vid,'reason':str(e)})
            if isinstance(e,Blocked):batch['stopped']=True
            print(f'{vid}: {e}',flush=True)
        finally:
            write(WORK/'library.json',lib);write(WORK/'batches'/f"{batch['id']}.json",batch);report(lib,batch)
        if batch['stopped']:break
    attempted=set(batch['originals'])|{e['vid'] for e in batch['errors']}
    batch['attempted']=len(attempted);batch['unattempted']=len(selected)-len(attempted)
    selected_entries=[lib[vid] for vid in attempted]
    batch['statuses']=dict(collections.Counter(e['status'] for e in selected_entries))
    batch['candidate_count']=sum(len(e['candidates']) for e in selected_entries)
    write(WORK/'batches'/f"{batch['id']}.json",batch);report(lib,batch)
    return 2 if batch['stopped'] or batch['errors'] else 0

def build():
    lib=read(WORK/'library.json')
    if lib is None: lib=read(ROOT/'data/confirmed.json',{}).get('entries',{})
    videos=[]
    for o in corpus():
        e=lib.get(o['vid'],{});versions=[]
        for c in e.get('candidates',[]):
            if c['status']!='confirmed' or c.get('availability')!='available':continue
            if not c.get('evidence') and not c.get('manual_review'):continue
            versions.append({k:c[k] for k in ['bvid','page','cid','title','up','duration','kind','views','pic','checked_at']})
        versions.sort(key=lambda c:(LANG_RANK[c['kind']],-c['views'],c['bvid'],c['page']))
        if not versions:continue
        videos.append({'id':o['vid'],'title':o['title'],'author':o.get('channel',''),
            'source_url':'https://www.youtube.com/watch?v='+o['vid'], 'summary':o.get('summary',''),
            'why':o.get('why_hn',''),'score':o.get('score',0),'tags':o.get('tags',[]),
            'categories':[c['id'] for c in o.get('categories',[])], 'versions':versions})
    # One BVID page cannot represent two different originals without explicit manual adjudication.
    owners=collections.defaultdict(list)
    for v in videos:
        for c in v['versions']:owners[(c['bvid'],c['page'])].append(v['id'])
    conflicts={key for key,ids in owners.items() if len(set(ids))>1}
    for v in videos:v['versions']=[c for c in v['versions'] if (c['bvid'],c['page']) not in conflicts]
    videos=[v for v in videos if v['versions']]
    summary=report(lib)
    summary['confirmed']=len(videos);summary['coverage']=len(videos)/summary['corpus']
    summary['processed_match_rate']=sum(v['id'] in lib and bool(lib[v['id']].get('completed_at')) for v in videos)/max(1,summary['processed'])
    summary['conflicting_segments']=len(conflicts)
    taxonomy=read(SOURCE/'taxonomy.json')['areas'];labels=read(ROOT/'web/labels.json',{})
    active={c for v in videos for c in v['categories']}
    areas=[]
    for area in taxonomy:
        cats=[{'id':c['id'],'name':labels.get(c['id'],c['name']),'original_name':c['name']} for c in area['categories'] if c['id'] in active]
        if cats:areas.append({'id':area['id'],'name':labels.get(area['id'],area['name']),'categories':cats})
    # Legacy BVID hashes and localStorage migrate to a single original. Prefer a confirmed mapping.
    legacy={}
    visible={v['id'] for v in videos}
    for vid,e in lib.items():
        for c in e['candidates']:
            if c['bvid'] not in legacy or vid in visible:legacy[c['bvid']]=vid
    public={'schema_version':1,'built_at':now(),'stats':{k:summary[k] for k in ['corpus','processed','confirmed','coverage','processed_match_rate']},'areas':areas,'videos':videos,'legacy':legacy}
    write(ROOT/'data.json',public)
    # Keep a minimal, reproducible approval ledger. HTTP caches and pending candidates remain local.
    ledger={vid:{'vid':vid,'status':e['status'],'completed_at':e.get('completed_at'),
        'candidates':[{k:v for k,v in c.items() if k not in {'legacy_title','legacy_confidence','query','origin'}} for c in e['candidates'] if c['status']=='confirmed']} for vid,e in lib.items()}
    write(ROOT/'data/confirmed.json',{'updated_at':now(),'entries':ledger})
    for filename in ['index.html','app.js','style.css']:(ROOT/filename).write_bytes((ROOT/'web'/filename).read_bytes())
    write(ROOT/'reports/publication.json',{'built_at':public['built_at'],'source_generated':read(SOURCE/'manifest.json')['generated'],'stats':public['stats'],'conflicting_segments':len(conflicts),'data_sha256':hashlib.sha256((ROOT/'data.json').read_bytes()).hexdigest()})
    print(json.dumps(public['stats'],ensure_ascii=False))

def inspect(args):
    lib=import_legacy();original=next(o for o in corpus() if o['vid']==args.vid)
    e=lib.setdefault(args.vid,{'vid':args.vid,'status':'review','candidates':[]})
    c=next((c for c in e['candidates'] if c['bvid']==args.bvid),None)
    if c is None:
        c={'bvid':args.bvid,'status':'review','origin':'manual lead'};e['candidates'].append(c)
    if args.page:c['page']=args.page
    result=evaluate(Client(),original,c)
    e['candidates'][e['candidates'].index(c)]=result;e['status']=entry_status(e['candidates'])
    write(WORK/'library.json',lib);report(lib);print(json.dumps(result,ensure_ascii=False,indent=2))

def review(args):
    lib=read(WORK/'library.json',{});e=lib[args.vid]
    c=next(c for c in e['candidates'] if c['bvid']==args.bvid)
    if args.decision=='confirmed':
        if not args.evidence or not args.page:raise ValueError('approval requires --evidence and --page')
        if c.get('availability')!='available' or c.get('page')!=args.page:raise ValueError('check selected segment availability first')
        if set(c.get('flags',[])) & {'conflicting years','conflicting episode','possibly abridged','missing segment','missing segment duration'}:raise ValueError('resolve content contradictions before approval')
        c['manual_review']={'at':now(),'evidence':args.evidence};c['evidence']=[args.evidence]
    c['status']=args.decision;e['status']=entry_status(e['candidates'])
    write(WORK/'library.json',lib);report(lib)

def check():
    d=read(ROOT/'data.json');assert d['schema_version']==1
    ids=set();segments=set();known={c['id'] for a in read(SOURCE/'taxonomy.json')['areas'] for c in a['categories']}
    for v in d['videos']:
        assert re.fullmatch(r'[A-Za-z0-9_-]{11}',v['id']) and v['id'] not in ids;ids.add(v['id'])
        assert v['versions'] and set(v['categories'])<=known
        for c in v['versions']:
            assert re.fullmatch(r'BV[A-Za-z0-9]{10}',c['bvid'])
            assert c['duration']>0 and c['page']>=1 and c['cid']
            assert (c['bvid'],c['page']) not in segments;segments.add((c['bvid'],c['page']))
    assert len(ids)==d['stats']['confirmed']
    public=(ROOT/'data.json').read_text()+(ROOT/'index.html').read_text()+(ROOT/'app.js').read_text()
    for forbidden in ['/Users/','/workspace/','source_file','legacy_confidence','SESSDATA','bili_jct']:assert forbidden not in public
    assert 'no-referrer' in (ROOT/'index.html').read_text()
    print(f'PASS: {len(ids)} originals, {len(segments)} verified segments; no internal paths or credentials')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);subs=parser.add_subparsers(dest='cmd',required=True)
    subs.add_parser('import');subs.add_parser('build');subs.add_parser('check');subs.add_parser('report');subs.add_parser('export-review')
    p=subs.add_parser('match');p.add_argument('--limit',type=int,default=50);p.add_argument('--delay',type=float,default=1.3);p.add_argument('--existing-only',action='store_true');p.add_argument('--recheck',action='store_true')
    p=subs.add_parser('inspect');p.add_argument('vid');p.add_argument('bvid');p.add_argument('--page',type=int)
    p=subs.add_parser('review');p.add_argument('vid');p.add_argument('bvid');p.add_argument('decision',choices=['confirmed','review','invalid']);p.add_argument('--page',type=int);p.add_argument('--evidence')
    a=parser.parse_args()
    if a.cmd=='import': print(len(import_legacy()),'legacy originals imported')
    elif a.cmd=='match':raise SystemExit(run_match(a))
    elif a.cmd=='build':build()
    elif a.cmd=='check':check()
    elif a.cmd=='review':review(a)
    elif a.cmd=='inspect':inspect(a)
    elif a.cmd=='export-review':
        lib=read(WORK/'library.json',{})
        queue=[{'vid':vid,**c} for vid,e in lib.items() for c in e['candidates'] if c['status']=='review']
        write(WORK/'review-queue.json',queue);print(len(queue),'candidates exported to local review queue')
    else:print(json.dumps(report(read(WORK/'library.json',{})),ensure_ascii=False,indent=2))
