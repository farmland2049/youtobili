#!/usr/bin/env python3
"""Standard-library-only, resumable metadata → candidate → confirmed-public pipeline."""
import argparse, collections, datetime, hashlib, html, http.cookiejar, http.client, json, os, re, time
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
    return set(re.findall(r'(?<![A-Za-z0-9_.-])(?:https?://)?(?:www\.|m\.)?(?:youtu\.be/|youtube(?:-nocookie)?\.com/(?:watch\?[^\s]*?v=|embed/|shorts/|live/))([A-Za-z0-9_-]{11})(?![A-Za-z0-9_-])', text))

def segment_identity_ids(title):
    # Common upload filenames preserve the exact original ID in brackets or at the end.
    ids=set(re.findall(r'\[([A-Za-z0-9_-]{11})\]',title))
    ids.update(re.findall(r'(?:^|[-\s])([A-Za-z0-9_-]{11})$',title))
    return ids

def primary_identity_ids(text):
    """Ignore recommended resources; accept an explicitly labeled YouTube ID too."""
    head = re.split(r'其他资源|参考资料|参考链接|相关阅读|related\s+(?:videos|resources)|other\s+resources', html.unescape(text), maxsplit=1, flags=re.I)[0]
    ids = identity_ids(head)
    ids.update(re.findall(r'(?im)^\s*(?:youtube(?:\s+(?:id|视频))?|原片(?:ID)?|原视频ID)\s*[:：]\s*([A-Za-z0-9_-]{11})(?![A-Za-z0-9_-])', head))
    return ids

def segment_source_ids(detail, segment):
    ids=segment_identity_ids(segment.get('part',''))
    desc=detail.get('desc','');part=segment.get('part','').strip()
    # Explicit P numbers refer to Bilibili pages even when the part title has no P prefix.
    page_blocks=list(re.finditer(r'(?im)^\s*P\s*(\d+)\s*[:：]',desc))
    for i,h in enumerate(page_blocks):
        if int(h.group(1))==segment.get('page'):
            end=page_blocks[i+1].start() if i+1<len(page_blocks) else len(desc)
            ids.update(primary_identity_ids(desc[h.end():end]))
    headings=list(re.finditer(r'(?im)^\s*(上篇|下篇|P\s*\d+|第\s*\d+\s*[集章课])\s*[:：]\s*$',desc))
    for i,h in enumerate(headings):
        label=re.sub(r'\s+','',h.group(1)).lower()
        normalized=re.sub(r'\s+','',part).lower()
        if normalized.startswith(label) and not normalized[len(label):len(label)+1].isdigit():
            end=headings[i+1].start() if i+1<len(headings) else len(desc)
            ids.update(primary_identity_ids(desc[h.end():end]))
    return ids

class Blocked(Exception): pass
class ApiError(Exception): pass

class Client:
    def __init__(self, delay=1.3):
        self.delay = max(1.2, delay)
        self.last = 0
        self.cookie_jar = http.cookiejar.CookieJar()
        self.opener = build_opener(HTTPCookieProcessor(self.cookie_jar))
        self.guest_ready = False
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        self.cache = WORK / 'http'
        self.cache.mkdir(parents=True, exist_ok=True)
    @staticmethod
    def is_search(url):
        parsed=urlparse(url)
        return parsed.hostname=='api.bilibili.com' and '/search/' in parsed.path
    def wait_turn(self, minimum=None):
        interval=max(self.delay,minimum or 0)
        time.sleep(max(0, interval - (time.monotonic() - self.last)))
        self.last=time.monotonic()
    def ensure_guest(self):
        if self.guest_ready:return
        self.wait_turn()
        req=Request('https://www.bilibili.com/',headers={'User-Agent':self.user_agent,'Referer':'https://www.bilibili.com/'})
        try:
            with self.opener.open(req,timeout=25) as response:response.read()
        except HTTPError as e:
            if e.code in (401,403,412,429):raise Blocked(f'Guest initialization HTTP {e.code}: batch stopped') from None
            raise ApiError(f'Guest initialization HTTP {e.code}') from None
        except (URLError,TimeoutError,ConnectionError,http.client.HTTPException) as e:raise ApiError('Guest initialization '+type(e).__name__) from None
        if not any(c.name=='buvid3' and (c.domain.lstrip('.')=='bilibili.com' or c.domain.endswith('.bilibili.com')) for c in self.cookie_jar):
            raise Blocked('Guest initialization did not supply buvid3; batch stopped')
        self.guest_ready=True
    def get(self, url, refresh=False):
        search=self.is_search(url)
        # Older anonymous searches sometimes returned irrelevant successes. Never reuse those.
        cache_input=('guest-search-v2:'+url) if search else url
        file = self.cache / (hashlib.sha256(cache_input.encode()).hexdigest() + '.json')
        cached = read(file)
        # Refresh availability after seven days. A cached error is never evidence.
        if cached and not refresh and time.time() - file.stat().st_mtime < 7*86400:
            return cached['body']
        if search:self.ensure_guest()
        self.wait_turn(3 if search else None)
        req = Request(url, headers={'User-Agent':self.user_agent, 'Referer':'https://search.bilibili.com/' if search else 'https://www.bilibili.com/'})
        try:
            with self.opener.open(req, timeout=25) as r: b = json.load(r)
        except HTTPError as e:
            if e.code in (401,403,412,429): raise Blocked(f'HTTP {e.code}: batch stopped') from None
            raise ApiError(f'HTTP {e.code}') from None
        except (URLError, TimeoutError, ConnectionError, http.client.HTTPException, json.JSONDecodeError) as e:
            raise ApiError(type(e).__name__) from None
        if isinstance(b,dict) and b.get('code',0) in (-101,-111,-352,-412,-509):
            raise Blocked(f"API {b['code']}: authentication/risk control; batch stopped")
        if isinstance(b,dict) and b.get('code',0) not in (0,-404):
            raise ApiError(f"API {b.get('code')}")
        write(file, {'url':url,'fetched_at':now(),'body':b,**({'search_session_version':2} if search else {})})
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

def lang_kind(title, owner, original, mid=None):
    account=read(ROOT/'data/official-channels.json',{}).get('accounts',{}).get(norm(original))
    # Neither matching names nor "官方" in a title prove creator ownership.
    official=bool(account and mid is not None and str(mid)==str(account['bilibili_mid']))
    sub = bool(re.search(r'双语|中英|中字|(?:中\s*[/／]\s*英|英\s*[/／]\s*中)(?:文)?\s*字幕|中文.{0,6}字幕|中文翻译|汉化|熟肉|精译',title))
    dub = bool(re.search(r'配音|中配|中文讲解|中文配|中文语音',title))
    return 'official_zh' if official and (sub or dub) else 'dub_zh' if dub else 'sub_zh' if sub else 'official_original' if official else 'original'

def content_years(title, segment_title=''):
    # Export and browser-recording timestamps describe the file, not the content.
    if re.fullmatch(r'成片-(?:19|20)\d{2}-\d{1,2}-\d{1,2} \d{1,2}:\d{2}:\d{2}', segment_title):
        segment_title = ''
    segment_title = re.sub(r'\s+-\s+个人\s+-\s+Microsoft Edge\s+(?:19|20)\d{2}-.*$', '', segment_title, flags=re.I)
    return set(re.findall(r'(?<![0-9A-Za-z_])(?:19|20)\d{2}(?![0-9A-Za-z_])', title+' '+segment_title))

def assess(original, detail, page, duration):
    """Conservative auto approval: explicit original URL, full segment, no contradictions."""
    title = detail.get('title','')
    desc = detail.get('desc','')
    ids = primary_identity_ids(desc)
    evidence = []
    flags = []
    pages = detail.get('pages',[])
    selected = next((p for p in pages if p.get('page') == page), None)
    if not selected: flags.append('missing segment')
    segment_title = selected.get('part','') if selected else ''
    actual = selected.get('duration',0) if selected else 0
    page_ids=segment_source_ids(detail,selected or {})
    page_identity=original['vid'] in page_ids and len(page_ids)==1
    if original['vid'] in ids: evidence.append('explicit original URL or labeled YouTube ID in Bilibili description')
    elif not page_identity: flags.append('no explicit original URL; manual identity review required')
    if page_identity: evidence.append('exact original YouTube ID explicitly associated with selected segment')
    a = content_years(original['title'])
    b = content_years(title, segment_title)
    if a and b and not (a & b): flags.append('conflicting years')
    episode = lambda s: re.findall(r'(?:lecture|chapter|part|lesson|第)\s*(\d+)',s,re.I)
    oa,ba=episode(original['title']),episode(segment_title if len(pages)>1 else title)
    if oa and ba and oa != ba: flags.append('conflicting episode')
    if re.search(r'删减|片段|节选|精华|cut\s*version|highlights',title+' '+segment_title,re.I): flags.append('possibly abridged')
    if re.search(r'AI\s*生成.{0,16}(?:衍生|二次创作)|AI\s*(?:翻唱|cover)|(?:翻唱|二创|remix)|MV\s*复刻', title+' '+segment_title, re.I) or re.search(r'(?:本音频|本视频|本作品).{0,12}AI\s*生成.{0,16}(?:衍生|二次创作)', desc, re.I):
        flags.append('derivative content requires review')
    if not duration: flags.append('original duration unavailable')
    elif abs(actual-duration)>max(60,0.08*duration): flags.append('duration outside tolerance')
    if len(pages)>1:
        if not page_identity:
            flags.append('collection segment identity requires review')
    elif len(ids)>1 and not page_identity: flags.append('description links multiple originals')
    if actual<=0: flags.append('missing segment duration')
    return {'status':'review' if flags else 'confirmed','evidence':evidence,'flags':flags,
        'reason':'; '.join(flags) if flags else 'explicit source URL, segment and duration verified'}

def evaluate(client, original, c):
    detail = client.get('https://api.bilibili.com/x/web-interface/view?'+urlencode({'bvid':c['bvid']}))
    if detail.get('code') == -404:
        return {**c,'status':'invalid','availability':'unavailable','reason':'view API explicitly returned -404','checked_at':now()}
    d = detail['data']
    meta = client.get('https://hackertube.org/api/video?'+urlencode({'vid':original['vid']}))
    metadata = meta.get('video', meta) if isinstance(meta,dict) else {}
    duration = (metadata or {}).get('duration_s')
    pages = d.get('pages',[])
    # A review decision can explicitly select a segment; never infer a collection from total duration.
    page = c.get('page')
    exact=[p['page'] for p in pages if segment_source_ids(d,p)=={original['vid']}]
    if len(exact)==1 and not c.get('page_locked') and not c.get('manual_review'):page=exact[0]
    if not page:
        ranked = sorted(pages,key=lambda p:title_overlap(original['title'],p.get('part','')),reverse=True)
        page = ranked[0]['page'] if ranked else 1
    result = assess(original,d,page,duration)
    p = next((p for p in pages if p['page']==page),{})
    kind = lang_kind(d['title'],d['owner']['name'],original.get('channel',''),d['owner'].get('mid'))
    fresh = {**c,**result,'page':page,'title':d['title'],'up':d['owner']['name'],
        'duration':p.get('duration',0),'original_duration':duration,'cid':p.get('cid'),'aid':d.get('aid'),
        'segment_title':p.get('part',''),'page_count':len(pages), 'kind':kind,
        'views':d.get('stat',{}).get('view',0),'pic':d.get('pic','').replace('http://','https://'),
        'checked_at':now(),'availability':'available'}
    fresh.pop('error',None)
    fresh.pop('duration_screened',None)
    fresh.pop('detail_deferred_after_match',None)
    if c.get('manual_review') and c.get('status')=='confirmed':
        # Explicit reviews survive rechecks only if availability and segment ID are unchanged.
        if c.get('cid')==fresh['cid'] and not any(f in fresh['flags'] for f in ['conflicting years','conflicting episode','possibly abridged','derivative content requires review','missing segment','missing segment duration']):
            fresh['status']='confirmed';fresh['reason']='manual content review; availability rechecked'
    if c.get('manual_rejection') and c.get('status')=='unmatched':
        if c.get('cid')==fresh.get('cid') and fresh.get('cid') and fresh.get('page_count')==1:
            fresh['status']='unmatched';fresh['reason']='manual content mismatch; availability rechecked'
            fresh['evidence']=[c['manual_rejection']['evidence']]
    if c.get('manual_review_hold') and c.get('status')=='review':
        # An automatic source-ID recheck cannot resolve a recorded content concern.
        fresh['status']='review'
        fresh['reason']=c['manual_review_hold']['reason']
        fresh['flags']=list(dict.fromkeys(fresh['flags']+['manual content review required']))
    return fresh

def entry_status(candidates):
    if any(c['status']=='confirmed' for c in candidates): return 'confirmed'
    if any(c['status']=='review' for c in candidates): return 'review'
    return 'invalid' if candidates and all(c['status']=='invalid' for c in candidates) else 'unmatched'

def report(lib, batch=None):
    rows=corpus(); statuses=collections.Counter(e['status'] for e in lib.values())
    if batch is None: batch=read(ROOT/'reports/summary.json',{}).get('batch')
    if batch and not batch.get('selected'):
        meaningful=[read(f,{}) for f in sorted((WORK/'batches').glob('*.json'))]
        batch=next((b for b in reversed(meaningful) if b.get('selected')),batch)
    if batch:
        attempted=set(batch['originals'])|{e['vid'] for e in batch['errors']}
        batch['attempted']=len(attempted);batch['unattempted']=batch['selected']-len(attempted)
        batch['statuses']=dict(collections.Counter(lib[vid]['status'] for vid in attempted if vid in lib))
    done=[e for e in lib.values() if e.get('completed_at')]
    confirmed=sum(e['status']=='confirmed' for e in lib.values())
    expansion_pending=sum(e['status']=='review' and (bool(e.get('last_error')) or ('search_result_limit' in e and e['search_result_limit']<20)) for e in lib.values())
    expanded_reviews=sum(e['status']=='review' and not e.get('last_error') and 'search_result_limit' in e and e['search_result_limit']>=20 for e in lib.values())
    metadata_missing=sum(e['status']=='review' and not e.get('last_error') and 'search_result_limit' not in e for e in lib.values())
    summary={'updated_at':now(),'corpus':len(rows),'processed':len(done),'confirmed':confirmed,
        'coverage':confirmed/len(rows),'processed_match_rate':sum(e['status']=='confirmed' for e in done)/len(done) if done else 0,
        'statuses':dict(statuses),'not_processed':len(rows)-len(done),
        'verification_batch':read(WORK/'lead-receipt.json'),
        'blocked_searches':[{'vid':vid,'reason':e['last_error']} for vid,e in lib.items() if e.get('last_error') and not e.get('completed_at')],
        'candidates':sum(len(e['candidates']) for e in lib.values()),'review_expansion_pending':expansion_pending,'expanded_reviews':expanded_reviews,'review_search_metadata_missing':metadata_missing,'batch':batch if batch is not None else read(ROOT/'reports/summary.json',{}).get('batch'),
        'candidate_statuses':dict(collections.Counter(c['status'] for e in lib.values() for c in e['candidates'])),
        'review_reasons':dict(collections.Counter(c.get('reason','') for e in lib.values() for c in e['candidates'] if c['status']=='review'))}
    write(ROOT/'reports/summary.json',summary)
    text=f"# 匹配进展\n\n更新时间：{summary['updated_at']}\n\n- 原片库：{len(rows)}\n- 完成处理：{len(done)}\n- 已确认原片：{confirmed}\n- 全库覆盖率：{summary['coverage']:.2%}\n- 已处理原片匹配率：{summary['processed_match_rate']:.2%}\n- 状态：{dict(statuses)}\n\n"
    text+=f"- 待审中尚需扩大候选检查：{expansion_pending}\n- 已扩大检查仍待审核：{expanded_reviews}\n- 待审中搜索元数据缺失（重建丢失，状态未知，需重新搜索）：{metadata_missing}\n\n"
    if summary['batch']: text+='## 最近批次\n\n```json\n'+json.dumps(summary['batch'],ensure_ascii=False,indent=2)+'\n```\n'
    if summary['verification_batch']:
        text+='\n## 最近公开线索核验\n\n```json\n'+json.dumps(summary['verification_batch'],ensure_ascii=False,indent=2)+'\n```\n'
    if summary['blocked_searches']:
        text+='\n搜索仍有受阻条目；保留断点，不自动反复请求。详情见 summary.json 的 blocked_searches。\n'
    (ROOT/'reports/STATUS.md').write_text(text)
    return summary

def search_duration(value):
    try:
        parts=[int(x) for x in str(value).strip().split(':')]
        if not 1<=len(parts)<=3 or any(x<0 for x in parts):return None
        if len(parts)>1 and parts[-1]>=60:return None
        return sum(x*60**i for i,x in enumerate(reversed(parts)))
    except (TypeError,ValueError):return None

def defer_short_candidate(original_duration,candidate_duration):
    return bool(original_duration and candidate_duration is not None and
                original_duration-candidate_duration>max(60,0.08*original_duration))

def search_queries(original):
    aliases=read(ROOT/'data/search-queries.json',{}).get(original['vid'])
    queries=aliases if aliases else [original['title'],original.get('channel','')+' '+original['title']]
    if not isinstance(queries,list) or not all(isinstance(q,str) and q.strip() for q in queries):
        raise ValueError('search query aliases must be a nonempty string list')
    return list(dict.fromkeys(q.strip() for q in queries))[:2]

def candidate_priority(candidate):
    hint=candidate.get('search_hint',{})
    return (LANG_RANK.get(candidate.get('kind',hint.get('kind','original')),4),
            not hint.get('identity',False),-candidate.get('views',hint.get('views',0)))

def run_match(args):
    if not 1 <= args.limit <= 50: raise ValueError('batch limit must be 1–50')
    primary_first=getattr(args,'primary_first',False)
    if primary_first and args.recheck:raise ValueError('primary-first cannot replace a full availability recheck')
    client=Client(args.delay);lib=import_legacy(); rows=corpus()
    excluded=set(getattr(args,'exclude_vid',[]) or [])
    if getattr(args,'vid',None):
        rows=[o for o in rows if o['vid']==args.vid]
        if not rows:raise ValueError('original ID not in corpus')
        if args.vid in excluded:raise ValueError('explicit original ID is excluded from this batch')
    if excluded:rows=[o for o in rows if o['vid'] not in excluded]
    ordered=sorted(rows,key=lambda x:(not bool(lib.get(x['vid'],{}).get('candidates')), -x.get('score',0)))
    if args.existing_only:ordered=[x for x in ordered if lib.get(x['vid'],{}).get('candidates')]
    if getattr(args,'expand_review',False):
        if args.existing_only or args.recheck:raise ValueError('expand-review cannot be combined with existing-only or recheck')
        # 元数据缺失条目（search_result_limit 缺失默认 0 < 20）因待审候选已随重建丢失，只能重新搜索，故保持选入
        ordered=[x for x in ordered if lib.get(x['vid'],{}).get('status')=='review' and (lib[x['vid']].get('search_result_limit',0)<20 or lib[x['vid']].get('last_error'))]
    elif not args.recheck:ordered=[x for x in ordered if not lib.get(x['vid'],{}).get('completed_at')]
    selected=ordered[:args.limit]
    if not selected:
        print('No pending candidate originals in this selection.');return 0
    batch={'id':datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ'),'selected':len(selected),'completed':0,'errors':[],'stopped':False,'originals':[]}
    batch.update(primary_first=primary_first,deferred_candidates=0,excluded_originals=sorted(excluded))
    for original in selected:
        vid=original['vid'];entry=lib.setdefault(vid,{'vid':vid,'status':'unmatched','candidates':[]})
        entry.pop('last_error',None)
        try:
            queries=search_queries(original) if not args.existing_only else []
            if not args.existing_only and (not entry.get('searched_at') or entry.get('search_session_version')!=2 or entry.get('search_queries')!=queries or entry.get('search_result_limit',0)<20):
                meta=client.get('https://hackertube.org/api/video?'+urlencode({'vid':vid}))
                source_duration=(meta.get('video',meta) or {}).get('duration_s') if isinstance(meta,dict) else None
                for q in dict.fromkeys(queries):
                    response=client.get('https://api.bilibili.com/x/web-interface/search/type?'+urlencode({'search_type':'video','keyword':q,'page':1}))
                    for item in response.get('data',{}).get('result',[])[:20]:
                        bv=item.get('bvid','')
                        if re.fullmatch(r'BV[A-Za-z0-9]{10}',bv) and not any(c['bvid']==bv for c in entry['candidates']):
                            candidate={'bvid':bv,'status':'review','origin':'search','query':q}
                            title=html.unescape(re.sub(r'<[^>]+>','',item.get('title') or ''))
                            snippet=html.unescape(re.sub(r'<[^>]+>','',item.get('description') or ''))
                            views=item.get('play',0)
                            candidate['search_hint']={'kind':lang_kind(title,item.get('author') or '',original.get('channel',''),item.get('mid')),
                                'identity':vid in primary_identity_ids(snippet),'views':views if isinstance(views,(int,float)) else 0}
                            duration=search_duration(item.get('duration'))
                            if defer_short_candidate(source_duration,duration):
                                candidate.update(duration_screened=True,search_duration=duration,reason='search duration shorter than original beyond tolerance; detail review deferred')
                            entry['candidates'].append(candidate)
                entry['searched_at']=now();entry['search_session_version']=2;entry['search_queries']=queries;entry['search_result_limit']=20
            # Persist every candidate: interruption resumes without discarding successful checks.
            if primary_first:entry['candidates'].sort(key=candidate_priority)
            for i,c in enumerate(entry['candidates']):
                if c.get('duration_screened') and not args.recheck:continue
                if not args.recheck and c.get('checked_at') and not c.get('error'):continue
                confirmed=[LANG_RANK[x['kind']] for x in entry['candidates'] if x['status']=='confirmed' and x.get('availability')=='available']
                if primary_first and confirmed and candidate_priority(c)[0]>=min(confirmed):
                    c['detail_deferred_after_match']=True
                    c.setdefault('reason','detail review deferred after primary identity confirmed')
                    batch['deferred_candidates']+=1
                    continue
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
        if batch['stopped'] or batch['errors']:break
    attempted=set(batch['originals'])|{e['vid'] for e in batch['errors']}
    batch['attempted']=len(attempted);batch['unattempted']=len(selected)-len(attempted)
    selected_entries=[lib[vid] for vid in attempted]
    batch['statuses']=dict(collections.Counter(e['status'] for e in selected_entries))
    batch['candidate_count']=sum(len(e['candidates']) for e in selected_entries)
    write(WORK/'batches'/f"{batch['id']}.json",batch);report(lib,batch)
    return 2 if batch['stopped'] or batch['errors'] else 0

def ledger_entry(e, vid=None):
    entry = {'vid': e.get('vid') or vid, 'status': e['status'], 'completed_at': e.get('completed_at'),
        'candidates': [{k: v for k, v in c.items() if k not in {'legacy_title', 'legacy_confidence', 'query', 'origin', 'search_hint', 'detail_deferred_after_match'}} for c in e.get('candidates', []) if c.get('status') == 'confirmed']}
    for k in ('searched_at', 'search_session_version', 'search_queries', 'search_result_limit', 'last_error'):
        if k in e and e[k] is not None:
            entry[k] = e[k]
    return entry

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
    # Legacy BVID hashes and localStorage migrate only through published versions.
    legacy={}
    for v in videos:
        for c in v['versions']:
            legacy.setdefault(c['bvid'],v['id'])
    public={'schema_version':1,'built_at':now(),'stats':{k:summary[k] for k in ['corpus','processed','confirmed','coverage','processed_match_rate']},'areas':areas,'videos':videos,'legacy':legacy}
    write(ROOT/'data.json',public)
    # Keep a minimal, reproducible approval ledger. HTTP caches and pending candidates remain local.
    ledger = {vid: ledger_entry(e, vid) for vid, e in lib.items()}
    write(ROOT/'data/confirmed.json',{'updated_at':now(),'entries':ledger})
    for filename in ['index.html','app.js','style.css']:(ROOT/filename).write_bytes((ROOT/'web'/filename).read_bytes())
    write(ROOT/'reports/publication.json',{'built_at':public['built_at'],'source_generated':read(SOURCE/'manifest.json')['generated'],'stats':public['stats'],'conflicting_segments':len(conflicts),'data_sha256':hashlib.sha256((ROOT/'data.json').read_bytes()).hexdigest()})
    print(json.dumps(public['stats'],ensure_ascii=False))

def reassess_cached():
    """Re-run identity rules against local evidence, without making any request."""
    lib=import_legacy();known={o['vid']:o for o in corpus()};changes=[]
    class Offline:
        def get(self,url):
            file=WORK/'http'/(hashlib.sha256(url.encode()).hexdigest()+'.json')
            cached=read(file)
            if not cached or time.time()-file.stat().st_mtime>=7*86400:raise ApiError('missing or expired cached evidence')
            return cached['body']
    for vid,e in lib.items():
        for i,c in enumerate(e['candidates']):
            if c.get('availability')!='available' or c['status']=='invalid':continue
            try:updated=evaluate(Offline(),known[vid],c)
            except ApiError:continue
            if c['status']!=updated['status']:changes.append({'vid':vid,'bvid':c['bvid'],'before':c['status'],'after':updated['status'],'reason':updated['reason']})
            e['candidates'][i]=updated
        e['status']=entry_status(e['candidates']) if e['candidates'] else e['status']
    write(WORK/'library.json',lib);write(WORK/'cached-reassessment.json',{'checked_at':now(),'changes':changes});report(lib)
    print(json.dumps(changes,ensure_ascii=False,indent=2))

def verify_leads(args):
    """Verify public-page leads without calling Bilibili search."""
    if not 1 <= args.limit <= 50: raise ValueError('batch limit must be 1–50')
    previous=read(WORK/'lead-receipt.json',{})
    if previous.get('stopped'):
        print('Previous detail verification batch hit risk control; inspect and archive its receipt before manually resuming.');return 2
    leads=read(Path(args.file),[]);lib=import_legacy();known={o['vid']:o for o in corpus()};client=Client(args.delay)
    receipt={'id':now(),'source':Path(args.file).name,'attempted':0,'completed':0,'confirmed':0,'errors':[],'stopped':False}
    for lead in leads[:args.limit]:
        bv=lead.get('bvid','')
        if bv:
            if not re.fullmatch(r'BV[A-Za-z0-9]{10}',bv):raise ValueError('invalid BVID')
            query={'bvid':bv}
        else:
            aid=lead.get('aid')
            if not isinstance(aid,int) or not 0<aid<10**16:raise ValueError('invalid AID')
            query={'aid':aid};bv='av'+str(aid)
        receipt['attempted']+=1
        try:
            response=client.get('https://api.bilibili.com/x/web-interface/view?'+urlencode(query))
            if response.get('code')==-404:
                # Remember newly discovered dead links too, so offline discovery cannot requeue them forever.
                if lead.get('vid') in known and re.fullmatch(r'BV[A-Za-z0-9]{10}',bv):
                    entry=lib.setdefault(lead['vid'],{'vid':lead['vid'],'status':'review','candidates':[]})
                    if not any(c['bvid']==bv for c in entry['candidates']):
                        entry['candidates'].append({'bvid':bv,'status':'review','origin':'public web index','lead_url':lead.get('url','')})
                for entry in lib.values():
                    for candidate in entry['candidates']:
                        if candidate['bvid']==bv or (lead.get('aid') and candidate.get('aid')==lead['aid']):
                            candidate.update(status='invalid',availability='unavailable',reason='view API explicitly returned -404',checked_at=now())
                    entry['status']=entry_status(entry['candidates']) if entry['candidates'] else entry['status']
                receipt['completed']+=1;receipt['errors'].append({'bvid':bv,'reason':'explicit -404'});continue
            d=response['data'];bv=d['bvid']
            canonical='https://api.bilibili.com/x/web-interface/view?'+urlencode({'bvid':bv})
            if query.get('aid'):
                source_url='https://api.bilibili.com/x/web-interface/view?'+urlencode(query)
                source_file=client.cache/(hashlib.sha256(source_url.encode()).hexdigest()+'.json')
                canonical_file=client.cache/(hashlib.sha256(canonical.encode()).hexdigest()+'.json')
                raw=read(source_file)
                write(canonical_file,{'url':canonical,'fetched_at':raw['fetched_at'],'body':response})
                os.utime(canonical_file,(source_file.stat().st_atime,source_file.stat().st_mtime))
            ids={lead['vid']} if lead.get('vid') else (primary_identity_ids(d.get('desc','')) | set().union(*(segment_source_ids(d,p) for p in d.get('pages',[])))) & known.keys()
            for vid in ids:
                if vid not in known:continue
                e=lib.setdefault(vid,{'vid':vid,'status':'review','candidates':[]})
                c=next((c for c in e['candidates'] if c['bvid']==bv),None)
                if c is None:
                    c={'bvid':bv,'status':'review','origin':'public web index','lead_url':lead.get('url','https://www.bilibili.com/video/'+bv)}
                    e['candidates'].append(c)
                if lead.get('page'):c['page']=lead['page'];c['page_locked']=True
                elif not lead.get('vid'):
                    exact=[p['page'] for p in d.get('pages',[]) if vid in segment_source_ids(d,p)]
                    if len(exact)==1:c['page']=exact[0]
                fresh=evaluate(client,known[vid],c);e['candidates'][e['candidates'].index(c)]=fresh
                e['status']=entry_status(e['candidates']);e['verified_at']=now()
                if not e.get('completed_at'):e['completed_at']=now();e['completion_method']='public lead verification'
                if fresh['status']=='confirmed':receipt['confirmed']+=1
                print(vid,bv,fresh['status'],fresh['reason'],flush=True)
            receipt['completed']+=1
        except (Blocked,ApiError) as err:
            receipt['errors'].append({'bvid':bv,'reason':str(err)})
            receipt['request_failed']=True
            if isinstance(err,Blocked):receipt['stopped']=True
        finally:
            write(WORK/'library.json',lib);write(WORK/'lead-receipt.json',receipt);report(lib)
        if receipt['stopped'] or receipt.get('request_failed'):break
    print(json.dumps(receipt,ensure_ascii=False))
    return 2 if receipt['errors'] else 0

def seed_identities():
    """Read cached public identities into a lead queue; never approve or mutate the library."""
    lib=read(WORK/'library.json',{});known={o['vid'] for o in corpus()};leads={}
    for file in sorted((WORK/'http').glob('*.json')):
        cached=read(file,{})
        url=cached.get('url','');body=(cached.get('body') or {}).get('data') or {}
        if '/x/web-interface/view?' in url:
            details=[body];origin='details'
        elif Client.is_search(url):
            details=[{'bvid':item.get('bvid',''),'desc':html.unescape(re.sub(r'<[^>]+>','',(item.get('description') or '')))} for item in body.get('result',[])]
            origin='search description'
        else:continue
        for d in details:
            bv=d.get('bvid','')
            if not re.fullmatch(r'BV[A-Za-z0-9]{10}',bv):continue
            ids=primary_identity_ids(d.get('desc','')) & known
            for page in d.get('pages',[]):ids |= segment_source_ids(d,page) & known
            for vid in sorted(ids):
                existing=next((c for c in lib.get(vid,{}).get('candidates',[]) if c['bvid']==bv),{})
                if existing.get('checked_at') and not existing.get('error'):continue
                lead={'vid':vid,'bvid':bv,'url':'https://www.bilibili.com/video/'+bv,
                      'discovery':'explicit source identity in cached public '+origin}
                exact=[page['page'] for page in d.get('pages',[]) if segment_source_ids(d,page)=={vid}]
                if len(exact)==1:lead['page']=exact[0]
                # Detail-backed page attribution takes priority over a search snippet.
                previous=leads.get((vid,bv),{})
                if origin=='details' or not previous.get('discovery','').endswith('details'):leads[(vid,bv)]=lead
    write(WORK/'cached-identity-leads.json',list(leads.values()))
    print(f'{len(leads)} source-identity leads; no requests or approval changes')

def seed_related():
    lib=import_legacy(); rows=corpus(); existing={(vid,c['bvid']) for vid,e in lib.items() for c in e['candidates']}
    stop={'the','and','with','for','what','how','part','lecture','chapter','from','that','this','are','you','why','introduction'}
    tokens=lambda title:set(re.findall(r'[a-z0-9]{3,}',title.lower()))-stop
    indexed=[(o,tokens(o['title']),norm(o['title'])) for o in rows]
    count=0; episodes={}
    for file in (WORK/'http').glob('*.json'):
        response=read(file,{})
        if '/x/web-interface/view?' not in response.get('url',''):continue
        d=response.get('body',{}).get('data',{}) or {}
        for section in (d.get('ugc_season') or {}).get('sections',[]):
            for e in section.get('episodes',[]):
                if e.get('bvid'):episodes[e['bvid']]={'title':e.get('title',''),'source_bvid':d.get('bvid')}
    for bv,e in episodes.items():
        t=tokens(e['title']);n=norm(e['title'])
        for o,ot,on in indexed:
            # Distinctive title match only seeds verification; no duration/identity assumptions.
            if not (len(ot)>=4 and len(ot&t)/len(ot)>=0.9 or len(on)>=24 and on in n):continue
            vid=o['vid']
            if (vid,bv) in existing:continue
            entry=lib.setdefault(vid,{'vid':vid,'status':'review','candidates':[]})
            entry['candidates'].append({'bvid':bv,'status':'review','origin':'public collection','lead_title':e['title'],'source_bvid':e['source_bvid'],'reason':'collection title lead; identity not yet verified'})
            entry.pop('completed_at',None);existing.add((vid,bv));count+=1
    write(WORK/'library.json',lib);report(lib)
    print(count,'new candidate leads from',len(episodes),'cached collection episodes')

def inspect(args):
    lib=import_legacy();original=next(o for o in corpus() if o['vid']==args.vid)
    e=lib.setdefault(args.vid,{'vid':args.vid,'status':'review','candidates':[]})
    c=next((c for c in e['candidates'] if c['bvid']==args.bvid),None)
    if c is None:
        c={'bvid':args.bvid,'status':'review','origin':'manual lead'};e['candidates'].append(c)
    if args.page:c['page']=args.page;c['page_locked']=True
    result=evaluate(Client(),original,c)
    e['candidates'][e['candidates'].index(c)]=result;e['status']=entry_status(e['candidates'])
    write(WORK/'library.json',lib);report(lib);print(json.dumps(result,ensure_ascii=False,indent=2))

def review(args):
    lib=read(WORK/'library.json',{});e=lib[args.vid]
    c=next(c for c in e['candidates'] if c['bvid']==args.bvid)
    if args.decision=='confirmed':
        if not args.evidence or not args.evidence.strip() or not args.page:raise ValueError('approval requires --evidence and --page')
        if c.get('availability')!='available' or c.get('page')!=args.page:raise ValueError('check selected segment availability first')
        if set(c.get('flags',[])) & {'conflicting years','conflicting episode','possibly abridged','derivative content requires review','missing segment','missing segment duration'}:raise ValueError('resolve content contradictions before approval')
        c['manual_review']={'at':now(),'evidence':args.evidence};c['evidence']=[args.evidence]
    if args.decision=='unmatched':
        if not args.evidence or not args.evidence.strip() or not args.page:raise ValueError('mismatch review requires --evidence and --page')
        if c.get('availability')!='available' or c.get('page')!=args.page or not c.get('cid'):raise ValueError('inspect the available selected segment first')
        if c.get('page_count')!=1:raise ValueError('do not reject a whole collection from a single inspected page')
        c['manual_rejection']={'at':now(),'evidence':args.evidence}
        c['evidence']=[args.evidence];c['reason']='manual review: available video does not match this original'
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
    published={(c['bvid'],v['id']) for v in d['videos'] for c in v['versions']}
    assert all((bv,vid) in published for bv,vid in d['legacy'].items()), 'legacy map includes unpublished candidates'
    public=(ROOT/'data.json').read_text()+(ROOT/'index.html').read_text()+(ROOT/'app.js').read_text()
    for forbidden in ['/Users/','/workspace/','source_file','legacy_confidence','SESSDATA','bili_jct']:assert forbidden not in public
    assert 'no-referrer' in (ROOT/'index.html').read_text()
    print(f'PASS: {len(ids)} originals, {len(segments)} verified segments; no internal paths or credentials')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);subs=parser.add_subparsers(dest='cmd',required=True)
    subs.add_parser('import');subs.add_parser('build');subs.add_parser('check');subs.add_parser('report');subs.add_parser('export-review');subs.add_parser('seed-related');subs.add_parser('seed-identities');subs.add_parser('reassess-cached')
    p=subs.add_parser('match');p.add_argument('--limit',type=int,default=50);p.add_argument('--delay',type=float,default=1.3);p.add_argument('--vid');p.add_argument('--exclude-vid',action='append',default=[]);p.add_argument('--existing-only',action='store_true');p.add_argument('--recheck',action='store_true');p.add_argument('--expand-review',action='store_true')
    p.add_argument('--primary-first',action='store_true')
    p=subs.add_parser('verify-leads');p.add_argument('file');p.add_argument('--limit',type=int,default=50);p.add_argument('--delay',type=float,default=2)
    p=subs.add_parser('inspect');p.add_argument('vid');p.add_argument('bvid');p.add_argument('--page',type=int)
    p=subs.add_parser('review');p.add_argument('vid');p.add_argument('bvid');p.add_argument('decision',choices=['confirmed','review','unmatched','invalid']);p.add_argument('--page',type=int);p.add_argument('--evidence')
    a=parser.parse_args()
    if a.cmd=='import': print(len(import_legacy()),'legacy originals imported')
    elif a.cmd=='match':raise SystemExit(run_match(a))
    elif a.cmd=='build':build()
    elif a.cmd=='check':check()
    elif a.cmd=='review':review(a)
    elif a.cmd=='inspect':inspect(a)
    elif a.cmd=='seed-related':seed_related()
    elif a.cmd=='seed-identities':seed_identities()
    elif a.cmd=='reassess-cached':reassess_cached()
    elif a.cmd=='verify-leads':raise SystemExit(verify_leads(a))
    elif a.cmd=='export-review':
        lib=read(WORK/'library.json',{})
        queue=[{'vid':vid,**c} for vid,e in lib.items() for c in e['candidates'] if c['status']=='review']
        write(WORK/'review-queue.json',queue);print(len(queue),'candidates exported to local review queue')
    else:print(json.dumps(report(read(WORK/'library.json',{})),ensure_ascii=False,indent=2))
