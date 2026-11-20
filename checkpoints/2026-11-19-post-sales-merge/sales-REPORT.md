# Sales message eval: results (2026-11-19)

**Dataset:** "Sales Message Eval Set" artifact.
- 835 AI-generated messages across 6 channels and 12 stages.
- Each message has a quality label: 423 strong, 242 average, 170 weak.
- 397 messages have a buyer reply with a sentiment label.
- 36 pairs share a `pair_id`. 22 of them are weak-vs-strong for the same scenario; the other 14 are average-vs-strong.

**Read every result as "agrees with the dataset's labeller", not "works on real buyers".** The sellers, buyers and products are fictional. The quality labels and buyer replies appear to have been generated together with the messages, so they reflect the labeller's idea of good sales writing. Strong messages are also longer in every channel except voicemail, so the per-1,000-word rates in part 1 are partly confounded by length.

**Data quality issue:** the dataset's `word_count` field sums to 107,046 words, but the message text contains 95,895 words. That field is about 12% too high.

---

## 1. Ontology style markers vs labels (all 835 messages, scripted)

**Precision of each marker: when it appears, how often is the message labelled weak?** The base rate for weak is 20%.

| Marker (ontology) | Messages containing it | Weak | Strong |
|---|---|---|---|
| Superlatives such as "industry-leading" or "#1" (M14) | 29 | **90%** | 7% |
| "Transform", "unlock", "empower" wording | 12 | **92%** | 8% |
| Ceremonial preamble such as "hope this finds you well" or "my name is" (M01) | 49 | **73%** | 12% |
| Manufactured urgency | 22 | **73%** | 18% |
| Generic offload close such as "let me know" or "feel free" (M15) | 116 | 45% | 12% |
| Any of the five markers above | 179 | 54% | 14% |

Together, these five markers catch 56% of the weak messages. They are high-precision signals but miss almost half the weak set.

**Markers that point the other way in this dataset:**

| Marker | Messages containing it | Strong | Weak | What this means |
|---|---|---|---|---|
| Contrast frames such as "instead of X" or "rather than" (M20) | 80 | **85%** | 0% | Strong messages use them to explain how the product works, e.g. "managers approve instead of texting 14 people". M20 should only flag rhetorical contrasts, not contrasts that describe a mechanism. |
| Bracketed placeholders (M18) | 120 | **68%** | 12% | They appear mostly in call and video scripts. As a quality signal M18 doesn't apply here; it's an authenticity signal only. |
| Explicit opt-out, e.g. "if not, no worries" (H06/H12) | 23 | **87%** | 9% | This confirms the human pattern. |

**Within the 22 weak/strong pairs:**
- The strong message is longer in 21 of 22 pairs.
- The strong message has a wider spread of sentence lengths in 20 of 22 pairs, consistent with the revised M11.
- The weak message has more triplets in 8 pairs, the strong message in 2.
- The rates of "I", "we" and question marks are higher in weak messages, but that is mostly because they are shorter.

**Buyer replies:** no marker separates positive replies from negative ones or unsubscribes beyond what the quality label already explains. Reply sentiment follows the quality label almost exactly: 192 of 211 positive replies went to messages labelled strong.

---

## 2. Content coding (eval B): 60 messages, two blind coders

**Sample:** the 22 weak/strong pairs plus 16 randomly chosen average messages. The coders saw the channel, stage and buyer context, but not the quality label, the quality notes or the reply.

**Agreement:** the two coders, Opus and Haiku, agreed at r ≥ 0.70 on 13 of 14 features. The exception is disputable point of view, at r = 0.67.

**Reading the table:** separation runs from 0.5 (no signal) to 1.0 (always separates). "Pairs" counts the matched pairs where the feature favours the strong message, out of 22. Each cell shows Opus / Haiku.

| Content feature | Separation | Pairs |
|---|---|---|
| Share of sentences about the buyer rather than the seller | 0.93 / 0.93 | 20 / 21 |
| Names a pain specific to the buyer's industry or role | 0.91 / 0.98 | 18 / 21 |
| Explains how the product works, in the buyer's terms | 0.84 / 0.86 | 15 / 16 |
| Offers value before asking for time (a resource, scan or sample) | 0.84 / 0.84 | 15 / 15 |
| Smaller ask (weak messages ask for demos and long meetings) | 0.77 / 0.82 | 13 / 16 |
| Cites a trigger specific to this buyer | 0.77 / 0.80 | 12 / 13 |
| Takes a point of view that could be wrong | 0.77 / 0.73 | 13 / 11 |
| Fewer unsupported claims | 0.89 / 0.74 | 17 / 13 |
| Opens with a self-introduction | 0.55 / 0.52 | no signal |

No weak message explained how the product works, and no weak message offered anything before asking for time.

**Conclusion:** the strong/weak distinction in this dataset is about content: buyer focus, industry pain, mechanism, value offered first, a small ask. The clichés from part 1 are surface symptoms of weak content, and a style rewrite cannot add any of these content features.

---

## 3. Rewrite fidelity (eval A): 24 messages, counterbalanced judging

**Sample:** 12 weak and 12 average messages across all channels.

**Rewriter:** Sonnet, with guarded rules:
- Do not change the strength of any ask, deadline or claim.
- Do not turn a report into an assertion.
- Do not add enthusiasm.
- Change "we" to "I" only when "we" means the writer personally.

**Judges:** Opus and Haiku. Each judged every pair twice, once in each order.

**Quality did not change.**

| Judge | Labelled weak: original → rewrite | Labelled average: original → rewrite |
|---|---|---|
| Opus | 0.08 → 0.08 | 1.83 → 1.83 |
| Haiku | 0.67 → 0.62 | 1.62 → 1.67 |

Grades are on a 0–2 scale (weak, average, strong). A style pass does not turn a weak sales message into a good one.

**There was no stable preference for either version.** When a pair's verdict changed after the order was flipped, it counts as inconsistent:

| Judge | Inconsistent | Rewrite preferred in both orders | Original preferred in both orders |
|---|---|---|---|
| Opus | 17 of 24 | 5 | 2 |
| Haiku | 17 of 24 | 3 | 4 |

The earlier result that both judges preferred whichever text came first was position bias, and counterbalancing removes it.

**Meaning was preserved.** Judges rated 93 of 96 judgments "same meaning".
- Most of the changes were intended: filler and hype removed ("Honestly", "Thanks!", "Byeee", "I made this video JUST for you").
- **Breach of the strength rule:** S10-0005 turned a 45-minute demo floated as an option into a direct proposal. Both judges flagged it in both orders.
- **Claims removed:** two weak claims were removed rather than kept, "we're really fast" and "reps will thank you".

**The judges miss subtle strength changes.** The rewriter itself reported changing a price from "would be" to "is" in S06-0047. Only 1 of the 4 judging runs caught it. LLM judges are not reliable for small modal or hedge changes. Use a deterministic diff of modal verbs and hedges (would, could, may, might, typically, about, up to) as a gate before or alongside judging.

---

## 4. What this means for the ontology (proposed; not yet merged)

1. **Keep the high-precision sales clichés as detectors:** M14 superlatives, M01 preamble, transform wording, and manufactured urgency. Document their recall as roughly half.
2. **Narrow M20.** Contrasts that explain how the product works ("instead of …") are a mark of strong messages here. Flag only rhetorical contrasts against a strawman.
3. **Limit M18 to authenticity.** Placeholders are not a quality signal in templated scripts.
4. **Add content-level patterns from eval B as human patterns or checks.** These cannot be fixed by rewriting, so they need to be addressed when the message is drafted:
   - Most sentences are about the buyer.
   - Names an industry-specific pain.
   - Explains the mechanism.
   - Offers value before the ask.
   - Makes a small ask.
5. **Add a deterministic strength-drift check** to any rewrite pipeline. Judges catch big changes in asks, but missed 3 of 4 times on a single modal-verb change.

## Files

- `data/sales.jsonl`: the extracted dataset.
- `data/markers.json`: per-message marker scores.
- `markers.py`: part 1.
- `B_inputs/`, `B_key.json`, `B_codings/`, `score_B.py`: part 2.
- `A_originals/`, `A_rewrites/`, `A_pairs/`, `A_pair_key.json`, `A_judgments/`, `score_A.py`, `A_results.json`: part 3.
