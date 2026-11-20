"""Score eval A: meaning preservation (from blinded judge units), human-voice preference, judge agreement, style deltas."""
import os, sys, json, glob, statistics as st, collections

A = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(A, '..', '..', 'baseline'))
from metrics import analyze  # noqa: E402

key = json.load(open(f'{A}/pair_key.json'))
judges = sorted(os.listdir(f'{A}/judgments'))
res = {j: {} for j in judges}

for j in judges:
    for pid, k in key.items():
        p = f'{A}/judgments/{j}/{pid}.json'
        if not os.path.exists(p):
            continue
        d = json.load(open(p))
        o_side = 'in_text1' if k['text1'] == 'original' else 'in_text2'
        r_side = 'in_text2' if o_side == 'in_text1' else 'in_text1'
        dropped, added, altered, kept = [], [], [], []
        for u in d['units']:
            # judges report strength change from Text 1 to Text 2; normalize to original -> rewrite
            if k['text1'] == 'rewrite' and u.get('altered') in ('strength_up', 'strength_down'):
                u['altered'] = 'strength_down' if u['altered'] == 'strength_up' else 'strength_up'
            ino, inr = bool(u.get(o_side)), bool(u.get(r_side))
            if ino and not inr: dropped.append(u)
            elif inr and not ino: added.append(u)
            elif ino and inr and u.get('altered'): altered.append(u)
            elif ino and inr: kept.append(u)
        n_orig = len(dropped) + len(altered) + len(kept)
        pick = d.get('more_human')
        pick = 'tie' if pick in ('tie', None) else ('rewrite' if k[f'text{pick}'] == 'rewrite' else 'original')
        res[j][pid] = dict(source=k['source'], n_orig=n_orig, dropped=dropped, added=added, altered=altered,
                           preserved=len(kept) / n_orig if n_orig else 0, same=d.get('same_meaning'), pick=pick,
                           reason=d.get('human_reason', ''))

print('== Meaning preservation (per judge)')
for j in judges:
    r = res[j].values()
    if not r: continue
    tot = lambda f: sum(len(x[f]) for x in r)
    print(f"{j}: pairs={len(r)} units_in_original={sum(x['n_orig'] for x in r)} preserved_unchanged={st.mean(x['preserved'] for x in r):.0%} "
          f"dropped={tot('dropped')} added={tot('added')} altered={tot('altered')} "
          f"same_meaning={dict(collections.Counter(x['same'] for x in r))} more_human={dict(collections.Counter(x['pick'] for x in r))}")
    kinds = collections.Counter((f, u.get('kind')) for x in r for f in ('dropped', 'added', 'altered') for u in x[f])
    print('   by kind:', dict(kinds))
    alt = collections.Counter(u.get('altered') for x in r for u in x['altered'])
    print('   alteration types:', dict(alt))

if len(judges) == 2:
    a, b = judges
    common = sorted(set(res[a]) & set(res[b]))
    agree_pick = sum(res[a][p]['pick'] == res[b][p]['pick'] for p in common)
    agree_same = sum(res[a][p]['same'] == res[b][p]['same'] for p in common)
    flag = lambda x: bool(x['dropped'] or x['added'] or x['altered'])
    agree_flag = sum(flag(res[a][p]) == flag(res[b][p]) for p in common)
    print(f'== Judge agreement on {len(common)} pairs: more_human {agree_pick}/{len(common)}, same_meaning {agree_same}/{len(common)}, any-meaning-change flag {agree_flag}/{len(common)}')
    both = [p for p in common if flag(res[a][p]) and flag(res[b][p])]
    print('   pairs both judges flag for meaning change:', [res[a][p]['source'] for p in both])

print('== Style deltas (original -> rewrite, mean of 15)')
KEYS = ['words', 'sent_sd', 'triplet_k', 'notbut_k', 'I_k', 'we_k', 'hedge_k', 'courtesy_k', 'offer_close', 'fmt_lines_pct', 'placeholders']
rows = collections.defaultdict(list)
for f in sorted(glob.glob(f'{A}/originals/*.txt')):
    rw = f.replace('/originals/', '/rewrites/')
    if os.path.exists(rw):
        o, w = analyze(f), analyze(rw)
        for k in KEYS: rows[k].append((o[k], w[k]))
for k in KEYS:
    print(f"  {k:14s} {st.mean(x for x, _ in rows[k]):7.1f} -> {st.mean(y for _, y in rows[k]):7.1f}")

json.dump({j: {p: {k: v for k, v in x.items()} for p, x in res[j].items()} for j in judges},
          open(f'{A}/results.json', 'w'), indent=1, default=str)
