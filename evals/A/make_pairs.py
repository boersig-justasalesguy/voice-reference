"""Build blinded pairs (original vs rewrite, random order) for eval A judges."""
import os, glob, random, json

A = os.path.dirname(os.path.abspath(__file__))
random.seed(20261119)
key = {}
for f in sorted(glob.glob(f'{A}/originals/*.txt')):
    name = os.path.basename(f)[:-4]
    rw = f'{A}/rewrites/{name}.txt'
    if not os.path.exists(rw):
        print('missing rewrite', name); continue
    texts = [('original', open(f).read().strip()), ('rewrite', open(rw).read().strip())]
    random.shuffle(texts)
    pid = f'P{len(key) + 1:02d}'
    key[pid] = {'source': name, 'text1': texts[0][0], 'text2': texts[1][0]}
    with open(f'{A}/pairs/{pid}.txt', 'w') as out:
        out.write(f'=== TEXT 1 ===\n{texts[0][1]}\n\n=== TEXT 2 ===\n{texts[1][1]}\n')
json.dump(key, open(f'{A}/pair_key.json', 'w'), indent=1)
print(len(key), 'pairs')
