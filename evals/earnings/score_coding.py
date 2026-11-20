"""Score blind content coding of earnings-call answers: human exec vs each AI model; inter-coder agreement."""
import os, json, glob, statistics as st

D = os.path.dirname(os.path.abspath(__file__))
key = json.load(open(f'{D}/coding_key.json'))
coders = sorted(os.listdir(f'{D}/codings'))
SPONT = {'low': 0, 'medium': 1, 'high': 2}
SOURCES = ['human', 'haiku', 'sonnet', 'opus']

def feats(d):
    sq = max(d.get('sub_questions', 1) or 1, 1)
    b = lambda k: int(bool(d.get(k)))
    return {'answered_share': min(d.get('sub_questions_answered', 0), sq) / sq, 'direct_answer_first': b('direct_answer_first'),
            'pivots_to_talking_point': b('pivots_to_talking_point'), 'number_dump': b('number_dump'),
            'reasoning_or_mechanism': b('reasoning_or_mechanism'), 'concrete_example': b('concrete_example'),
            'owned_view': b('owned_view'), 'admits_uncertainty_or_limit': b('admits_uncertainty_or_limit'),
            'declines_or_deflects': b('declines_or_deflects'), 'enumerated_structure': b('enumerated_structure'),
            'triplet_count': d.get('triplet_count', 0), 'rapport_markers': d.get('rapport_markers', 0),
            'spontaneity': SPONT.get(d.get('spontaneity'), 0)}

data = {c: {os.path.basename(f)[:-5]: feats(json.load(open(f))) for f in glob.glob(f'{D}/codings/{c}/R*.json')} for c in coders}
F = list(feats({}).keys())
for c in coders:
    print(f'\n== Coder {c} ({len(data[c])} answers): mean by source')
    print('feature'.ljust(30) + ''.join(s.rjust(9) for s in SOURCES))
    for f in F:
        row = [st.mean([v[f] for r, v in data[c].items() if key[r]['source'] == s] or [float('nan')]) for s in SOURCES]
        print(f.ljust(30) + ''.join(f'{x:9.2f}' for x in row))
if len(coders) == 2:
    a, b = coders; common = sorted(set(data[a]) & set(data[b]))
    print(f'\n== Inter-coder agreement ({len(common)})')
    for f in F:
        x = [data[a][r][f] for r in common]; y = [data[b][r][f] for r in common]
        mx, my, sx, sy = st.mean(x), st.mean(y), st.pstdev(x), st.pstdev(y)
        rr = sum((i - mx) * (j - my) for i, j in zip(x, y)) / (len(x) * sx * sy) if sx and sy else float('nan')
        print(f'  {f:30s} exact {sum(i == j for i, j in zip(x, y)) / len(common):.0%}  r={rr:.2f}')
