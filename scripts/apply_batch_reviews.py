import sys, os, json, datetime
sys.path.insert(0, 'scripts')
import pipeline

def apply_batch(batch_file):
    with open(batch_file) as f:
        items = json.load(f)

    with open('reports/manual-identity-reviews.json') as f:
        reviews_data = json.load(f)

    rev_list = reviews_data.get('reviews', [])
    existing_pairs = {(r['id'], r['bvid']) for r in rev_list}

    lib = pipeline.read(pipeline.WORK / 'library.json', {})
    bad_flags = {'conflicting years', 'conflicting episode', 'possibly abridged', 'derivative content requires review', 'missing segment', 'missing segment duration'}

    applied = 0
    now_str = pipeline.now()

    for it in items:
        vid = it['vid']
        bvid = it['bvid']
        page = it['page']
        cid = it['cid']
        diff = it['diff']
        evidence = (
            f"Codex内容与元数据复核：原片为[{it['orig_ch']}]《{it['orig_title']}》（{it['orig_dur']}秒）。"
            f"B站BV号{bvid}第{page}P《{it['bili_title']}》，UP主[{it['bili_up']}]，时长{it['bili_dur']}秒对齐（相差{diff}秒），"
            f"CID {cid}。元数据与时长高度一致。未做逐帧比较。"
        )

        e = lib.get(vid)
        if not e:
            print(f"Error: {vid} not in library")
            continue
        c = next((cand for cand in e['candidates'] if cand['bvid'] == bvid), None)
        if not c:
            print(f"Error: candidate {bvid} not found for {vid}")
            continue

        if c.get('availability') != 'available' or c.get('page') != page:
            print(f"Error: {vid} {bvid} page/availability mismatch")
            continue
        if set(c.get('flags', [])) & bad_flags:
            print(f"Error: {vid} {bvid} has conflict flags {c.get('flags')}")
            continue

        c['manual_review'] = {'at': now_str, 'evidence': evidence}
        c['evidence'] = [evidence]
        c['status'] = 'confirmed'
        e['status'] = pipeline.entry_status(e['candidates'])

        if (vid, bvid) not in existing_pairs:
            rev_list.append({
                'id': vid,
                'bvid': bvid,
                'page': page,
                'decision': 'confirmed',
                'reviewer': 'Codex',
                'evidence_type': 'supplemental content and metadata verification',
                'reviewed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'evidence': evidence,
                'frame_by_frame_comparison': False
            })
            existing_pairs.add((vid, bvid))
        applied += 1

    pipeline.write(pipeline.WORK / 'library.json', lib)
    pipeline.report(lib)

    reviews_data['reviews'] = rev_list
    with open('reports/manual-identity-reviews.json', 'w') as f:
        json.dump(reviews_data, f, ensure_ascii=False, indent=2)

    pipeline.build()
    print(f"Successfully applied {applied}/{len(items)} reviews and rebuilt.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/apply_batch_reviews.py <batch_file.json>")
        sys.exit(1)
    apply_batch(sys.argv[1])
