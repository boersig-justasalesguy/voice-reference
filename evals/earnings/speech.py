"""Speech-specific features layered on the baseline metrics: discourse markers, contractions, repairs, stance markers, answer openings."""
import re, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'baseline'))
from metrics import analyze  # noqa: E402

# sentence- or turn-initial discourse markers ("So, ..." "Look, ..." "Yeah, ...")
OPENERS = r"(?:^|(?<=[.!?]\s))(so|well|look|yeah|yes|no|sure|okay|ok|right|and|but|listen|honestly|frankly|i mean|you know)\b[,]?"
MARKERS = r"\b(you know|i mean|kind of|sort of|i think|i guess|i'd say|let me|the way i'd|frankly|honestly|look|obviously|actually|basically|candidly|to be clear|again)\b"
CONTRACTIONS = r"\b\w+['’](s|re|ve|ll|d|t|m)\b"
REPAIRS = r"\b(\w+)\s+\1\b|--|—\s*(i mean|well|or|sorry)|\b(sorry|rather|or actually|let me rephrase)\b"
TRANSCRIPT_EDIT = r"\[(inaudible|technical difficulty|crosstalk|indiscernible)\]"
FORWARD = r"\b(we expect|we anticipate|we believe|we continue to|going forward|we remain|we're confident|we are confident)\b"
STANCE_I = r"\b(i think|i believe|i'd say|i would say|my view|i feel|i'm not sure|i don't know)\b"
DEFLECT = r"\b(we don't (break out|guide|disclose|comment)|not going to (comment|break out|get into)|too early to)\b"

def speech_features(path):
    base = analyze(path)
    t = open(path, encoding='utf8').read()
    low = ' '.join(t.lower().split())
    nw = max(base['words'], 1)
    k = lambda pat: 1000 * len(re.findall(pat, low)) / nw
    first = re.split(r'(?<=[.!?])\s+', low.strip(), maxsplit=1)[0] if low.strip() else ''
    return {
        **base,
        'opener_k': k(OPENERS),
        'marker_k': k(MARKERS),
        'contraction_k': k(CONTRACTIONS),
        'repair_k': k(REPAIRS),
        'forward_k': k(FORWARD),
        'stance_I_k': k(STANCE_I),
        'deflect_k': k(DEFLECT),
        'edited_marks': len(re.findall(TRANSCRIPT_EDIT, low)),
        'first_sent_words': len(first.split()),
        'starts_with_marker': int(bool(re.match(r"(so|well|look|yeah|yes|sure|okay|ok|great|thanks|thank you|good question|great question)\b", first))),
    }
