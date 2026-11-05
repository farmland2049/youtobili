import copy, importlib.util, json, tempfile, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('pipeline',Path(__file__).resolve().parents[1]/'scripts/pipeline.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)

class MatchingTests(unittest.TestCase):
 def setUp(self):
  self.o={'vid':'abcdefghijk','title':'Neural networks chapter 1 2024','channel':'Author'}
  self.d={'title':'【中文字幕】Neural networks chapter 1 2024','desc':'https://youtu.be/abcdefghijk', 'pages':[{'page':1,'duration':450,'part':'Neural networks chapter 1 2024','cid':123}]}
 def test_foreign_or_unspecified_subtitles_do_not_claim_chinese(self):
  for title in ['Talk [英语字幕]','Talk【字幕】','Talk [English subtitles]']:
   self.assertEqual(p.lang_kind(title,'Uploader','Author'),'original')
  self.assertEqual(p.lang_kind('Talk【中文字幕】','Uploader','Author'),'sub_zh')
 def test_explicit_chinese_english_subtitle_options(self):
  for title in ['Talk【中/英字幕可选】','Talk【中／英字幕】','Talk【英/中文字幕】','Talk【中 / 英 字幕】']:
   self.assertEqual(p.lang_kind(title,'Uploader','Author'),'sub_zh')
  self.assertEqual(p.lang_kind('Talk【英/日字幕】','Uploader','Author'),'original')
  self.assertEqual(p.lang_kind('Talk【中/英配音】','Uploader','Author'),'dub_zh')
 def result(self):return p.assess(self.o,self.d,1,450)
 def test_chinese_year_and_export_timestamp(self):
  self.o['title']='Using a 1930 Teletype as a Linux Terminal'
  self.d['title']='[生肉]把1930年的电传打字机用作Linux终端'
  self.d['pages'][0]['part']='成片-2020-4-30 17:42:54'
  self.assertEqual(self.result()['status'],'confirmed')
 def test_browser_recording_timestamp_is_not_content_year(self):
  self.o['title']='Ivan Sutherland Sketchpad Demo 1963'
  self.d['title']='Ivan Sutherland Sketchpad Demo'
  self.d['pages'][0]['part']='Ivan Sutherland Sketchpad Demo - YouTube 和另外 8 个页面 - 个人 - Microsoft Edge 2021-0'
  self.assertEqual(self.result()['status'],'confirmed')
  self.d['pages'][0]['part']='Sketchpad Demo 1965 - 个人 - Microsoft Edge 2021-0'
  self.assertIn('conflicting years',self.result()['flags'])
 def test_chinese_content_year_conflicts_still_require_review(self):
  self.d['title']='2026年的神经网络'
  self.d['pages'][0]['part']='成片-2024-1-1 12:00:00'
  self.assertIn('conflicting years',self.result()['flags'])
  self.assertEqual(p.content_years('型号12024年'),set())
  self.assertEqual(p.content_years('型号20240年'),set())
 def test_short_video_with_identity_is_accepted(self):self.assertEqual(self.result()['status'],'confirmed')
 def test_title_and_duration_without_identity_are_not_enough(self):
  self.d['desc']='title is similar';self.assertEqual(self.result()['status'],'review')
 def test_wrong_year(self):
  self.d['title']='Neural networks chapter 1 2026';self.d['pages'][0]['part']='';self.assertIn('conflicting years',self.result()['flags'])
 def test_wrong_episode(self):
  self.d['title']='Neural networks chapter 2 2024';self.assertIn('conflicting episode',self.result()['flags'])
 def test_abridged(self):
  self.d['title']+=' 精华片段';self.assertEqual(self.result()['status'],'review')
 def test_explicit_ai_derivative_is_not_a_source_copy(self):
  self.d['desc']+='\n本音频为 AI 生成衍生二次创作作品，仅供欣赏。'
  self.assertIn('derivative content requires review',self.result()['flags'])
  self.assertEqual(self.result()['status'],'review')
 def test_derivative_flag_blocks_preserved_manual_confirmation(self):
  self.d['desc']+='\n本音频为 AI 生成衍生二次创作作品。'
  self.d.update(owner={'name':'Uploader'},bvid='BV1234567890')
  d=self.d
  class Cached:
   def get(self,url):
    return {'data':d} if 'bilibili.com' in url else {'duration_s':450}
  fresh=p.evaluate(Cached(),self.o,{'bvid':'BV1234567890','page':1,'cid':123,'status':'confirmed','manual_review':{'evidence':'Prior source link review'}})
  self.assertEqual(fresh['status'],'review')
  self.assertIn('derivative content requires review',fresh['flags'])
 def test_cover_and_remix_require_content_review(self):
  for suffix in [' AI翻唱',' remix',' 二创']:
   with self.subTest(suffix=suffix):
    self.d['title']='Neural networks chapter 1 2024'+suffix
    self.assertIn('derivative content requires review',self.result()['flags'])
 def test_manual_approval_cannot_override_explicit_derivative_flag(self):
  from unittest.mock import patch
  from types import SimpleNamespace
  c={'bvid':'BV1234567890','page':1,'availability':'available','status':'review','flags':['derivative content requires review']}
  with patch.object(p,'read',return_value={self.o['vid']:{'candidates':[c]}}),patch.object(p,'write') as write:
   with self.assertRaisesRegex(ValueError,'resolve content contradictions'):
    p.review(SimpleNamespace(vid=self.o['vid'],bvid=c['bvid'],page=1,decision='confirmed',evidence='Contains original source URL'))
   write.assert_not_called()
 def test_translated_dubbing_does_not_imply_derivative_content(self):
  self.d['title']='【中配】Neural networks chapter 1 2024'
  self.d['desc']+='\n本视频使用 AI 生成中文配音，完整翻译原片。'
  self.assertEqual(self.result()['status'],'confirmed')
 def test_wrong_duration(self):
  self.d['pages'][0]['duration']=700;self.assertIn('duration outside tolerance',self.result()['flags'])
 def test_collection_uses_segment_not_total_duration(self):
  self.d['duration']=900;self.d['pages'][0]['part']+=' [abcdefghijk]';self.d['pages'].append({'page':2,'duration':450,'part':'chapter 2'})
  self.assertEqual(self.result()['status'],'confirmed')
 def test_inline_explicit_page_sources_bind_only_the_numbered_page(self):
  self.d['desc']='P1: 英语原视频 https://youtu.be/abcdefghijk\nP2: 汉语配音视频 https://example.org/dub\nP10: https://youtu.be/ABCDEFGHIJK'
  self.d['pages'][0]['part']='Original talk without a page prefix'
  self.d['pages'].append({'page':2,'duration':450,'part':'Dubbed talk'})
  self.assertEqual(p.segment_source_ids(self.d,self.d['pages'][0]),{'abcdefghijk'})
  self.assertEqual(p.segment_source_ids(self.d,self.d['pages'][1]),set())
  self.assertEqual(self.result()['status'],'confirmed')
  self.assertEqual(p.assess(self.o,self.d,2,450)['status'],'review')
  self.assertEqual(p.segment_source_ids(self.d,{'page':10}),{'ABCDEFGHIJK'})
 def test_collection_global_url_and_exact_title_do_not_bind_a_page(self):
  self.d['pages'].append({'page':2,'duration':450,'part':'another version'})
  self.assertEqual(self.result()['status'],'review')
  self.assertIn('collection segment identity requires review',self.result()['flags'])
 def test_collection_without_segment_identity(self):
  self.d['pages'][0]['part']='P1';self.d['pages'].append({'page':2,'duration':450,'part':'P2'})
  self.assertIn('collection segment identity requires review',self.result()['flags'])
 def test_missing_original_duration(self):self.assertEqual(p.assess(self.o,self.d,1,None)['status'],'review')
 def test_multiple_original_links(self):
  self.d['desc']+=' https://youtu.be/ABCDEFGHIJK';self.assertEqual(self.result()['status'],'review')
 def test_language_ranking_and_official_identity(self):
  self.assertEqual(p.lang_kind('官方双语','Author','Author'),'sub_zh')
  self.assertEqual(p.lang_kind('官方双语','搬运者','Author'),'sub_zh')
  self.assertEqual(p.lang_kind('中文配音','搬运者','Author'),'dub_zh')
  self.assertEqual(p.lang_kind('中文字幕配音','搬运者','Author'),'dub_zh')
  self.assertEqual(p.lang_kind('【熟肉】向量','Author','Author'),'sub_zh')
  self.assertLess(p.LANG_RANK['sub_zh'],p.LANG_RANK['dub_zh'])
 def test_official_requires_verified_creator_account_id(self):
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as temp,patch.object(p,'ROOT',Path(temp)):
   p.write(Path(temp)/'data/official-channels.json',{'accounts':{'author':{'bilibili_mid':123}}})
   self.assertEqual(p.lang_kind('官方双语','Author','Author',456),'sub_zh')
   self.assertEqual(p.lang_kind('官方双语','Author','Author'),'sub_zh')
   self.assertEqual(p.lang_kind('官方双语','Renamed account','Author','123'),'official_zh')
   self.assertEqual(p.lang_kind('Original','Renamed account','Author',123),'official_original')
   self.assertEqual(p.lang_kind('Original','Author','Other creator',123),'original')
 def test_missing_official_registry_does_not_trust_matching_names(self):
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as temp,patch.object(p,'ROOT',Path(temp)):
   self.assertEqual(p.lang_kind('Original','Author','Author',123),'original')
 def test_network_failure_is_not_invalid(self):
  class Failing:
   def get(self,url):raise p.ApiError('timeout')
  with self.assertRaises(p.ApiError):p.evaluate(Failing(),self.o,{'bvid':'BV1234567890','status':'confirmed'})
 def test_explicit_deleted_is_invalid(self):
  class Deleted:
   def get(self,url):return {'code':-404}
  self.assertEqual(p.evaluate(Deleted(),self.o,{'bvid':'BV1234567890'})['status'],'invalid')
  self.assertEqual(p.evaluate(Deleted(),self.o,{'bvid':'BV1234567890','availability':'available'})['availability'],'unavailable')
 def test_url_extractors(self):
  self.assertEqual(p.youtube_id('https://www.youtube.com/watch?v=abcdefghijk&x=1'),'abcdefghijk')
  self.assertEqual(p.identity_ids('https://www.youtube.com/watch?v=abcdefghijk&t=1'),{'abcdefghijk'})
  self.assertFalse(p.identity_ids('https://youtu.be/abcdefghijk123'))
  self.assertFalse(p.identity_ids('https://notyoutube.com/watch?v=abcdefghijk'))
  self.assertFalse(p.identity_ids('https://evil.youtube.com/watch?v=abcdefghijk'))
 def test_labeled_original_id_and_references_are_separate(self):
  self.d['desc']='YouTube: abcdefghijk\n其他资源：\nYouTube: ABCDEFGHIJK'
  self.assertEqual(self.result()['status'],'confirmed')
  self.o['vid']='ABCDEFGHIJK';self.assertEqual(self.result()['status'],'review')
 def test_exact_id_in_segment_filename(self):
  self.d['desc']='https://www.youtube.com/playlist?list=example'
  self.d['pages'][0]['part']='Neural networks chapter 1 2024-abcdefghijk'
  self.d['pages'].append({'page':2,'duration':700,'part':'other-ABCDEFGHIJK'})
  self.assertEqual(self.result()['status'],'confirmed')
  self.assertIn('exact original YouTube ID explicitly associated with selected segment',self.result()['evidence'])
 def test_segment_source_id_cannot_approve_different_episode(self):
  self.d['desc']='';self.d['pages'][0]['part']='chapter 2-abcdefghijk'
  self.d['pages'].append({'page':2,'duration':450,'part':'other-ABCDEFGHIJK'})
  self.assertEqual(self.result()['status'],'review')
 def test_segment_id_must_be_bracketed_or_terminal(self):
  self.assertEqual(p.segment_identity_ids('talk [abcdefghijk]'),{'abcdefghijk'})
  self.assertEqual(p.segment_identity_ids('talk-abcdefghijk'),{'abcdefghijk'})
  self.assertFalse(p.segment_identity_ids('Reference abcdefghijk appears in the middle'))
 def test_labeled_collection_maps_each_source_to_its_own_page(self):
  self.d['desc']='上篇：\nhttps://youtu.be/ABCDEFGHIJK\n下篇：\nhttps://youtu.be/abcdefghijk'
  self.d['pages']=[{'page':1,'duration':900,'part':'上篇 直观理解','cid':1},{'page':2,'duration':450,'part':'下篇 微积分原理','cid':2}]
  self.assertEqual(p.assess(self.o,self.d,2,450)['status'],'confirmed')
  self.assertEqual(p.assess(self.o,self.d,1,450)['status'],'review')
 def test_page_one_heading_is_not_page_ten(self):
  detail={'desc':'P1:\nhttps://youtu.be/abcdefghijk\nP10:\nhttps://youtu.be/ABCDEFGHIJK'}
  self.assertEqual(p.segment_source_ids(detail,{'part':'P10 正确内容'}),{'ABCDEFGHIJK'})
 def test_cached_response_and_expiry(self):
  with tempfile.TemporaryDirectory() as temp:
   old=p.WORK;p.WORK=Path(temp)
   try:
    c=p.Client();u='https://example.test/';key=c.cache/(p.hashlib.sha256(u.encode()).hexdigest()+'.json')
    p.write(key,{'body':{'code':0,'data':[]}})
    self.assertEqual(c.get(u),{'code':0,'data':[]})
   finally:p.WORK=old

class MismatchReviewTests(unittest.TestCase):
 def test_available_mismatch_is_not_unavailable(self):
  from types import SimpleNamespace
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as temp,patch.object(p,'WORK',Path(temp)),patch.object(p,'report'):
   c={'bvid':'BV1234567890','status':'review','availability':'available','page':1,'cid':123,'page_count':1}
   lib={'abcdefghijk':{'status':'review','candidates':[c]}}
   p.write(p.WORK/'library.json',lib)
   p.review(SimpleNamespace(vid='abcdefghijk',bvid=c['bvid'],decision='unmatched',page=1,evidence='Creator and content are a different recorded talk'))
   saved=p.read(p.WORK/'library.json')['abcdefghijk']
   self.assertEqual(saved['status'],'unmatched')
   self.assertEqual(saved['candidates'][0]['availability'],'available')
   self.assertTrue(saved['candidates'][0]['manual_rejection']['evidence'])
   self.assertEqual(p.entry_status([saved['candidates'][0],{'status':'invalid'}]),'unmatched')
   self.assertEqual(p.entry_status([saved['candidates'][0],{'status':'review'}]),'review')
 def test_mismatch_requires_evidence_and_cannot_reject_collection(self):
  from types import SimpleNamespace
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as temp,patch.object(p,'WORK',Path(temp)),patch.object(p,'report'):
   c={'bvid':'BV1234567890','status':'review','availability':'available','page':1,'cid':123,'page_count':2}
   p.write(p.WORK/'library.json',{'abcdefghijk':{'status':'review','candidates':[c]}})
   for evidence in ['','   ','Only one page inspected']:
    with self.assertRaises(ValueError):p.review(SimpleNamespace(vid='abcdefghijk',bvid=c['bvid'],decision='unmatched',page=1,evidence=evidence))
   self.assertEqual(p.read(p.WORK/'library.json')['abcdefghijk']['status'],'review')
 def test_rejection_expires_when_content_or_collection_changes(self):
  o={'vid':'abcdefghijk','title':'Talk','channel':'Author'}
  c={'bvid':'BV1234567890','status':'unmatched','cid':123,'page':1,'manual_rejection':{'evidence':'Different content'}}
  detail={'title':'Other talk','desc':'','owner':{'name':'Uploader'},'pages':[{'page':1,'cid':123,'duration':300,'part':'Other talk'}]}
  class Fixture:
   def get(self,url):return {'video':{'duration_s':300}} if 'hackertube.org' in url else {'data':detail}
  self.assertEqual(p.evaluate(Fixture(),o,c)['status'],'unmatched')
  detail['pages'][0]['cid']=456
  self.assertEqual(p.evaluate(Fixture(),o,c)['status'],'review')
  detail['pages'][0]['cid']=123;detail['pages'].append({'page':2,'cid':456,'duration':300,'part':'new content'})
  self.assertEqual(p.evaluate(Fixture(),o,c)['status'],'review')

class BuildTests(unittest.TestCase):
 def test_only_confirmed_and_unique_segments_are_published(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp);old=(p.ROOT,p.SOURCE,p.WORK);p.ROOT=root;p.SOURCE=root/'data/source';p.WORK=root/'data/work'
   try:
    p.SOURCE.mkdir(parents=True);(root/'web').mkdir();(root/'reports').mkdir()
    rows=[{'vid':i,'title':i,'categories':[{'id':'cat'}]} for i in ['abcdefghijk','ABCDEFGHIJK','01234567890']]
    (p.SOURCE/'videos.jsonl').write_text('\n'.join(json.dumps(x) for x in rows))
    p.write(p.SOURCE/'taxonomy.json',{'areas':[{'id':'a','name':'A','categories':[{'id':'cat','name':'C'}]}]})
    p.write(p.SOURCE/'manifest.json',{'generated':'2026-11-04'})
    for f in ['index.html','app.js','style.css']:(root/'web'/f).write_text('')
    def candidate(status,page):return {'bvid':'BV1234567890','status':status,'availability':'available','evidence':['original link'],'page':page,'cid':page,'title':'T','up':'U','duration':50,'kind':'sub_zh','views':1,'pic':'https://example.org/pic','checked_at':p.now()}
    lib={rows[0]['vid']:{'status':'confirmed','candidates':[candidate('confirmed',1),candidate('review',3)]},rows[1]['vid']:{'status':'confirmed','candidates':[candidate('confirmed',2)]},rows[2]['vid']:{'status':'review','candidates':[candidate('review',4)]}}
    lib[rows[0]['vid']]['candidates'][0]['search_hint']={'identity':True}
    lib[rows[0]['vid']]['candidates'][1]['bvid']='BV9999999999'
    lib[rows[2]['vid']]['candidates'][0]['bvid']='BV8888888888'
    p.write(p.WORK/'library.json',lib);p.build();d=p.read(root/'data.json')
    self.assertEqual(len(d['videos']),2);self.assertEqual(len(d['videos'][0]['versions']),1)
    self.assertNotIn('search_hint',(root/'data.json').read_text())
    self.assertNotIn('search_hint',(root/'data/confirmed.json').read_text())
    self.assertEqual(d['legacy'],{'BV1234567890':rows[0]['vid']})
    lib[rows[1]['vid']]['candidates'][0]['page']=1;p.write(p.WORK/'library.json',lib);p.build()
    self.assertEqual(len(p.read(root/'data.json')['videos']),0)
    self.assertEqual(p.read(root/'data.json')['legacy'],{})
   finally:p.ROOT,p.SOURCE,p.WORK=old


class BatchTests(unittest.TestCase):
 def test_block_stops_batch_and_resume_preserves_completed_work(self):
  from unittest.mock import patch
  from types import SimpleNamespace
  with tempfile.TemporaryDirectory() as temp:
   old=p.ROOT,p.WORK;p.ROOT=Path(temp);p.WORK=Path(temp)/'work'
   rows=[{'vid':x,'score':1} for x in ['abcdefghijk','ABCDEFGHIJK','01234567890']]
   lib={x['vid']:{'vid':x['vid'],'status':'review','candidates':[{'bvid':'BV1234567890','status':'review'}]} for x in rows}
   seen=[]
   def evaluate(client,o,c):
    seen.append(o['vid'])
    if o['vid']=='ABCDEFGHIJK':raise p.Blocked('HTTP 412')
    return {**c,'status':'confirmed','checked_at':p.now()}
   args=SimpleNamespace(delay=1.3,existing_only=True,recheck=False,limit=50)
   try:
    with patch.object(p,'corpus',return_value=rows),patch.object(p,'import_legacy',return_value=lib),patch.object(p,'report'),patch.object(p,'Client'),patch.object(p,'evaluate',side_effect=evaluate):
     self.assertEqual(p.run_match(args),2)
    self.assertEqual(seen,['abcdefghijk','ABCDEFGHIJK'])
    saved=p.read(p.WORK/'library.json');self.assertTrue(saved['abcdefghijk'].get('completed_at'));self.assertNotIn('completed_at',saved['ABCDEFGHIJK'])
    seen.clear()
    def success(client,o,c):seen.append(o['vid']);return {**c,'status':'confirmed','checked_at':p.now()}
    with patch.object(p,'corpus',return_value=rows),patch.object(p,'import_legacy',return_value=saved),patch.object(p,'report'),patch.object(p,'Client'),patch.object(p,'evaluate',side_effect=success):
     self.assertEqual(p.run_match(args),0)
    self.assertEqual(seen,['ABCDEFGHIJK','01234567890'])
   finally:p.ROOT,p.WORK=old

 def test_network_error_stops_and_leaves_later_originals_unattempted(self):
  from unittest.mock import patch
  from types import SimpleNamespace
  with tempfile.TemporaryDirectory() as temp,patch.object(p,'WORK',Path(temp)),patch.object(p,'report'):
   rows=[{'vid':v,'score':1} for v in ['abcdefghijk','ABCDEFGHIJK']]
   lib={r['vid']:{'status':'review','candidates':[{'bvid':'BV1234567890','status':'review'}]} for r in rows}
   with patch.object(p,'corpus',return_value=rows),patch.object(p,'import_legacy',return_value=lib),patch.object(p,'Client'),patch.object(p,'evaluate',side_effect=p.ApiError('RemoteDisconnected')) as evaluate:
    self.assertEqual(p.run_match(SimpleNamespace(limit=2,delay=1.3,existing_only=True,recheck=False)),2)
   self.assertEqual(evaluate.call_count,1)
   batch=p.read(next((Path(temp)/'batches').glob('*.json')))
   self.assertEqual(batch['unattempted'],1);self.assertFalse(batch['stopped'])
   self.assertEqual(lib['abcdefghijk']['candidates'][0]['status'],'review')
   self.assertNotIn('completed_at',lib['abcdefghijk'])

class SearchCandidateTests(unittest.TestCase):
 def test_primary_first_keeps_candidates_and_requires_full_identity(self):
  from unittest.mock import patch
  from types import SimpleNamespace
  with tempfile.TemporaryDirectory() as temp,patch.object(p,'ROOT',Path(temp)),patch.object(p,'WORK',Path(temp)/'work'):
   original={'vid':'abcdefghijk','title':'Original title','channel':'Creator'}
   results=[{'bvid':'BV0000000001','title':'Original title','duration':'10:00'},
    {'bvid':'BV0000000002','title':'【中文字幕】Original title','description':'https://youtu.be/abcdefghijk','duration':'10:00'},
    {'bvid':'BV0000000003','title':'Original title','duration':'10:00'}]
   seen=[];lib={}
   class Fixture:
    def __init__(self,delay):pass
    def get(self,url):
     if 'hackertube.org' in url:return {'video':{'duration_s':600}}
     if '/search/' in url:return {'data':{'result':results}}
     bv=p.parse_qs(p.urlparse(url).query)['bvid'][0];seen.append(bv)
     return {'data':{'title':next(x['title'] for x in results if x['bvid']==bv),
      'desc':'https://youtu.be/abcdefghijk' if bv=='BV0000000001' else '',
      'owner':{'name':'Uploader'},'pages':[{'page':1,'cid':123,'duration':600,'part':'Original title'}]}}
   args=SimpleNamespace(delay=1.3,existing_only=False,recheck=False,limit=1,primary_first=True)
   with patch.object(p,'corpus',return_value=[original]),patch.object(p,'import_legacy',return_value=lib),patch.object(p,'Client',Fixture),patch.object(p,'report'):
    self.assertEqual(p.run_match(args),0)
   self.assertEqual(seen,['BV0000000002','BV0000000001'])
   candidates={c['bvid']:c for c in lib['abcdefghijk']['candidates']}
   self.assertEqual(candidates['BV0000000002']['status'],'review')
   self.assertEqual(candidates['BV0000000001']['status'],'confirmed')
   self.assertTrue(candidates['BV0000000003']['detail_deferred_after_match'])
   self.assertNotIn('checked_at',candidates['BV0000000003'])
   self.assertEqual(len(candidates),3)
 def test_primary_first_recheck_is_rejected_before_requests(self):
  from unittest.mock import patch
  from types import SimpleNamespace
  with patch.object(p,'Client') as client:
   with self.assertRaises(ValueError):p.run_match(SimpleNamespace(limit=1,primary_first=True,recheck=True))
   client.assert_not_called()
 def test_excluded_original_is_not_requested_and_is_reported(self):
  from unittest.mock import patch
  from types import SimpleNamespace
  with tempfile.TemporaryDirectory() as temp,patch.object(p,'ROOT',Path(temp)),patch.object(p,'WORK',Path(temp)/'work'):
   rows=[{'vid':'blocked0001','title':'Blocked original'}, {'vid':'next0000001','title':'Next original'}]
   lib={};requests=[]
   class Fixture:
    def __init__(self,delay):pass
    def get(self,url):
     requests.append(url)
     return {'video':{'duration_s':600}} if 'hackertube.org' in url else {'data':{'result':[]}}
   args=SimpleNamespace(delay=1.3,existing_only=False,recheck=False,expand_review=False,
       limit=1,primary_first=True,vid=None,exclude_vid=['blocked0001'])
   with patch.object(p,'corpus',return_value=rows),patch.object(p,'import_legacy',return_value=lib),patch.object(p,'Client',Fixture),patch.object(p,'report'):
    self.assertEqual(p.run_match(args),0)
   batch=next((Path(temp)/'work'/'batches').glob('*.json'))
   receipt=p.read(batch)
   self.assertEqual(receipt['originals'],['next0000001'])
   self.assertEqual(receipt['excluded_originals'],['blocked0001'])
   self.assertEqual(len(requests),2)
   self.assertIn('completed_at',lib['next0000001'])
   self.assertNotIn('blocked0001',lib)
 def test_review_expansion_selects_shallow_reviews_and_failed_expansions(self):
  from unittest.mock import patch
  from types import SimpleNamespace
  with tempfile.TemporaryDirectory() as temp,patch.object(p,'ROOT',Path(temp)),patch.object(p,'WORK',Path(temp)/'work'):
   rows=[{'vid':v,'title':v} for v in ['abcdefghijk','ABCDEFGHIJK','01234567890','abcdefghij0']]
   lib={r['vid']:{'status':'review','completed_at':'before','search_result_limit':20,'candidates':[]} for r in rows}
   lib[rows[0]['vid']]['search_result_limit']=5
   lib[rows[2]['vid']]['status']='confirmed'
   lib[rows[3]['vid']]['last_error']='network error'
   class Fixture:
    def __init__(self,delay):pass
    def get(self,url):return {'video':{'duration_s':600}} if 'hackertube.org' in url else {'data':{'result':[]}}
   args=SimpleNamespace(delay=1.3,existing_only=False,recheck=False,expand_review=True,limit=50)
   with patch.object(p,'corpus',return_value=rows),patch.object(p,'import_legacy',return_value=lib),patch.object(p,'Client',Fixture),patch.object(p,'report'):
    self.assertEqual(p.run_match(args),0)
   self.assertNotEqual(lib[rows[0]['vid']]['completed_at'],'before')
   self.assertEqual(lib[rows[1]['vid']]['completed_at'],'before')
   self.assertEqual(lib[rows[2]['vid']]['completed_at'],'before')
   self.assertNotEqual(lib[rows[3]['vid']]['completed_at'],'before')
   self.assertNotIn('last_error',lib[rows[3]['vid']])
 def test_matching_candidate_after_fifth_result_is_checked(self):
  from unittest.mock import patch
  from types import SimpleNamespace
  with tempfile.TemporaryDirectory() as temp,patch.object(p,'ROOT',Path(temp)),patch.object(p,'WORK',Path(temp)/'work'):
   original={'vid':'abcdefghijk','title':'Distinctive original title','channel':'Author'}
   results=[{'bvid':'BV'+str(i).zfill(10),'duration':'10:00'} for i in range(7)]
   lib={};seen=[]
   class Fixture:
    def __init__(self,delay):pass
    def get(self,url):
     return {'video':{'duration_s':600}} if 'hackertube.org' in url else {'data':{'result':results}}
   def evaluate(client,o,c):
    seen.append(c['bvid'])
    return {**c,'status':'confirmed' if c['bvid']==results[-1]['bvid'] else 'review','checked_at':p.now()}
   args=SimpleNamespace(delay=1.3,existing_only=False,recheck=False,limit=1)
   with patch.object(p,'corpus',return_value=[original]),patch.object(p,'import_legacy',return_value=lib),patch.object(p,'Client',Fixture),patch.object(p,'evaluate',side_effect=evaluate),patch.object(p,'report'):
    self.assertEqual(p.run_match(args),0)
   self.assertIn(results[-1]['bvid'],seen)
   self.assertEqual(len(lib[original['vid']]['candidates']),7)
   self.assertEqual(lib[original['vid']]['status'],'confirmed')
 def test_only_shorter_candidates_are_deferred(self):
  self.assertTrue(p.defer_short_candidate(3600,600))
  self.assertFalse(p.defer_short_candidate(3600,3650))
  self.assertFalse(p.defer_short_candidate(3600,50000))
  self.assertFalse(p.defer_short_candidate(None,20))
  self.assertFalse(p.defer_short_candidate(3600,None))
 def test_search_duration_formats(self):
  self.assertEqual(p.search_duration('90:01'),5401)
  self.assertEqual(p.search_duration('1:30:01'),5401)
  self.assertIsNone(p.search_duration('unavailable'))
  self.assertIsNone(p.search_duration('12:88'))
 def test_query_aliases_change_search_not_original_identity(self):
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as temp,patch.object(p,'ROOT',Path(temp)):
   original={'vid':'abcdefghijk','title':'Original English title','channel':'Author'}
   p.write(Path(temp)/'data/search-queries.json',{'abcdefghijk':['short author title','translated title']})
   self.assertEqual(p.search_queries(original),['short author title','translated title'])
   self.assertEqual(original['title'],'Original English title')

class GuestSearchTests(unittest.TestCase):
 def fixture(self,bootstrap_cookie=True,blocked=False):
  import io
  from urllib.error import HTTPError
  c=p.Client(delay=3);calls=[]
  class Opener:
   def open(self,req,timeout):
    calls.append(req)
    if len(calls)==1:
     if blocked:raise HTTPError(req.full_url,412,'blocked',None,None)
     if bootstrap_cookie:c.cookie_jar.set_cookie(p.http.cookiejar.Cookie(0,'buvid3','test-visitor',None,False,'.bilibili.com',True,True,'/',True,False,None,True,None,None,{},False))
     return io.BytesIO(b'<html>public homepage</html>')
    return io.BytesIO(b'{"code":0,"data":{"result":[]}}')
  c.opener=Opener();return c,calls
 def test_disconnection_is_an_error_without_retry_or_cache(self):
  from unittest.mock import patch
  from http.client import RemoteDisconnected
  with tempfile.TemporaryDirectory() as temp,patch.object(p,'WORK',Path(temp)),patch.object(p.Client,'wait_turn'):
   for guest in (False,True):
    c=p.Client();c.opener=unittest.mock.Mock()
    c.opener.open.side_effect=RemoteDisconnected('closed')
    with self.assertRaisesRegex(p.ApiError,'RemoteDisconnected'):
     if guest:c.ensure_guest()
     else:c.get('https://api.bilibili.com/x/web-interface/view?bvid=BV1234567890')
    self.assertEqual(c.opener.open.call_count,1)
    self.assertEqual(list(c.cache.glob('*.json')),[])
 def test_homepage_is_visited_once_before_search_with_headers(self):
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as temp,patch.object(p,'WORK',Path(temp)),patch.object(p.Client,'wait_turn'):
   c,calls=self.fixture();c.get('https://api.bilibili.com/x/web-interface/search/type?keyword=one');c.get('https://api.bilibili.com/x/web-interface/search/type?keyword=two')
   self.assertEqual([r.full_url for r in calls][0],'https://www.bilibili.com/')
   self.assertEqual(len(calls),3);self.assertTrue(c.guest_ready)
   self.assertEqual(calls[1].get_header('Referer'),'https://search.bilibili.com/')
   self.assertIn('AppleWebKit',calls[1].get_header('User-agent'))
 def test_missing_cookie_stops_before_search(self):
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as temp,patch.object(p,'WORK',Path(temp)),patch.object(p.Client,'wait_turn'):
   c,calls=self.fixture(bootstrap_cookie=False)
   with self.assertRaises(p.Blocked):c.get('https://api.bilibili.com/x/web-interface/search/type?keyword=one')
   self.assertEqual(len(calls),1)
 def test_bootstrap_412_is_not_retried(self):
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as temp,patch.object(p,'WORK',Path(temp)),patch.object(p.Client,'wait_turn'):
   c,calls=self.fixture(blocked=True)
   with self.assertRaises(p.Blocked):c.get('https://api.bilibili.com/x/web-interface/search/type?keyword=one')
   self.assertEqual(len(calls),1)
 def test_old_anonymous_cache_is_not_reused(self):
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as temp,patch.object(p,'WORK',Path(temp)),patch.object(p.Client,'wait_turn'):
   c,calls=self.fixture();url='https://api.bilibili.com/x/web-interface/search/type?keyword=one'
   p.write(c.cache/(p.hashlib.sha256(url.encode()).hexdigest()+'.json'),{'body':{'code':0,'bad_cache':True}})
   self.assertNotIn('bad_cache',c.get(url));self.assertEqual(len(calls),2)
   c.get(url);self.assertEqual(len(calls),2)
 def test_search_has_three_second_minimum_even_with_default_delay(self):
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as temp,patch.object(p,'WORK',Path(temp)),patch.object(p.time,'sleep') as sleep,patch.object(p.time,'monotonic',return_value=100):
   c,calls=self.fixture();c.delay=1.3;c.last=99
   c.get('https://api.bilibili.com/x/web-interface/search/type?keyword=one')
   self.assertEqual(sleep.call_args.args[0],3)
 def test_view_requests_do_not_visit_homepage(self):
  from unittest.mock import patch
  import io
  with tempfile.TemporaryDirectory() as temp,patch.object(p,'WORK',Path(temp)),patch.object(p.Client,'wait_turn'):
   c=p.Client();calls=[]
   class Opener:
    def open(self,req,timeout):calls.append(req.full_url);return io.BytesIO(b'{"code":0,"data":{}}')
   c.opener=Opener();c.get('https://api.bilibili.com/x/web-interface/view?bvid=BV1234567890')
   self.assertEqual(len(calls),1);self.assertFalse(c.guest_ready)

class PublicLeadTests(unittest.TestCase):
 def test_ordinary_request_error_stops_lead_batch(self):
  from unittest.mock import patch
  from types import SimpleNamespace
  with tempfile.TemporaryDirectory() as temp,patch.object(p,'WORK',Path(temp)),patch.object(p,'report'):
   file=Path(temp)/'leads.json';p.write(file,[{'vid':'abcdefghijk','bvid':'BV1234567890'},{'vid':'abcdefghijk','bvid':'BV1234567891'}])
   with patch.object(p,'import_legacy',return_value={}),patch.object(p,'corpus',return_value=[{'vid':'abcdefghijk'}]),patch.object(p,'Client') as client:
    client.return_value.get.side_effect=p.ApiError('RemoteDisconnected')
    self.assertEqual(p.verify_leads(SimpleNamespace(file=str(file),limit=50,delay=1.3)),2)
    self.assertEqual(client.return_value.get.call_count,1)
   receipt=p.read(Path(temp)/'lead-receipt.json')
   self.assertEqual(receipt['attempted'],1);self.assertTrue(receipt['request_failed']);self.assertFalse(receipt['stopped'])
 def test_new_deleted_identity_lead_is_recorded_without_completing_original(self):
  from unittest.mock import patch
  from types import SimpleNamespace
  with tempfile.TemporaryDirectory() as temp,patch.object(p,'WORK',Path(temp)):
   p.write(p.WORK/'leads.json',[{'vid':'abcdefghijk','bvid':'BV1234567890'}])
   class Deleted:
    def __init__(self,delay):pass
    def get(self,url):return {'code':-404}
   with patch.object(p,'import_legacy',return_value={}),patch.object(p,'corpus',return_value=[{'vid':'abcdefghijk'}]),patch.object(p,'Client',Deleted),patch.object(p,'report'):
    self.assertEqual(p.verify_leads(SimpleNamespace(limit=50,file=str(p.WORK/'leads.json'),delay=2)),2)
   entry=p.read(p.WORK/'library.json')['abcdefghijk']
   self.assertEqual(entry['status'],'invalid')
   self.assertEqual(entry['candidates'][0]['availability'],'unavailable')
   self.assertTrue(entry['candidates'][0]['checked_at'])
   self.assertNotIn('completed_at',entry)
 def test_detail_block_latch_prevents_followup_requests(self):
  from unittest.mock import patch
  from types import SimpleNamespace
  with tempfile.TemporaryDirectory() as temp:
   old=p.WORK;p.WORK=Path(temp)
   try:
    p.write(p.WORK/'lead-receipt.json',{'stopped':True})
    with patch.object(p,'Client') as client:
     self.assertEqual(p.verify_leads(SimpleNamespace(limit=50,file='unused',delay=2)),2)
     client.assert_not_called()
   finally:p.WORK=old
 def test_explicit_deleted_lead_removes_previously_confirmed_version(self):
  from unittest.mock import patch
  from types import SimpleNamespace
  with tempfile.TemporaryDirectory() as temp:
   old=p.WORK;p.WORK=Path(temp)
   lib={'abcdefghijk':{'vid':'abcdefghijk','status':'confirmed','candidates':[{'bvid':'BV1234567890','status':'confirmed','availability':'available'}]}}
   p.write(Path(temp)/'leads.json',[{'bvid':'BV1234567890'}])
   class Deleted:
    def get(self,url):return {'code':-404}
   try:
    with patch.object(p,'import_legacy',return_value=lib),patch.object(p,'corpus',return_value=[]),patch.object(p,'Client',return_value=Deleted()),patch.object(p,'report'):
     self.assertEqual(p.verify_leads(SimpleNamespace(limit=50,file=str(Path(temp)/'leads.json'),delay=2)),2)
    c=p.read(p.WORK/'library.json')['abcdefghijk']['candidates'][0]
    self.assertEqual(c['status'],'invalid');self.assertEqual(c['availability'],'unavailable')
   finally:p.WORK=old
 def test_aid_resolution_does_not_extend_cached_evidence_lifetime(self):
  from unittest.mock import patch
  from types import SimpleNamespace
  with tempfile.TemporaryDirectory() as temp:
   old=p.WORK;p.WORK=Path(temp)
   p.write(Path(temp)/'leads.json',[{'aid':123}])
   class Cached:
    def __init__(self,delay):self.cache=Path(temp)/'http';self.cache.mkdir()
    def get(self,url):
     file=self.cache/(p.hashlib.sha256(url.encode()).hexdigest()+'.json')
     body={'code':0,'data':{'bvid':'BV1234567890','desc':'https://youtu.be/abcdefghijk','pages':[]}}
     p.write(file,{'url':url,'fetched_at':'2026-11-04T00:00:00+00:00','body':body})
     p.os.utime(file,(p.time.time()-600,p.time.time()-600));return body
   try:
    with patch.object(p,'import_legacy',return_value={}),patch.object(p,'corpus',return_value=[{'vid':'abcdefghijk'}]),patch.object(p,'Client',Cached),patch.object(p,'report'),patch.object(p,'evaluate',side_effect=lambda client,o,c:{**c,'status':'confirmed','reason':'fixture verified'}):
     self.assertEqual(p.verify_leads(SimpleNamespace(limit=50,file=str(Path(temp)/'leads.json'),delay=2)),0)
    canonical='https://api.bilibili.com/x/web-interface/view?bvid=BV1234567890'
    file=p.WORK/'http'/(p.hashlib.sha256(canonical.encode()).hexdigest()+'.json')
    self.assertGreater(p.time.time()-file.stat().st_mtime,590)
    self.assertEqual(p.read(file)['fetched_at'],'2026-11-04T00:00:00+00:00')
   finally:p.WORK=old
 def test_cached_source_id_leads_do_not_request_or_approve(self):
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as temp,patch.object(p,'WORK',Path(temp)):
   lib={'abcdefghijk':{'status':'review','candidates':[]}}
   p.write(p.WORK/'library.json',lib)
   detail={'bvid':'BV1234567890','desc':'https://youtu.be/abcdefghijk\nOther resources:\nhttps://youtu.be/01234567890',
           'pages':[{'page':1,'part':'main'},{'page':2,'part':'Another talk [ABCDEFGHIJK]'}]}
   p.write(p.WORK/'http/one.json',{'url':'https://api.bilibili.com/x/web-interface/view?bvid=BV1234567890','body':{'data':detail}})
   rows=[{'vid':v} for v in ['abcdefghijk','ABCDEFGHIJK','01234567890']]
   with patch.object(p,'corpus',return_value=rows),patch.object(p,'Client') as client:
    p.seed_identities();client.assert_not_called()
   leads=p.read(p.WORK/'cached-identity-leads.json')
   self.assertEqual({x['vid'] for x in leads},{'abcdefghijk','ABCDEFGHIJK'})
   self.assertEqual(next(x for x in leads if x['vid']=='ABCDEFGHIJK')['page'],2)
   self.assertEqual(p.read(p.WORK/'library.json'),lib)
   lib['abcdefghijk']['candidates']=[{'bvid':'BV1234567890','checked_at':p.now(),'status':'review'}]
   p.write(p.WORK/'library.json',lib)
   with patch.object(p,'corpus',return_value=rows):p.seed_identities()
   self.assertEqual([x['vid'] for x in p.read(p.WORK/'cached-identity-leads.json')],['ABCDEFGHIJK'])
 def test_cached_search_source_id_after_fifth_result_is_only_a_lead(self):
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as temp,patch.object(p,'WORK',Path(temp)):
   results=[{'bvid':'BV'+str(i).zfill(10),'description':''} for i in range(6)]
   results[-1]['description']='https://youtu.be/<em>abcdefghijk</em>'
   p.write(p.WORK/'http/search.json',{'url':'https://api.bilibili.com/x/web-interface/search/type?keyword=topic','body':{'data':{'result':results}}})
   with patch.object(p,'corpus',return_value=[{'vid':'abcdefghijk'}]),patch.object(p.Client,'__init__') as client_init:
    p.seed_identities();client_init.assert_not_called()
   leads=p.read(p.WORK/'cached-identity-leads.json')
   self.assertEqual(len(leads),1);self.assertEqual(leads[0]['bvid'],results[-1]['bvid'])
   self.assertFalse((p.WORK/'library.json').exists())
 def test_collection_titles_only_seed_candidates(self):
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as temp:
   old=p.WORK;p.WORK=Path(temp)
   o={'vid':'abcdefghijk','title':'Building a programmable computer with simple gates'}
   p.write(p.WORK/'http/one.json',{'url':'https://api.bilibili.com/x/web-interface/view?bvid=BV1234567890','body':{'data':{'bvid':'BV1234567890','ugc_season':{'sections':[{'episodes':[{'bvid':'BVABCDEFGHIJ','title':o['title']}]}]}}}})
   try:
    with patch.object(p,'import_legacy',return_value={}),patch.object(p,'corpus',return_value=[o]),patch.object(p,'report'),patch.object(p,'Client') as client:
     p.seed_related();client.assert_not_called()
    self.assertEqual(p.read(p.WORK/'library.json')['abcdefghijk']['candidates'][0]['status'],'review')
   finally:p.WORK=old

if __name__=='__main__':unittest.main()
