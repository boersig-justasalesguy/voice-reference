"""Insert a uniform Tags line into every marker (M##) and human pattern (H##) of human-voice-ontology.md, plus a tag legend.

Tags: src = evidence sources, ev = evidence type, ch = channels, reg = registers, status = validation state.
Re-running is safe: existing Tags lines are replaced.
"""
import re, sys

P = sys.argv[1] if len(sys.argv) > 1 else 'human-voice-ontology.md'

ALL_CH, ALL_REG = 'all', 'all'
T = {
    # markers
    'M01': ('CF CL SL', 'obs lab', 'email dm voicemail', 'stranger exec', 'confirmed-quality'),
    'M02': ('CF', 'obs', ALL_CH, ALL_REG, 'corpus-only'),
    'M03': ('CF CL', 'obs', ALL_CH, ALL_REG, 'corpus-only'),
    'M04': ('IN CF AB', 'obs meas', 'email dm', 'peer IC tech-buyer', 'revised: institutional-not-AI'),
    'M05': ('IN AB', 'obs meas', ALL_CH, ALL_REG, 'confirmed-AI-diff'),
    'M06': ('IN PW', 'obs', 'email dm', ALL_REG, 'corpus-only'),
    'M07': ('IN', 'obs', 'email dm', 'stranger peer exec', 'corpus-only'),
    'M08': ('IN', 'obs', ALL_CH, 'peer tech-buyer', 'corpus-only'),
    'M09': ('IN PW SL', 'obs code', ALL_CH, 'tech-buyer procurement', 'confirmed-quality'),
    'M10': ('IN PW', 'obs', 'long-form dm', 'peer tech-buyer', 'corpus-only'),
    'M11': ('IN CF AB SL', 'obs meas', ALL_CH, ALL_REG, 'revised: spread-not-length'),
    'M12': ('PW', 'obs', 'email dm', ALL_REG, 'corpus-only'),
    'M13': ('PW', 'obs', ALL_CH, ALL_REG, 'corpus-only'),
    'M14': ('IN PW SL', 'obs lab', 'email dm voicemail', 'stranger exec', 'confirmed-quality'),
    'M15': ('CF SL', 'obs lab', 'email dm', ALL_REG, 'partial: 45%-weak-precision'),
    'M16': ('AB', 'inf meas', ALL_CH, ALL_REG, 'unsupported'),
    'M17': ('IN CF', 'obs', 'email', 'exec', 'corpus-only'),
    'M18': ('AB SL', 'meas lab', 'email dm', ALL_REG, 'narrowed: authenticity-only'),
    'M19': ('AB CL', 'meas obs', 'email dm', 'stranger peer', 'confirmed-AI-diff; guarded'),
    'M20': ('AB PW SL', 'meas lab', ALL_CH, ALL_REG, 'narrowed: rhetorical-only'),
    'M21': ('AB PW', 'meas', 'long-form', 'tech-buyer peer', 'confirmed-AI-diff; vendor-list-bias'),
    'M22': ('SL', 'lab', 'email dm voicemail call', 'stranger exec', 'confirmed-quality (labeler only)'),
    'M23': ('SL', 'lab code', 'email dm call', 'stranger', 'confirmed-quality (labeler only)'),
    # human patterns
    'H01': ('CL PW', 'obs', ALL_CH, ALL_REG, 'corpus-only'),
    'H02': ('CL PW', 'obs', ALL_CH, 'peer tech-buyer stranger procurement', 'corpus-only'),
    'H03': ('PW', 'obs', 'long-form email dm', 'peer tech-buyer', 'corpus-only; coding-unreliable'),
    'H04': ('CL PW', 'obs', ALL_CH, ALL_REG, 'corpus-only'),
    'H05': ('CL PW AB', 'obs code', ALL_CH, 'tech-buyer IC procurement', 'confirmed-AI-diff'),
    'H06': ('CL SL', 'obs code lab', 'email dm', 'stranger exec', 'confirmed-quality'),
    'H07': ('CL', 'obs', 'email dm', 'peer stranger', 'corpus-only'),
    'H08': ('CL PW', 'obs', 'email dm', 'peer friction subordinate', 'corpus-only'),
    'H09': ('CL PW', 'obs', ALL_CH, 'peer tech-buyer exec', 'corpus-only; coding-unreliable'),
    'H10': ('CL PW AB SL', 'obs meas', ALL_CH, 'all-but-procurement', 'confirmed-AI-diff'),
    'H11': ('CL', 'obs', 'email', 'exec', 'corpus-only'),
    'H12': ('CF', 'obs', 'email dm', 'procurement friction', 'corpus-only'),
    'H13': ('PW RT', 'obs', 'long-form email', 'tech-buyer peer', 'corpus-only'),
    'H14': ('PW AB', 'obs code', 'long-form dm', 'peer tech-buyer', 'confirmed-AI-diff'),
    'H15': ('CL PW', 'obs', ALL_CH, ALL_REG, 'corpus-only'),
    'H16': ('PW', 'obs', 'dm long-form', 'peer IC', 'corpus-only'),
    'H17': ('RT CL', 'obs', ALL_CH, ALL_REG, 'corpus-only; sources-unverified'),
    'H18': ('SL', 'code lab', 'email dm voicemail call', 'stranger exec', 'confirmed-quality (labeler only)'),
    'H19': ('SL', 'code lab', 'email dm voicemail call', 'stranger exec', 'confirmed-quality (labeler only)'),
    'H20': ('SL', 'code lab', 'email dm call', 'tech-buyer exec', 'confirmed-quality (labeler only)'),
    'H21': ('SL', 'code lab', 'email dm', 'stranger exec', 'confirmed-quality (labeler only)'),
}

LEGEND = """### Tag scheme

Every marker (M##) and human pattern (H##) has a **Tags** line with five fields:

`src:` the corpus or corpora the evidence comes from.

| Code | Corpus |
|---|---|
| CL | Classic letters (Lincoln, Franklin, Darwin, Chekhov) |
| CF | Classic fiction dialogue (Austen) |
| RT | Rhetoric theory (Aristotle, Cicero; summarized from memory) |
| IN | Institutional analysts (Gartner/IDC) |
| PW | Practitioner writing (Latio) |
| AB | AI baseline (section 7) |
| SL | Labeled sales dataset (section 8) |
| ES | Earnings-call speech |
| BK | Books by genre (reserved for later) |

`ev:` what kind of evidence it is.

| Code | Evidence |
|---|---|
| obs | Qualitative observation in the source |
| meas | Scripted metric |
| code | Blind coding by two coders |
| lab | Agreement with dataset quality labels |
| inf | Inference or general knowledge only |

`ch:` the channels it applies to: email, dm, sms, voicemail, call, long-form, spoken, or all.

`reg:` the registers it applies to: stranger, exec, peer, IC, tech-buyer, procurement, friction, subordinate, or all.

`status:` how far it has been validated.

| Status | Meaning |
|---|---|
| confirmed-AI-diff | Separates AI text from human text in a matched baseline |
| confirmed-quality | Separates strong from weak messages, against dataset labels only |
| revised / narrowed | Scope changed by later evidence |
| partial | Weak precision |
| unsupported | Not borne out by the data |
| corpus-only | Seen in the human sources but not yet tested against AI or outcomes |

Transformations (section 4) inherit the tags of the marker they fix.

"""

text = open(P, encoding='utf8').read()
text = re.sub(r'\n- \*\*Tags:\*\*[^\n]*', '', text)
text = re.sub(r'### Tag scheme\n.*?(?=## 1\. Source profiles)', '', text, flags=re.S)

def add(m):
    head, cat = m.group(1), m.group(2)
    item = re.match(r'### ([MH]\d\d)\.', head).group(1)
    src, ev, ch, reg, status = T[item]
    return f"{head}{cat}\n- **Tags:** `src: {src}` · `ev: {ev}` · `ch: {ch}` · `reg: {reg}` · `status: {status}`"

text, n = re.subn(r'(### [MH]\d\d\.[^\n]*\n)(- \*\*Category:\*\*[^\n]*)', add, text)
text = text.replace('## 1. Source profiles', LEGEND + '## 1. Source profiles', 1)
open(P, 'w', encoding='utf8').write(text)
items = set(re.findall(r'### ([MH]\d\d)\.', text))
tagged = set(re.findall(r'### ([MH]\d\d)\.[^\n]*\n- \*\*Category:\*\*[^\n]*\n- \*\*Tags:\*\*', text))
print(f'tagged {n}; items {len(items)}; missing {sorted(items - tagged)}; unknown in table {sorted(set(T) - items)}')
