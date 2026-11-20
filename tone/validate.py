"""Held-out check: build references on 70% of documents, score the other 30%, and see whether human text lands nearer 1 than AI text.

Splits are by document (all chunks of a document stay on one side). Repeated over 20 random splits.
Usage: python3 -I tone/validate.py --human-root <dir>
"""
import os, sys, random, argparse, statistics as st, collections, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_refs import situations, build  # noqa: E402
from tone import score_features  # noqa: E402

def split(samples, rng, frac=0.7):
    docs = sorted({d for d, _ in samples}); rng.shuffle(docs)
    train = set(docs[:max(1, int(len(docs) * frac))])
    return [s for s in samples if s[0] in train], [s for s in samples if s[0] not in train]

def auc(pos, neg):
    return sum((p > n) + 0.5 * (p == n) for p in pos for n in neg) / (len(pos) * len(neg)) if pos and neg else float('nan')

ap = argparse.ArgumentParser(); ap.add_argument('--human-root', required=True); a = ap.parse_args()
report = {}
for name, cfg in situations(a.human_root).items():
    if not cfg['human']: continue
    ai, hu = cfg['ai'](), cfg['human']()
    rng = random.Random(7); aucs, pa, ph = [], [], []
    for _ in range(20):
        ai_tr, ai_te = split(ai, rng); hu_tr, hu_te = split(hu, rng)
        if not ai_te or not hu_te: continue
        ref = build(ai_tr, hu_tr)
        sa = [score_features(x, ref)[1] for _, x in ai_te]; sh = [score_features(x, ref)[1] for _, x in hu_te]
        sa = [s for s in sa if s is not None]; sh = [s for s in sh if s is not None]
        aucs.append(auc(sh, sa)); pa.append(st.mean(sa)); ph.append(st.mean(sh))
    report[name] = {'auc_mean': st.mean(aucs), 'auc_min': min(aucs), 'ai_position_mean': st.mean(pa), 'human_position_mean': st.mean(ph),
                    'proxy': cfg['proxy'], 'n_ai': len(ai), 'n_human': len(hu)}
    print(f"{name:20s} held-out AUC {st.mean(aucs):.2f} (worst split {min(aucs):.2f}) | mean position: AI {st.mean(pa):.2f}, human {st.mean(ph):.2f}"
          + ('  [proxy target]' if cfg['proxy'] else ''))
json.dump(report, open(f'{HERE}/validation.json', 'w'), indent=1)
