"""Score where a message sits between the AI default and the human target for its situation.

Usage:
  python3 -I tone/tone.py --situation live_exec_answer message.txt
  cat message.txt | python3 -I tone/tone.py --situation practitioner_post
  python3 -I tone/tone.py --list                      # available situations
  add --json for machine-readable output

Per feature:
  z_ai      standard deviations from the AI default mean (|z| < 1 = typical AI output)
  position  0 = AI default mean, 1 = human target mean (only for features where AI and human clearly differ, |d| >= 0.5)
  overshoot past the human target by more than 2 human standard deviations (sounds forced)
Overall position = |d|-weighted mean of per-feature positions (clipped to -0.5..1.5).
"""
import os, sys, json, glob, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from features import features, FEATURES  # noqa: E402

def load(name):
    p = f'{HERE}/references/{name}.json'
    if not os.path.exists(p):
        sys.exit(f'unknown situation {name!r}; run with --list')
    return json.load(open(p))

def score_features(x, ref):
    rows, num, den = [], 0.0, 0.0
    for f in FEATURES:
        a = ref['ai'][f]; sd_a = a['sd'] or 1e-9
        row = {'feature': f, 'label': FEATURES[f], 'value': x[f], 'ai_mean': a['mean'], 'z_ai': (x[f] - a['mean']) / sd_a}
        meta = ref['features'][f]
        if ref['human'] and meta['discriminative']:
            h = ref['human'][f]; gap = h['mean'] - a['mean']
            pos = (x[f] - a['mean']) / gap
            z_h = (x[f] - h['mean']) / (h['sd'] or 1e-9)
            row.update(human_mean=h['mean'], d=meta['d'], position=pos,
                       overshoot=bool(pos > 1 and z_h * (1 if gap > 0 else -1) > 2))
            w = abs(meta['d']); num += w * max(-0.5, min(1.5, pos)); den += w
        rows.append(row)
    return rows, (num / den if den else None)

def score(text, situation):
    ref = load(situation)
    x = features(text)
    rows, overall = score_features(x, ref)
    disc = [r for r in rows if 'position' in r]
    ai_typical = [r for r in rows if abs(r['z_ai']) < 1]
    if overall is None:
        verdict = 'no human target for this situation; showing deviation from the AI default only'
    elif overall < 0.33:
        verdict = 'reads like the AI default'
    elif overall < 0.67:
        verdict = 'between the AI default and the human target'
    else:
        verdict = 'within the human target range'
    warnings = []
    if x['_words'] < 60: warnings.append(f"short text ({x['_words']} words): per-1,000-word rates are noisy")
    if ref.get('proxy'): warnings.append('human target is a proxy (' + (ref.get('human_source') or '') + ')')
    warnings += [f"overshoot on {r['label']}: past the human target (sounds forced)" for r in disc if r['overshoot']]
    return {'situation': situation, 'label': ref['label'], 'words': x['_words'], 'overall_position': overall,
            'verdict': verdict, 'ai_typical_share': len(ai_typical) / len(rows), 'features': rows, 'warnings': warnings,
            'ai_source': ref['ai_source'], 'human_source': ref['human_source']}

def show(res):
    print(f"{res['label']}  ({res['words']} words)")
    if res['overall_position'] is not None:
        p = res['overall_position']; bar = int(round(max(0, min(1, p)) * 30))
        print(f"overall position {p:.2f}  AI default |{'-' * bar}●{'-' * (30 - bar)}| human target   -> {res['verdict']}")
    else:
        print(res['verdict'])
    print(f"{res['ai_typical_share']:.0%} of features are within 1 SD of typical AI output\n")
    print(f"{'feature':48s}{'value':>8s}{'AI':>8s}{'human':>8s}{'z_ai':>7s}{'pos':>7s}")
    for r in sorted(res['features'], key=lambda r: -abs(r.get('d') or 0)):
        hm = f"{r['human_mean']:8.1f}" if 'human_mean' in r else '       -'
        pos = f"{r['position']:7.2f}" if 'position' in r else '      -'
        print(f"{r['label'][:47]:48s}{r['value']:8.1f}{r['ai_mean']:8.1f}{hm}{r['z_ai']:7.1f}{pos}")
    for w in res['warnings']: print('! ' + w)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('file', nargs='?'); ap.add_argument('--situation'); ap.add_argument('--json', action='store_true')
    ap.add_argument('--list', action='store_true')
    a = ap.parse_args()
    if a.list:
        for p in sorted(glob.glob(f'{HERE}/references/*.json')):
            r = json.load(open(p)); print(f"{r['situation']:20s} {r['label']}  [AI n={r['n_ai']}, human n={r['n_human']}]")
        sys.exit()
    if not a.situation: sys.exit('--situation is required (see --list)')
    text = open(a.file, encoding='utf8').read() if a.file else sys.stdin.read()
    res = score(text, a.situation)
    print(json.dumps(res, indent=1)) if a.json else show(res)
