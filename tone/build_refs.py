"""Build per-situation reference distributions: the AI default vs the human target, feature by feature.

Usage: python3 -I tone/build_refs.py --human-root <dir>
  <dir> holds the human corpora (kept outside the repo for copyright):
    earnings/turns/*.json   parsed earnings-call turns
    g/b_*.txt               Gartner/IDC body texts
    latio/<slug>.txt        Latio posts
    classic/*.txt           classic letters
Only summary statistics (means, spreads, counts) are written to tone/references/; no source text.
"""
import os, sys, json, glob, argparse, statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from features import features, chunks, FEATURES  # noqa: E402

LATIO_EARLY = ['what-do-i-think-about-wiz-code', 'wtf-is-cdr-part-13', 'the-great-cnapp-re-bundle']

def read(p): return open(p, encoding='utf8', errors='ignore').read()

def txt_samples(paths, chunked):
    """(doc_id, features) pairs; long documents are chunked so units are message-sized."""
    out = []
    for p in paths:
        pieces = chunks(read(p)) if chunked else [read(p)]
        out += [(p, features(c)) for c in pieces if len(c.split()) >= 40]
    return out

def live_answer_samples(turn_files):
    out = []
    for p in turn_files:
        for i, t in enumerate(json.load(open(p))):
            if t['section'] == 'qa' and t['role'] == 'exec' and len(t['text'].split()) >= 60:
                out.append((p, features(t['text'])))
    return out

def sales_samples(paths):
    out = []
    for p in paths:
        for line in open(p):
            if line.strip():
                r = json.loads(line)
                out.append((f"{p}:{r['id']}", features(r['message'])))
    return out

def situations(hroot):
    ai_base = lambda nums: [f for n in nums for f in glob.glob(f'{ROOT}/baseline/ai_outputs/*/{n}.txt')]
    return {
        'live_exec_answer': dict(
            label='Executive answering a question live (call, meeting, live reply)',
            ai=lambda: txt_samples(glob.glob(f'{ROOT}/evals/earnings/ai_answers/*/*.txt'), chunked=False),
            human=lambda: live_answer_samples(sorted(glob.glob(f'{hroot}/earnings/turns/*.json'))),
            ai_src='Claude Haiku/Sonnet/Opus answering 24 analyst questions (72 answers)',
            human_src='Live executive answers, 12 earnings calls (src ES)', proxy=False),
        'analyst_report': dict(
            label='Analyst / research-firm writing',
            ai=lambda: txt_samples(ai_base(['01', '02', '03']), chunked=True),
            human=lambda: txt_samples(sorted(glob.glob(f'{hroot}/g/b_*.txt')), chunked=True),
            ai_src='AI baseline prompts 01-03 (9 texts, chunked)',
            human_src='Gartner/IDC public pieces 2019-2021 (src IN, chunked)', proxy=False),
        'practitioner_post': dict(
            label='Practitioner-analyst post (opinionated, first-hand)',
            ai=lambda: txt_samples(ai_base(['04', '05', '06']), chunked=True),
            human=lambda: txt_samples([f'{hroot}/latio/{s}.txt' for s in LATIO_EARLY], chunked=True),
            ai_src='AI baseline prompts 04-06 (9 texts, chunked)',
            human_src='Latio early posts 2024-25 (src PW, chunked)', proxy=False),
        'one_to_one_message': dict(
            label='One-to-one business message (PROXY human target: 19th-century letters)',
            ai=lambda: txt_samples(ai_base(['07', '08', '09', '10', '11']), chunked=False),
            human=lambda: txt_samples(sorted(glob.glob(f'{hroot}/classic/*.txt')), chunked=True),
            ai_src='AI baseline prompts 07-11 (15 messages)',
            human_src='Classic letters (src CL) - era mismatch, use as a rough proxy only', proxy=True),
        'sales_outreach': dict(
            label='Sales outreach (AI reference only - no human target yet)',
            ai=lambda: sales_samples([f'{ROOT}/evals/sales/data/sales.jsonl', f'{ROOT}/evals/set2/data/sales.jsonl']),
            human=None,
            ai_src='Both AI-generated sales sets (1,711 messages)',
            human_src=None, proxy=False),
    }

def summarize(samples):
    out = {}
    for f in FEATURES:
        v = [s[f] for _, s in samples]
        out[f] = {'mean': st.mean(v), 'sd': st.pstdev(v), 'n': len(v)}
    return out

def build(ai, human):
    ref = {'ai': summarize(ai), 'human': summarize(human) if human else None, 'features': {}}
    for f in FEATURES:
        a = ref['ai'][f]
        if human:
            h = ref['human'][f]
            pooled = ((a['sd'] ** 2 + h['sd'] ** 2) / 2) ** 0.5 or 1e-9
            d = (h['mean'] - a['mean']) / pooled
            ref['features'][f] = {'d': d, 'discriminative': abs(d) >= 0.5}
        else:
            ref['features'][f] = {'d': None, 'discriminative': False}
    return ref

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--human-root', required=True)
    args = ap.parse_args()
    os.makedirs(f'{HERE}/references', exist_ok=True)
    for name, cfg in situations(args.human_root).items():
        ai = cfg['ai'](); human = cfg['human']() if cfg['human'] else None
        ref = build(ai, human)
        ref.update(situation=name, label=cfg['label'], ai_source=cfg['ai_src'], human_source=cfg['human_src'],
                   proxy=cfg['proxy'], n_ai=len(ai), n_human=len(human) if human else 0)
        json.dump(ref, open(f'{HERE}/references/{name}.json', 'w'), indent=1)
        disc = [f for f, v in ref['features'].items() if v['discriminative']]
        print(f'{name:20s} ai={len(ai):5d} human={ref["n_human"]:4d} discriminative features={len(disc)}')
