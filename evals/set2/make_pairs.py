"""Build counterbalanced pairs: order1 has a random side first; order2 is the exact reverse. Context lines are shared."""
import os, json, random, re

D = os.path.dirname(os.path.abspath(__file__))
random.seed(1119)
akey = json.load(open(f'{D}/A_key.json'))
key = {}
for i, rid in enumerate(sorted(akey)):
    orig = open(f'{D}/A_originals/{rid}.txt').read()
    ctx, msg = orig.split('MESSAGE:\n', 1)
    subj = re.search(r'^SUBJECT: .*$', ctx, re.M)
    ctx = re.sub(r'^SUBJECT: .*\n', '', ctx, flags=re.M)
    o_text = (subj.group(0) + '\n' if subj else '') + msg.strip()
    r_text = open(f'{D}/A_rewrites/{rid}.txt').read().strip()
    pid = f'Q{i + 1:02d}'
    first = random.choice(['original', 'rewrite'])
    key[pid] = {'id': rid, 'order1_text1': first}
    texts = {'original': o_text, 'rewrite': r_text}
    second = 'rewrite' if first == 'original' else 'original'
    for folder, (a, b) in (('order1', (first, second)), ('order2', (second, first))):
        open(f'{D}/A_pairs/{folder}/{pid}.txt', 'w').write(f'{ctx.strip()}\n\n=== TEXT 1 ===\n{texts[a]}\n\n=== TEXT 2 ===\n{texts[b]}\n')
json.dump(key, open(f'{D}/A_pair_key.json', 'w'), indent=1)
print(len(key), 'pairs x 2 orders')
