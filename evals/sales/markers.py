"""Score every sales message on ontology markers; test which markers separate the dataset's quality labels and reply outcomes."""
import os, re, sys, json, tempfile, statistics as st, collections

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(D, '..', '..', 'baseline'))
from metrics import analyze  # noqa: E402

recs = [json.loads(l) for l in open(f'{D}/data/sales.jsonl')]

SUPERLATIVE = r"\b(industry[- ]leading|leading|#1|number one|world[- ]class|best[- ]in[- ]class|cutting[- ]edge|state[- ]of[- ]the[- ]art|revolutionary|innovative|premier|trusted by)\b"
PREAMBLE = r"\b(hope (this|you)[^.?!]{0,30}(well|great|good)|i wanted to (reach out|introduce|touch base)|my name is|just (checking|following) (in|up)|reaching out (to|because))\b"
TRANSFORM = r"\b(transform|unlock|empower|streamline|revolutioni[sz]e|supercharge|game[- ]chang\w*|take \w+ to the next level|digital transformation)\b"
URGENCY = r"\b(act now|urgent|time is running out|limited time|spots? (are )?filling|before it'?s too late|don'?t miss|expires?)\b"
OFFLOAD = r"\b(let me know|feel free|don'?t hesitate|happy to (help|chat|answer)|looking forward)\b"
OPTOUT = r"\b(if not,? no worries|ignore me|tell me and i'?ll stop|no (call|pressure) needed|if i'?ve misread|either answer|not (a fit|the right person)|won'?t add to it|under control)\b"

def feature_dump(t):
    # longest run of comma-separated items in one sentence
    best = 0
    for s in re.split(r'(?<=[.!?])\s+', t):
        best = max(best, s.count(',') + (1 if re.search(r'\b(and|or)\b', s) else 0))
    return best

rows = []
with tempfile.TemporaryDirectory() as tmp:
    for r in recs:
        t = r['message']
        p = os.path.join(tmp, r['id'] + '.txt'); open(p, 'w').write(t)
        a = analyze(p)
        low = t.lower()
        b = r['buyer']
        company_tokens = [w for w in re.split(r'\W+', b['company']) if len(w) > 3 and w.lower() not in ('group', 'systems', 'partners', 'health', 'software', 'company')]
        row = dict(
            id=r['id'], quality=r['quality'], reply=r.get('reply_sentiment') or 'none', channel=r['channel'], stage=r['stage'],
            pair=r.get('pair_id'),
            words=a['words'], sent_sd=a['sent_sd'], triplet_k=a['triplet_k'], notbut_k=a['notbut_k'], I_k=a['I_k'],
            we_k=a['we_k'], you_k=a['you_k'], hedge_k=a['hedge_k'], num_k=a['num_k'], q_k=a['q_k'], placeholders=a['placeholders'],
            superlative=len(re.findall(SUPERLATIVE, low)), preamble=len(re.findall(PREAMBLE, low)),
            transform=len(re.findall(TRANSFORM, low)), urgency=len(re.findall(URGENCY, low)),
            offload_close=len(re.findall(OFFLOAD, low)), opt_out=len(re.findall(OPTOUT, low)),
            feature_dump=feature_dump(t),
            names_company=int(any(re.search(r'\b' + re.escape(w) + r'\b', t) for w in company_tokens)),
            ends_with_question=int(bool(re.search(r'\?\s*(\n|$)', t.strip().rsplit('\n\n', 1)[0] + '\n') or re.search(r'\?\s*\n+\s*\S{0,40}\s*$', t.strip()))),
        )
        rows.append(row)
json.dump(rows, open(f'{D}/data/markers.json', 'w'))

FEATS = ['words', 'sent_sd', 'triplet_k', 'notbut_k', 'I_k', 'we_k', 'you_k', 'hedge_k', 'num_k', 'q_k', 'placeholders',
         'superlative', 'preamble', 'transform', 'urgency', 'offload_close', 'opt_out', 'feature_dump', 'names_company', 'ends_with_question']

def auc(pos, neg):
    # P(random pos > random neg); 0.5 = no signal
    if not pos or not neg: return float('nan')
    gt = sum((p > n) + 0.5 * (p == n) for p in pos for n in neg)
    return gt / (len(pos) * len(neg))

print('== Means by quality label')
print('feature'.ljust(20) + ''.join(q.rjust(10) for q in ('strong', 'average', 'weak')) + '   AUC(weak>strong)')
for f in FEATS:
    g = {q: [x[f] for x in rows if x['quality'] == q] for q in ('strong', 'average', 'weak')}
    print(f.ljust(20) + ''.join(f'{st.mean(g[q]):10.2f}' for q in g) + f"   {auc(g['weak'], g['strong']):.2f}")

print('\n== Reply outcome (positive vs negative/unsubscribe) within each quality label is not separable by design; overall AUC:')
pos = [x for x in rows if x['reply'] == 'positive']; neg = [x for x in rows if x['reply'] in ('negative', 'unsubscribe')]
for f in FEATS:
    print(f'  {f:20s} AUC(neg>pos)={auc([x[f] for x in neg], [x[f] for x in pos]):.2f}')

print('\n== Within-pair (36 weak/strong pairs, same scenario): share of pairs where weak > strong / weak < strong')
by = collections.defaultdict(dict)
for x in rows:
    if x['pair']: by[x['pair']][x['quality']] = x
pairs = [v for v in by.values() if 'weak' in v and 'strong' in v]
print('  pairs usable:', len(pairs))
for f in FEATS:
    hi = sum(v['weak'][f] > v['strong'][f] for v in pairs); lo = sum(v['weak'][f] < v['strong'][f] for v in pairs)
    print(f'  {f:20s} weak higher {hi:2d} | weak lower {lo:2d} | tie {len(pairs) - hi - lo:2d}')

print('\n== Quality x reply cross-tab (shows labels and replies were generated together)')
print(collections.Counter((x['quality'], x['reply']) for x in rows))
