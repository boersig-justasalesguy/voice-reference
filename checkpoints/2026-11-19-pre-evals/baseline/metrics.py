import re, sys, os, glob, json, statistics as st

S = os.path.dirname(os.path.abspath(__file__))

GROUPS = {
    'AI analyst (01-03)':      [f'{S}/ai/{m}/{n}.txt' for m in ('haiku','sonnet','opus') for n in ('01','02','03')],
    'AI practitioner (04-06)': [f'{S}/ai/{m}/{n}.txt' for m in ('haiku','sonnet','opus') for n in ('04','05','06')],
    'AI B2B message (07-11)':  [f'{S}/ai/{m}/{n}.txt' for m in ('haiku','sonnet','opus') for n in ('07','08','09','10','11')],
    'Gartner/IDC':             sorted(glob.glob(f'{S}/g/b_*.txt')),
    'Latio early (2024-25)':   [f'{S}/latio/{s}.txt' for s in ('what-do-i-think-about-wiz-code','wtf-is-cdr-part-13','the-great-cnapp-re-bundle')],
    'Latio transition (Dec25)': [f'{S}/latio/{s}.txt' for s in ('emerging-categories-the-evolution','the-5-security-features-that-will')],
    'Latio late (2026)':       [f'{S}/latio/{s}.txt' for s in ('the-complete-guide-to-preventing','the-privatization-of-vulnerability','the-new-normal-what-the-recent-incidents')],
    'Classic letters':         [f'{S}/classic/{s}.txt' for s in ('lincoln_hooker','lincoln_greeley','lincoln_bixby','darwin_gray','chekhov_nikolay','chekhov_suvorin_1888')],
    'Collins letter':          [f'{S}/classic/austen_collins_letter.txt'],
}

ABSTRACT = r'\b(enabl\w*|driv(e|es|ing|en)|leverag\w*|facilitat\w*|transform\w*|empower\w*|streamlin\w*|optimi[sz]\w*|ensur\w*|enhanc\w*|foster\w*|unlock\w*)\b'
HEDGE = r'\b(may|might|could|perhaps|potentially|possibly|likely|arguably|somewhat|probably|maybe)\b|\bcan help\b|\bit seems\b'
TICS = r'\b(delve\w*|landscape|navigat\w*|journey|harness\w*|robust|seamless\w*|crucial|pivotal|moreover|furthermore|additionally|ultimately|tapestry|realm|game-changer|elevate|comprehensive|holistic|ever-evolving|rapidly evolving|in today\'s|it\'s worth noting|in conclusion|in summary|key takeaways?)\b'
COURTESY = r'\b(i hope (this|you)|hope this|i\'d love|excited|happy to|feel free|don\'t hesitate|looking forward|reach(ing)? out|thank you for (your )?time|i appreciate|appreciate (your|any)|let me know)\b'
TRIPLET = r'\b[\w-]+(?: [\w-]+){0,2}, [\w-]+(?: [\w-]+){0,2},? (?:and|or) [\w-]+'
NOTBUT = r'\bnot (just|only|merely)\b|\bnot \w+(?: \w+){0,3},? but\b|\brather than\b'

def analyze(path):
    raw = open(path, encoding='utf8', errors='ignore').read()
    raw = re.sub(r'(?m)^Subject:.*$', '', raw)
    placeholders = len(re.findall(r'\[[^\]\n]{1,80}\]', raw))
    raw = re.sub(r'\[[^\]\n]{1,80}\]', 'X', raw)
    lines = [l for l in raw.split('\n') if l.strip()]
    fmt = sum(1 for l in lines if re.match(r'\s*([-*•]|#{1,6}|\d+[.)])\s', l))
    bold = len(re.findall(r'\*\*[^*]+\*\*', raw))
    t = re.sub(r'[*#_`>|]', ' ', raw)
    t = re.sub(r'^\s*([-•]|\d+[.)])\s+', '', t, flags=re.M)
    flat = ' '.join(t.split())
    words = flat.split(); nw = len(words); low = flat.lower()
    sents = [s for s in re.split(r'(?<=[.!?…])[”"’)]*\s+(?=[“"(A-Z0-9])', flat) if len(s.split()) >= 1]
    L = [len(s.split()) for s in sents]
    mean = st.mean(L); sd = st.pstdev(L)
    # proper-noun proxy: capitalized tokens not at sentence start, not I / I'm etc.
    caps = 0
    for s in sents:
        toks = s.split()[1:]
        caps += sum(1 for w in toks if re.match(r'^[A-Z][A-Za-z0-9]+', w) and not re.match(r"^I('|’|$)", w))
    per_k = lambda n: 1000 * n / nw
    tail = ' '.join(sents[-3:]).lower()
    return dict(
        words=nw, sents=len(L), sent_mean=mean, sent_sd=sd, sent_cv=sd/mean if mean else 0,
        short_pct=100*sum(1 for x in L if x <= 6)/len(L),
        nominal_100=100*len(re.findall(r'\b\w+(?:tion|ment|ity|ness|ance|ence)s?\b', low))/nw,
        abstract_k=per_k(len(re.findall(ABSTRACT, low))),
        hedge_k=per_k(len(re.findall(HEDGE, low))),
        will_k=per_k(len(re.findall(r'\bwill\b', low))),
        tic_k=per_k(len(re.findall(TICS, low))),
        courtesy_k=per_k(len(re.findall(COURTESY, low))),
        triplet_k=per_k(len(re.findall(TRIPLET, flat))),
        notbut_k=per_k(len(re.findall(NOTBUT, low))),
        I_k=per_k(len(re.findall(r"\b(i|me|my|i'm|i’m|i've|i’ve|i'd|i’d)\b", low))),
        we_k=per_k(len(re.findall(r'\b(we|our|us)\b', low))),
        you_k=per_k(len(re.findall(r'\b(you|your)\b', low))),
        num_k=per_k(len(re.findall(r'\b\d[\d,.%]*\b|\$\d', flat))),
        caps_100=100*caps/nw,
        emdash_k=per_k(flat.count('—') + flat.count(' - ') + flat.count('--')),
        q_k=per_k(flat.count('?')),
        fmt_lines_pct=100*fmt/len(lines), bold=bold,
        offer_close=int(bool(re.search(COURTESY, tail))),
        placeholders=placeholders,
    )

KEYS = ['words','sent_mean','sent_sd','sent_cv','short_pct','nominal_100','abstract_k','hedge_k','will_k','tic_k','courtesy_k',
        'triplet_k','notbut_k','I_k','we_k','you_k','num_k','caps_100','emdash_k','q_k','fmt_lines_pct','offer_close','placeholders']

if __name__ == '__main__':
    out = {}
    for g, files in GROUPS.items():
        files = [f for f in files if os.path.exists(f) and os.path.getsize(f) > 0]
        rows = [analyze(f) for f in files]
        if not rows: continue
        out[g] = {'n': len(rows), **{k: st.mean(r[k] for r in rows) for k in KEYS},
                  'per_doc': {os.path.relpath(f, S): rows[i] for i, f in enumerate(files)}}
    json.dump(out, open(f'{S}/metrics.json', 'w'), indent=1)
    hdr = ['group','n'] + KEYS
    print('\t'.join(hdr))
    for g, d in out.items():
        print('\t'.join([g, str(d['n'])] + [f"{d[k]:.1f}" if k not in ('offer_close',) else f"{d[k]:.2f}" for k in KEYS]))
