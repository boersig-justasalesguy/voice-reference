"""Score eval B: content profile per group from blinded claim codings; inter-coder agreement."""
import os, json, glob, statistics as st, collections

B = os.path.dirname(os.path.abspath(__file__))
key = json.load(open(f'{B}/key.json'))
coders = sorted(os.listdir(f'{B}/codings'))
ORDER = ['AI analyst', 'Gartner/IDC', 'AI practitioner', 'Latio early', 'Latio transition', 'Latio late']

def profile(d, words):
    c = d.get('claims', [])
    n = len(c) or 1
    frac = lambda f: sum(1 for x in c if f(x)) / n
    return {
        'claims_per_100w': 100 * len(c) / words,
        'evidenced_%': 100 * frac(lambda x: x.get('evidence') not in ('none', 'reasoning_only')),
        'first_hand_%': 100 * frac(lambda x: x.get('evidence') == 'first_hand'),
        'data_cited_%': 100 * frac(lambda x: x.get('evidence') == 'data_cited'),
        'named_example_%': 100 * frac(lambda x: x.get('evidence') in ('named_example', 'named_source')),
        'no_support_%': 100 * frac(lambda x: x.get('evidence') == 'none'),
        'specific_%': 100 * frac(lambda x: x.get('specific')),
        'hedged_%': 100 * frac(lambda x: x.get('hedged')),
        'author_owned_%': 100 * frac(lambda x: x.get('owner') == 'author'),
        'prescriptive_%': 100 * frac(lambda x: x.get('type') == 'prescriptive'),
        'evaluative_%': 100 * frac(lambda x: x.get('type') == 'evaluative'),
        'predictive_%': 100 * frac(lambda x: x.get('type') == 'predictive'),
        'named_entities': d.get('named_entities', 0),
        'named_criticism': d.get('named_criticism', 0),
        'admitted_limits': d.get('admitted_limits', 0),
        'stake_disclosure': int(bool(d.get('stake_disclosure'))),
        'disputable_thesis': int(bool(d.get('disputable_thesis'))),
    }

per = {c: {} for c in coders}
for c in coders:
    for f in glob.glob(f'{B}/codings/{c}/T*.json'):
        tid = os.path.basename(f)[:-5]
        try:
            per[c][tid] = profile(json.load(open(f)), key[tid]['words'])
        except Exception as e:
            print('bad', c, tid, e)

METRICS = list(next(iter(next(iter(per.values())).values())).keys())
out = {}
for c in coders:
    print(f'\n== Coder: {c} ({len(per[c])} texts)')
    print('metric'.ljust(20) + ''.join(g[:16].rjust(17) for g in ORDER))
    out[c] = {}
    for m in METRICS:
        row = []
        for g in ORDER:
            vals = [v[m] for t, v in per[c].items() if key[t]['group'] == g]
            row.append(st.mean(vals) if vals else float('nan'))
            out[c].setdefault(g, {})[m] = row[-1]
        print(m.ljust(20) + ''.join(f'{x:17.1f}' for x in row))

if len(coders) == 2:
    a, b = coders
    common = sorted(set(per[a]) & set(per[b]))
    print(f'\n== Inter-coder agreement on {len(common)} texts (Pearson r of per-text values; binary = % agree)')
    def r(x, y):
        mx, my = st.mean(x), st.mean(y); sx, sy = st.pstdev(x), st.pstdev(y)
        return sum((i - mx) * (j - my) for i, j in zip(x, y)) / (len(x) * sx * sy) if sx and sy else float('nan')
    for m in METRICS:
        x = [per[a][t][m] for t in common]; y = [per[b][t][m] for t in common]
        if m in ('stake_disclosure', 'disputable_thesis'):
            print(f'  {m:20s} agree {sum(i == j for i, j in zip(x, y))}/{len(common)}')
        else:
            print(f'  {m:20s} r={r(x, y):.2f}')
    # does each coder rank AI vs human the same way on each metric?
    print('\n== Direction check: AI genre group vs its human comparison, does each coder agree on the sign?')
    for m in METRICS:
        signs = []
        for c in coders:
            ga = (out[c]['AI analyst'][m] - out[c]['Gartner/IDC'][m], out[c]['AI practitioner'][m] - out[c]['Latio early'][m])
            signs.append(tuple('+' if v > 0 else '-' if v < 0 else '0' for v in ga))
        print(f'  {m:20s} analyst-vs-Gartner / practitioner-vs-Latio-early: {a}={signs[0]} {b}={signs[1]}')

json.dump(out, open(f'{B}/results.json', 'w'), indent=1)
