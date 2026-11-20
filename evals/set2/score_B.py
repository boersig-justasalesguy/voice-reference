"""Score sales eval B: which content features separate the dataset's strong/average/weak labels; inter-coder agreement; within-pair tests."""
import os, json, glob, collections as C, statistics as st

D = os.path.dirname(os.path.abspath(__file__))
key = json.load(open(f'{D}/B_key.json'))
coders = sorted(os.listdir(f'{D}/B_codings'))
PROOF = {'none': 0, 'qualitative': 1, 'anonymous_quantified': 2, 'named_quantified': 3}
ASK = {'none': 0, 'reply_or_answer': 1, 'send_resource': 1, 'short_call_<=20min': 2, 'meeting_>20min_or_demo': 3, 'purchase_or_signature': 3}
PRESS = {'low': 0, 'medium': 1, 'high': 2}

def feats(d):
    b = lambda k: int(bool(d.get(k)))
    return {
        'buyer_specific_trigger': b('buyer_specific_trigger'), 'industry_specific_pain': b('industry_specific_pain'),
        'proof_level': PROOF.get(d.get('proof'), 0), 'unsupported_claims': d.get('unsupported_claims', 0),
        'feature_list_items': d.get('feature_list_items', 0), 'buyer_centric_pct': d.get('buyer_centric_sentences_pct', 0),
        'mechanism_explained': b('mechanism_explained'), 'ask_size': ASK.get(d.get('ask'), 0),
        'ask_pressure': PRESS.get(d.get('ask_pressure'), 0), 'opt_out': b('opt_out_offered'),
        'value_before_ask': b('value_before_ask'), 'manufactured_urgency': b('manufactured_urgency'),
        'self_intro_first': b('self_introduction_first'), 'disputable_pov': b('disputable_point_of_view'),
    }

data = {c: {os.path.basename(f)[:-5]: feats(json.load(open(f))) for f in glob.glob(f'{D}/B_codings/{c}/M*.json')} for c in coders}
F = list(feats({}).keys())

def auc(pos, neg):
    return sum((p > n) + 0.5 * (p == n) for p in pos for n in neg) / (len(pos) * len(neg)) if pos and neg else float('nan')

for c in coders:
    print(f'\n== Coder {c} ({len(data[c])} messages): means by dataset label, AUC strong>weak, within-pair wins')
    pairs = C.defaultdict(dict)
    for m, v in data[c].items():
        if key[m]['pair']: pairs[key[m]['pair']][key[m]['quality']] = v
    pairs = [p for p in pairs.values() if len(p) == 2]
    print('feature'.ljust(24) + 'strong'.rjust(8) + 'avg'.rjust(8) + 'weak'.rjust(8) + '  AUC   pairs s>w / s<w')
    for f in F:
        g = {q: [v[f] for m, v in data[c].items() if key[m]['quality'] == q] for q in ('strong', 'average', 'weak')}
        sw = sum(p['strong'][f] > p['weak'][f] for p in pairs); ws = sum(p['strong'][f] < p['weak'][f] for p in pairs)
        print(f.ljust(24) + ''.join(f'{st.mean(g[q]):8.2f}' for q in g) + f"  {auc(g['strong'], g['weak']):.2f}   {sw:2d} / {ws:2d}")

if len(coders) == 2:
    a, b = coders
    common = sorted(set(data[a]) & set(data[b]))
    print(f'\n== Inter-coder agreement ({len(common)} messages)')
    for f in F:
        x = [data[a][m][f] for m in common]; y = [data[b][m][f] for m in common]
        exact = sum(i == j for i, j in zip(x, y)) / len(common)
        mx, my, sx, sy = st.mean(x), st.mean(y), st.pstdev(x), st.pstdev(y)
        r = sum((i - mx) * (j - my) for i, j in zip(x, y)) / (len(x) * sx * sy) if sx and sy else float('nan')
        print(f'  {f:24s} exact {exact:.0%}  r={r:.2f}')
