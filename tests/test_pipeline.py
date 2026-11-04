import copy, importlib.util, json, tempfile, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('pipeline',Path(__file__).resolve().parents[1]/'scripts/pipeline.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)

class MatchingTests(unittest.TestCase):
 def setUp(self):
  self.o={'vid':'abcdefghijk','title':'Neural networks chapter 1 2024','channel':'Author'}
  self.d={'title':'【中文字幕】Neural networks chapter 1 2024','desc':'https://youtu.be/abcdefghijk', 'pages':[{'page':1,'duration':450,'part':'Neural networks chapter 1 2024','cid':123}]}
 def result(self):return p.assess(self.o,self.d,1,450)
 def test_short_video_with_identity_is_accepted(self):self.assertEqual(self.result()['status'],'confirmed')
 def test_title_and_duration_without_identity_are_not_enough(self):
  self.d['desc']='title is similar';self.assertEqual(self.result()['status'],'review')
 def test_wrong_year(self):
  self.d['title']='Neural networks chapter 1 2026';self.d['pages'][0]['part']='';self.assertIn('conflicting years',self.result()['flags'])
 def test_wrong_episode(self):
  self.d['title']='Neural networks chapter 2 2024';self.assertIn('conflicting episode',self.result()['flags'])
 def test_abridged(self):
  self.d['title']+=' 精华片段';self.assertEqual(self.result()['status'],'review')
 def test_wrong_duration(self):
  self.d['pages'][0]['duration']=700;self.assertIn('duration outside tolerance',self.result()['flags'])
 def test_collection_uses_segment_not_total_duration(self):
  self.d['duration']=900;self.d['pages'].append({'page':2,'duration':450,'part':'chapter 2'})
  self.assertEqual(self.result()['status'],'confirmed')
 def test_collection_without_segment_identity(self):
  self.d['pages'][0]['part']='P1';self.d['pages'].append({'page':2,'duration':450,'part':'P2'})
  self.assertIn('collection segment identity requires review',self.result()['flags'])
 def test_missing_original_duration(self):self.assertEqual(p.assess(self.o,self.d,1,None)['status'],'review')
 def test_multiple_original_links(self):
  self.d['desc']+=' https://youtu.be/ABCDEFGHIJK';self.assertEqual(self.result()['status'],'review')
 def test_language_ranking_and_official_identity(self):
  self.assertEqual(p.lang_kind('官方双语','Author','Author'),'official_zh')
  self.assertEqual(p.lang_kind('官方双语','搬运者','Author'),'sub_zh')
  self.assertEqual(p.lang_kind('中文配音','搬运者','Author'),'dub_zh')
  self.assertLess(p.LANG_RANK['sub_zh'],p.LANG_RANK['dub_zh'])
 def test_network_failure_is_not_invalid(self):
  class Failing:
   def get(self,url):raise p.ApiError('timeout')
  with self.assertRaises(p.ApiError):p.evaluate(Failing(),self.o,{'bvid':'BV1234567890','status':'confirmed'})
 def test_explicit_deleted_is_invalid(self):
  class Deleted:
   def get(self,url):return {'code':-404}
  self.assertEqual(p.evaluate(Deleted(),self.o,{'bvid':'BV1234567890'})['status'],'invalid')
 def test_url_extractors(self):
  self.assertEqual(p.youtube_id('https://www.youtube.com/watch?v=abcdefghijk&x=1'),'abcdefghijk')
  self.assertEqual(p.identity_ids('https://www.youtube.com/watch?v=abcdefghijk&t=1'),{'abcdefghijk'})
  self.assertFalse(p.identity_ids('https://youtu.be/abcdefghijk123'))
 def test_cached_response_and_expiry(self):
  with tempfile.TemporaryDirectory() as temp:
   old=p.WORK;p.WORK=Path(temp)
   try:
    c=p.Client();u='https://example.test/';key=c.cache/(p.hashlib.sha256(u.encode()).hexdigest()+'.json')
    p.write(key,{'body':{'code':0,'data':[]}})
    self.assertEqual(c.get(u),{'code':0,'data':[]})
   finally:p.WORK=old

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
    p.write(p.WORK/'library.json',lib);p.build();d=p.read(root/'data.json')
    self.assertEqual(len(d['videos']),2);self.assertEqual(len(d['videos'][0]['versions']),1)
    lib[rows[1]['vid']]['candidates'][0]['page']=1;p.write(p.WORK/'library.json',lib);p.build()
    self.assertEqual(len(p.read(root/'data.json')['videos']),0)
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

if __name__=='__main__':unittest.main()
