#!/usr/bin/env python3
"""Fetch only public HackerTube metadata; validate before replacing current snapshot."""
import datetime, hashlib, json, tempfile, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
files={'manifest.json':'api/export','DATA.md':'download/DATA.md','videos.jsonl':'download/videos.jsonl','taxonomy.json':'download/taxonomy.json','browse.json':'api/browse'}
with tempfile.TemporaryDirectory() as temp:
    stage=Path(temp);provenance={}
    for name,route in files.items():
        url='https://hackertube.org/'+route
        with urllib.request.urlopen(url,timeout=60) as r:body=r.read()
        (stage/name).write_bytes(body)
        provenance[name]={'url':url,'sha256':hashlib.sha256(body).hexdigest(),'bytes':len(body)}
    manifest=json.loads((stage/'manifest.json').read_text())
    rows=[json.loads(line) for line in (stage/'videos.jsonl').read_text().splitlines()]
    assert len(rows)==manifest['videos']==len({x['vid'] for x in rows})
    tax=json.loads((stage/'taxonomy.json').read_text())
    assert all('id' in a and 'categories' in a for a in tax['areas'])
    dest=ROOT/'data/source';dest.mkdir(parents=True,exist_ok=True)
    # Keep the previous immutable source set locally for recovery; do not duplicate it publicly.
    old=json.loads((dest/'provenance.json').read_text()) if (dest/'provenance.json').exists() else None
    if old:
        archive=ROOT/'data/work/source-history'/hashlib.sha256(json.dumps(old,sort_keys=True).encode()).hexdigest()[:16]
        archive.mkdir(parents=True,exist_ok=True)
        for path in dest.iterdir():
            if path.is_file() and not (archive/path.name).exists():(archive/path.name).write_bytes(path.read_bytes())
    for name in files:(dest/name).write_bytes((stage/name).read_bytes())
    (dest/'provenance.json').write_text(json.dumps({'fetched_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':provenance},ensure_ascii=False,indent=2)+'\n')
    print(f'Imported {len(rows)} originals; {len(tax["areas"])} areas')
