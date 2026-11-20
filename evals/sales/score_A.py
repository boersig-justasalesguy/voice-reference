"""Score sales eval A: meaning drift, order-corrected preference, and quality grade of original vs rewrite."""
import os, json, collections as C, statistics as st

D = os.path.dirname(os.path.abspath(__file__))
key = json.load(open(f'{D}/A_pair_key.json'))
akey = json.load(open(f'{D}/A_key.json'))
GRADE = {'weak': 0, 'average': 1, 'strong': 2}

def side_map(pid, order):
    first = key[pid]['order1_text1']
    other = 'rewrite' if first == 'original' else 'original'
    return {'1': first, '2': other} if order == 'order1' else {'1': other, '2': first}

out = C.defaultdict(dict)  # (judge) -> pid -> order -> parsed
for judge in sorted(os.listdir(f'{D}/A_judgments')):
    for order in ('order1', 'order2'):
        folder = f'{D}/A_judgments/{judge}/{order}'
        if not os.path.isdir(folder): continue
        for pid in key:
            p = f'{folder}/{pid}.json'
            if not os.path.exists(p): continue
            d = json.load(open(p)); sm = side_map(pid, order)
            o, r = ('in_text1', 'in_text2') if sm['1'] == 'original' else ('in_text2', 'in_text1')
            dropped = [u for u in d['units'] if u.get(o) and not u.get(r)]
            added = [u for u in d['units'] if u.get(r) and not u.get(o)]
            altered = [u for u in d['units'] if u.get(o) and u.get(r) and u.get('altered')]
            pick = d.get('better_message')
            out[judge].setdefault(pid, {})[order] = dict(
                dropped=dropped, added=added, altered=altered, same=d.get('same_meaning'),
                pick=sm.get(pick, 'tie'), pos=pick,
                grade_orig=GRADE.get(d.get(f"grade_text{'1' if sm['1'] == 'original' else '2'}")),
                grade_rw=GRADE.get(d.get(f"grade_text{'1' if sm['1'] == 'rewrite' else '2'}")))

for judge, res in out.items():
    print(f'\n== Judge {judge}: {len(res)} pairs')
    allv = [v for x in res.values() for v in x.values()]
    print('  position of pick (all orders):', dict(C.Counter(v['pos'] for v in allv)))
    # order-corrected preference: a pair counts for the rewrite only if picked in both orders
    both = [x for x in res.values() if len(x) == 2]
    cons = C.Counter('rewrite' if all(v['pick'] == 'rewrite' for v in x.values()) else
                     'original' if all(v['pick'] == 'original' for v in x.values()) else 'inconsistent' for x in both)
    print('  better message, consistent across both orders:', dict(cons))
    for q in ('weak', 'average'):
        sub = [x for pid, x in res.items() if akey[key[pid]['id']]['quality'] == q and len(x) == 2]
        c = C.Counter('rewrite' if all(v['pick'] == 'rewrite' for v in x.values()) else
                      'original' if all(v['pick'] == 'original' for v in x.values()) else 'inconsistent' for x in sub)
        go = [st.mean([v['grade_orig'] for v in x.values() if v['grade_orig'] is not None]) for x in sub]
        gr = [st.mean([v['grade_rw'] for v in x.values() if v['grade_rw'] is not None]) for x in sub]
        print(f'  dataset label {q:7s}: preference {dict(c)}; mean grade original {st.mean(go):.2f} -> rewrite {st.mean(gr):.2f} (0=weak,1=avg,2=strong)')
    drift = C.Counter((f, u.get('kind'), u.get('altered')) for v in allv for f in ('dropped', 'added', 'altered') for u in v[f])
    print('  meaning changes (summed over both orders):', dict(drift))
    print('  same_meaning:', dict(C.Counter(v['same'] for v in allv)))
    flagged = sorted({key[pid]['id'] for pid, x in res.items() if all(v['dropped'] or v['added'] or v['altered'] for v in x.values())})
    print('  flagged for a meaning change in BOTH orders:', flagged)
    for pid, x in res.items():
        if key[pid]['id'] in flagged:
            for f in ('dropped', 'added', 'altered'):
                for u in x['order1'][f]:
                    print(f"     {key[pid]['id']} {f} {u.get('kind')} {u.get('altered') or ''} | {u.get('unit')} | {u.get('note') or ''}")

json.dump({j: r for j, r in out.items()}, open(f'{D}/A_results.json', 'w'), indent=1, default=str)
