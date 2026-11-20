"""Score every message in a JSONL file against one or more situations; write a per-message CSV and print a summary.

Usage: python3 -I tone/batch.py <messages.jsonl> <out.csv> --situations one_to_one_message sales_outreach [--name set1]
Each JSONL record needs "id" and "message"; "quality" and "channel" are used for the summary if present.
"""
import os, sys, csv, json, argparse, statistics as st, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from tone import score  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument('infile'); ap.add_argument('outfile'); ap.add_argument('--situations', nargs='+', required=True); ap.add_argument('--name', default='')
a = ap.parse_args()
recs = [json.loads(l) for l in open(a.infile) if l.strip()]
rows = []
for r in recs:
    row = {'set': a.name, 'id': r['id'], 'channel': r.get('channel', ''), 'quality': r.get('quality', '')}
    for s in a.situations:
        res = score(r['message'], s)
        row[f'{s}_position'] = res['overall_position']
        row[f'{s}_ai_typical_share'] = res['ai_typical_share']
        row[f'{s}_overshoot'] = sum(1 for f in res['features'] if f.get('overshoot'))
        row['words'] = res['words']
    rows.append(row)
with open(a.outfile, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

def summ(vals): return f'{st.mean(vals):.2f}' if vals else '  -'
for s in a.situations:
    key = f'{s}_position' if rows[0][f'{s}_position'] is not None else f'{s}_ai_typical_share'
    kind = 'position (0=AI, 1=human)' if key.endswith('position') else 'share of features within typical AI range'
    print(f'\n== {a.name} on {s}: mean {kind}')
    by_q = collections.defaultdict(list); by_c = collections.defaultdict(list)
    for r in rows:
        if r[key] is not None: by_q[r['quality']].append(r[key]); by_c[r['channel']].append(r[key])
    print('  by label:   ' + '  '.join(f'{q} {summ(v)}' for q, v in sorted(by_q.items())))
    print('  by channel: ' + '  '.join(f'{c} {summ(v)}' for c, v in sorted(by_c.items())))
    allv = [r[key] for r in rows if r[key] is not None]
    print(f'  overall {summ(allv)}; overshoot flags in {sum(1 for r in rows if r[f"{s}_overshoot"])} messages')
