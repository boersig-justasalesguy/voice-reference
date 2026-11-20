"""Compare scripted (prepared remarks) vs live (Q&A answers) executive speech, and human vs AI answers to the same analyst questions.

Usage: python3 -I score.py <scratch_earnings_dir>
"""
import os, sys, glob, json, statistics as st

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
from speech import speech_features  # noqa: E402

E = sys.argv[1]
F = ['words', 'sent_mean', 'sent_sd', 'short_pct', 'nominal_100', 'abstract_k', 'hedge_k', 'triplet_k', 'notbut_k',
     'I_k', 'we_k', 'you_k', 'num_k', 'opener_k', 'marker_k', 'contraction_k', 'repair_k', 'forward_k', 'stance_I_k',
     'deflect_k', 'first_sent_words', 'starts_with_marker']

def mean(rows, f): return st.mean(r[f] for r in rows) if rows else float('nan')

calls = sorted({os.path.basename(p).rsplit('_', 1)[0] for p in glob.glob(f'{E}/pooled/*_prepared.txt')})
prep = {c: speech_features(f'{E}/pooled/{c}_prepared.txt') for c in calls if os.path.getsize(f'{E}/pooled/{c}_prepared.txt') > 500}
qa = {c: speech_features(f'{E}/pooled/{c}_qa.txt') for c in calls if os.path.getsize(f'{E}/pooled/{c}_qa.txt') > 500}
both = sorted(set(prep) & set(qa))

key = json.load(open(f'{D}/exchange_key.json'))
human = [speech_features(f'{E}/human_answers/{x}.txt') for x in sorted(key)]
ai = {m: [speech_features(p) for p in sorted(glob.glob(f'{D}/ai_answers/{m}/*.txt'))] for m in ('haiku', 'sonnet', 'opus')}
ai_all = [r for v in ai.values() for r in v]

print(f'== Same executives, same call: prepared remarks vs live answers ({len(both)} calls); "live>prep" = calls where live is higher')
print('feature'.ljust(20) + 'prepared'.rjust(10) + 'live'.rjust(10) + '   live>prep')
for f in F:
    p = [prep[c][f] for c in both]; q = [qa[c][f] for c in both]
    print(f.ljust(20) + f'{st.mean(p):10.1f}{st.mean(q):10.1f}   {sum(b > a for a, b in zip(p, q)):2d}/{len(both)}')

print(f'\n== Answers to the same {len(human)} analyst questions: human exec vs AI (per-answer means)')
print('feature'.ljust(20) + 'human'.rjust(9) + 'AI all'.rjust(9) + ''.join(m.rjust(9) for m in ai) + '   AI>human (paired, AI-all mean per question)')
for f in F:
    paired = 0
    for i, x in enumerate(sorted(key)):
        vals = [st.mean([speech_features(p)[f]]) for p in glob.glob(f'{D}/ai_answers/*/{x}.txt')]
        if vals and st.mean(vals) > human[i][f]: paired += 1
    print(f.ljust(20) + f'{mean(human, f):9.1f}{mean(ai_all, f):9.1f}' + ''.join(f'{mean(ai[m], f):9.1f}' for m in ai) + f'   {paired:2d}/{len(human)}')

json.dump({'prepared': prep, 'live': qa, 'human_answers': human, 'ai_answers': ai},
          open(f'{D}/results.json', 'w'), indent=1)
