#!/usr/bin/env python3
"""Bounded search diagnostic: real guest requests, no login and no automatic retry."""
import json
from pipeline import Client, Blocked, ApiError, WORK, ROOT, now, write, urlencode, re, html

CASES = [
    ('3Blue1Brown 傅里叶变换', 'BV1pW411J7s8'),
    ('How to Speak Patrick Winston', 'BV1tU4y187xz'),
    ('3Blue1Brown 神经网络', 'BV1bx411M7Zx'),
]

def main():
    client = Client(delay=3)
    report = {'checked_at':now(), 'mode':'anonymous guest', 'search_session_version':2,
              'queries':[], 'stopped':False}
    for query, expected in CASES:
        try:
            response = client.get('https://api.bilibili.com/x/web-interface/search/type?' +
                                  urlencode({'search_type':'video','keyword':query,'page':1}), refresh=True)
            rows = response.get('data',{}).get('result',[])
            result = {'query':query, 'code':response.get('code'), 'result_count':len(rows),
                      'expected_bvid_found':any(r.get('bvid')==expected for r in rows),
                      'examples':[{'bvid':r.get('bvid'), 'title':html.unescape(re.sub('<[^>]*>','',r.get('title','')))}
                                  for r in rows[:3]]}
            report['queries'].append(result)
            print(json.dumps(result,ensure_ascii=False),flush=True)
        except (Blocked,ApiError) as error:
            report['queries'].append({'query':query,'error':str(error)})
            report['stopped']=True
            break
    report['guest_cookie_names']=sorted(c.name for c in client.cookie_jar)
    report['passed']=len(report['queries'])==len(CASES) and all(r.get('expected_bvid_found') for r in report['queries'])
    write(ROOT/'reports/search-health.json',report)
    return 0 if report['passed'] else 2

if __name__=='__main__':raise SystemExit(main())
