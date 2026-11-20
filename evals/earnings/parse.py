"""Split earnings-call transcripts into speaker turns and tag role (operator / exec / analyst) and section (prepared / qa).

Usage: python3 -I parse.py <raw_dir> <out_dir>
Speaker labels vary by transcript vendor; a label is a short, repeated line that names a person (plus, for some layouts,
a title on the following line). Roles come from [Q]/[A] tags, analyst-firm keywords, or executive-title keywords.
"""
import os, re, sys, json, glob, collections

ANALYST = re.compile(r"\[Q\]|analyst|research|securities|capital|partners|bank\b|sachs|morgan|barclays|jefferies|cowen|wolfe|needham|piper|stifel|evercore|"
                     r"oppenheimer|baird|associate|northcoast|guggenheim|cantor|keybanc|rbc|ubs|bmo|citi|credit suisse|deutsche|wells fargo|"
                     r"raymond james|william blair|craig-hallum|lake street|rosenblatt|riley|mizuho|truist|suntrust|macquarie|canaccord|davidson|"
                     r"berenberg|bernstein|bofa|nomura|benchmark|northland|roth|wedbush|susquehanna|equity|\bllc\b|& co", re.I)
EXEC = re.compile(r"\[A\]|\bceo\b|\bcfo\b|chief|president|officer|vice president|\bvp\b|\bsvp\b|\bevp\b|investor relations|\bir\b|"
                  r"director|founder|treasurer|head|chair|controller|manager|general counsel", re.I)
IR = re.compile(r"investor relations|\bir\b|strategy and head", re.I)
END = re.compile(r"^(disclaimer|definitions|copyright|thomson reuters reserves|the information contained|this transcript may not)", re.I)

def is_sentence(line):
    s = line.strip()
    if re.search(r"(inc|llc|ltd|corp|co|plc|n\.v|s\.a|l\.p)\.\s*(\[[QA]\])?$", s, re.I):
        return False
    return bool(re.search(r"[.?!:\"”)]\s*$", s)) or len(s.split()) > 28

def parse(path):
    lines = [l.rstrip() for l in open(path, encoding='utf8', errors='ignore').read().split('\n')]
    for i, l in enumerate(lines):
        if i > len(lines) * 0.6 and END.match(l.strip()):
            lines = lines[:i]; break
    counts = collections.Counter(l.strip() for l in lines if l.strip())
    def label_at(i):
        s = lines[i].strip()
        if not s: return None
        if s.lower() in ('operator', 'unidentified participant', 'unidentified analyst', 'unknown speaker'): return s
        if s.startswith('[Unnamed speaker'): return s
        if re.search(r"\[[QA]\]$", s) and len(s) < 180: return s
        if counts[s] >= 2 and not is_sentence(s) and len(s) < 180 and re.search(r"[A-Z][a-z]+", s):
            return s
        return None
    turns, cur, buf, qa_seen = [], None, [], False
    i = 0
    while i < len(lines):
        lab = label_at(i)
        if lab:
            # two-line layout: name line followed by a repeated title/firm line
            if i + 1 < len(lines) and label_at(i + 1) and not label_at(i + 2 if i + 2 < len(lines) else i) is None and False:
                pass
            nxt = lines[i + 1].strip() if i + 1 < len(lines) else ''
            if nxt and counts[nxt] >= 2 and not is_sentence(nxt) and len(nxt.split()) <= 12 and not re.search(r"[A-Z][a-z]+ [A-Z]\.? ?[A-Z][a-z]+$", nxt) is None:
                lab = lab + ' | ' + nxt; i += 1
            if cur is not None and buf:
                turns.append({'label': cur, 'text': ' '.join(buf).strip()})
            cur, buf = lab, []
        elif cur is not None and lines[i].strip() and not re.match(r"^(QUESTIONS? AND ANSWERS?( SECTION)?|PRESENTATION|MANAGEMENT DISCUSSION SECTION)$", lines[i].strip(), re.I):
            buf.append(lines[i].strip())
        i += 1
    if cur is not None and buf:
        turns.append({'label': cur, 'text': ' '.join(buf).strip()})
    turns = [t for t in turns if len(t['text'].split()) >= 1]
    for t in turns:
        L = t['label']
        if re.match(r"operator", L, re.I): t['role'] = 'operator'
        elif '[Q]' in L or L.startswith('[Unnamed'): t['role'] = 'analyst'
        elif '[A]' in L: t['role'] = 'exec'
        elif ANALYST.search(L) and not re.search(r"\b(ceo|cfo|chief|officer|founder)\b", L, re.I): t['role'] = 'analyst'
        elif EXEC.search(L): t['role'] = 'exec'
        else: t['role'] = 'unknown'
        t['is_ir'] = bool(IR.search(L))
    # drop participant-list debris before the operator opens the call
    first_op = next((i for i, t in enumerate(turns) if t['role'] == 'operator'), 0)
    turns = turns[first_op:]
    # Q&A starts at the first operator turn that opens the queue, or the first analyst turn, whichever is earlier
    cue = re.compile(r"(first question|star[- ]?1|\*1|press star|question[- ]and[- ]answer session|operator instructions\]?\s*(your|our|the) (first|next))", re.I)
    seen = False
    for i, t in enumerate(turns):
        if t['role'] == 'analyst' or (i > 0 and t['role'] == 'operator' and cue.search(t['text'])): seen = True
        t['section'] = 'qa' if seen else 'prepared'
    return turns

if __name__ == '__main__':
    raw, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    for f in sorted(glob.glob(os.path.join(raw, '*.txt'))):
        turns = parse(f)
        name = os.path.basename(f)[:-4]
        json.dump(turns, open(os.path.join(out, name + '.json'), 'w'), indent=1)
        c = collections.Counter((t['section'], t['role']) for t in turns)
        w = collections.Counter()
        for t in turns: w[(t['section'], t['role'])] += len(t['text'].split())
        labels_unknown = sorted({t['label'][:60] for t in turns if t['role'] == 'unknown'})[:4]
        print(f"{name:13s} turns={len(turns):3d} prep_exec={c[('prepared','exec')]:2d}/{w[('prepared','exec')]:5d}w "
              f"qa_exec={c[('qa','exec')]:3d}/{w[('qa','exec')]:5d}w analyst={c[('qa','analyst')]:3d}/{w[('qa','analyst')]:5d}w "
              f"unknown={c[('prepared','unknown')] + c[('qa','unknown')]} {labels_unknown}")
