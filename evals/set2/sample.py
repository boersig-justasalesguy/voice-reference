"""Draw the content-coding (B) and rewrite (A) samples from data/sales.jsonl using the same rules and seeds as the set-1 sales eval.

B: every weak/strong pair + 16 random unpaired average messages, shuffled into M##.txt (labels hidden).
A: 12 weak messages from pairs + 12 average messages not used in B.
"""
import os, json, random, collections as C

D = os.path.dirname(os.path.abspath(__file__))
random.seed(835)
recs = {r['id']: r for r in (json.loads(l) for l in open(f'{D}/data/sales.jsonl') if l.strip())}

def ctx(r):
    b, s = r['buyer'], r['seller']
    return (f"CHANNEL: {r['channel']}\nSTAGE: {r['stage']}\nSELLER: {s['role']} at {r['product']}\n"
            f"BUYER: {b['title']}, {b['industry']}, {b['company']} ({b['company_size']} employees)\n"
            + (f"SUBJECT: {r['subject']}\n" if r.get('subject') else '') + f"MESSAGE:\n{r['message']}\n")

pairs = C.defaultdict(dict)
for r in recs.values():
    if r.get('pair_id'): pairs[r['pair_id']][r['quality']] = r
sw = [v for v in pairs.values() if 'weak' in v and 'strong' in v]
avg = [r for r in recs.values() if r['quality'] == 'average' and not r.get('pair_id')]

for d in ('B_inputs', 'A_originals', 'A_rewrites', 'A_pairs/order1', 'A_pairs/order2',
          'B_codings/opus', 'B_codings/haiku', 'A_judgments/opus/order1', 'A_judgments/opus/order2',
          'A_judgments/haiku/order1', 'A_judgments/haiku/order2'):
    os.makedirs(f'{D}/{d}', exist_ok=True)

bset = [v['weak'] for v in sw] + [v['strong'] for v in sw] + random.sample(avg, 16)
random.shuffle(bset); bkey = {}
for i, r in enumerate(bset):
    cid = f'M{i + 1:02d}'
    bkey[cid] = {'id': r['id'], 'quality': r['quality'], 'pair': r.get('pair_id'), 'channel': r['channel'], 'words': len(r['message'].split())}
    open(f'{D}/B_inputs/{cid}.txt', 'w').write(ctx(r))
json.dump(bkey, open(f'{D}/B_key.json', 'w'), indent=1)

used = {v['id'] for v in bkey.values()}
weak12 = random.sample([v['weak'] for v in sw], 12)
avg12 = random.sample([r for r in avg if r['id'] not in used], 12)
akey = {}
for r in weak12 + avg12:
    open(f"{D}/A_originals/{r['id']}.txt", 'w').write(ctx(r))
    akey[r['id']] = {'quality': r['quality'], 'channel': r['channel'], 'pair': r.get('pair_id')}
json.dump(akey, open(f'{D}/A_key.json', 'w'), indent=1)
print(f'B: {len(bkey)} messages {dict(C.Counter(v["quality"] for v in bkey.values()))}; '
      f'A: {len(akey)} messages {dict(C.Counter(v["quality"] for v in akey.values()))}')
