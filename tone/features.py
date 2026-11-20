"""Feature extraction for the tone scorer.

Reuses the existing measurement code read-only (baseline/metrics.py via evals/earnings/speech.py); nothing there is modified.
All rates are per 1,000 words unless the name says otherwise.
"""
import os, re, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'evals', 'earnings'))
from speech import speech_features  # noqa: E402

FEATURES = {
    'triplet_k': 'lists of three ("X, Y and Z")',
    'notbut_k': 'contrast frames ("not X but Y", "rather than")',
    'num_k': 'numbers and figures',
    'opener_k': 'discourse openers ("So,", "Look,", "Yeah,")',
    'marker_k': 'stance markers ("I mean", "kind of", "you know")',
    'stance_I_k': 'first-person stance ("I think", "my view")',
    'hedge_k': 'hedges ("may", "probably", "likely")',
    'contraction_k': "contractions (it's, we're)",
    'repair_k': 'self-corrections and restarts',
    'forward_k': 'stock forward-looking phrases ("we expect", "going forward")',
    'courtesy_k': 'courtesy formulas ("happy to", "let me know")',
    'I_k': '"I / me / my"',
    'we_k': '"we / our / us"',
    'you_k': '"you / your"',
    'q_k': 'questions',
    'sent_sd': 'sentence-length spread (std dev, words)',
    'short_pct': 'share of sentences of 6 words or fewer (%)',
    'nominal_100': 'nominalizations per 100 words',
    'abstract_k': 'abstract enabling verbs ("enable", "drive", "leverage")',
}

def features(text):
    """Feature vector for one text."""
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False, encoding='utf8') as f:
        f.write(text); path = f.name
    try:
        full = speech_features(path)
    finally:
        os.unlink(path)
    out = {k: float(full[k]) for k in FEATURES}
    out['_words'] = full['words']
    return out

def chunks(text, size=150):
    """Split long text into ~size-word pieces at sentence boundaries, so long documents compare with short messages."""
    sents = re.split(r'(?<=[.!?])\s+', ' '.join(text.split()))
    out, cur = [], []
    for s in sents:
        cur.append(s)
        if sum(len(x.split()) for x in cur) >= size:
            out.append(' '.join(cur)); cur = []
    if cur and sum(len(x.split()) for x in cur) >= size // 2:
        out.append(' '.join(cur))
    return out
