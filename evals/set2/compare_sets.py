"""Compare two scored sales sets side by side: marker prevalence, precision against the weak label, and strong-vs-weak gaps.

Usage: python3 -I compare_sets.py <markers_A.json> <markers_B.json> [nameA] [nameB]
Inputs are the per-message outputs of markers.py.
"""
import sys, json, statistics as st, collections as C

A, B = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
na = sys.argv[3] if len(sys.argv) > 3 else 'set1'
nb = sys.argv[4] if len(sys.argv) > 4 else 'set2'
PRESENCE = ['superlative', 'transform', 'preamble', 'urgency', 'offload_close', 'opt_out', 'placeholders', 'notbut_k', 'triplet_k']
RATES = ['words', 'sent_sd', 'triplet_k', 'notbut_k', 'I_k', 'we_k', 'you_k', 'hedge_k', 'num_k', 'q_k']
CLICHE = ['superlative', 'transform', 'preamble', 'urgency', 'offload_close']

def label_mix(rows):
    c = C.Counter(r['quality'] for r in rows); n = len(rows)
    return {q: c[q] / n for q in ('strong', 'average', 'weak')}

def presence(rows, f):
    hit = [r for r in rows if r[f] > 0]
    c = C.Counter(r['quality'] for r in hit)
    return len(hit) / len(rows), (c['weak'] / len(hit) if hit else float('nan')), (c['strong'] / len(hit) if hit else float('nan'))

print(f'== Size and label mix\n  {na}: n={len(A)} ' + ' '.join(f'{k} {v:.0%}' for k, v in label_mix(A).items()) +
      f'\n  {nb}: n={len(B)} ' + ' '.join(f'{k} {v:.0%}' for k, v in label_mix(B).items()))

print('\n== Marker presence: share of messages containing it | share of those labelled weak | labelled strong')
print('marker'.ljust(16) + f'{na:>28s}{nb:>28s}')
for f in PRESENCE:
    a, b = presence(A, f), presence(B, f)
    print(f.ljust(16) + f'{a[0]:10.1%} {a[1]:7.0%} {a[2]:7.0%}' + f'{b[0]:12.1%} {b[1]:7.0%} {b[2]:7.0%}')
for name, rows in ((na, A), (nb, B)):
    hit = [r for r in rows if any(r[f] > 0 for f in CLICHE)]
    weak = [r for r in rows if r['quality'] == 'weak']
    c = C.Counter(r['quality'] for r in hit)
    print(f'  any cliché ({name}): present in {len(hit) / len(rows):.0%}; {c["weak"] / max(len(hit), 1):.0%} of those weak; catches {c["weak"] / max(len(weak), 1):.0%} of weak messages')

print('\n== Mean by label (strong / weak) per set')
print('feature'.ljust(12) + f'{na + " strong":>14s}{na + " weak":>12s}{nb + " strong":>14s}{nb + " weak":>12s}')
for f in RATES:
    g = lambda rows, q: st.mean([r[f] for r in rows if r['quality'] == q])
    print(f.ljust(12) + f'{g(A, "strong"):14.1f}{g(A, "weak"):12.1f}{g(B, "strong"):14.1f}{g(B, "weak"):12.1f}')

print('\n== Within-pair (weak vs strong, same scenario): pairs where weak is higher / lower')
for name, rows in ((na, A), (nb, B)):
    by = C.defaultdict(dict)
    for r in rows:
        if r.get('pair'): by[r['pair']][r['quality']] = r
    pairs = [v for v in by.values() if 'weak' in v and 'strong' in v]
    print(f'  {name}: {len(pairs)} weak/strong pairs')
    for f in ['words', 'sent_sd', 'triplet_k', 'notbut_k', 'superlative', 'preamble', 'opt_out', 'offload_close']:
        hi = sum(v['weak'][f] > v['strong'][f] for v in pairs); lo = sum(v['weak'][f] < v['strong'][f] for v in pairs)
        print(f'     {f:14s} weak higher {hi:2d} | lower {lo:2d}')

print('\n== Reply sentiment by label')
for name, rows in ((na, A), (nb, B)):
    print(f'  {name}:', dict(C.Counter((r['quality'], r['reply']) for r in rows).most_common(8)))
