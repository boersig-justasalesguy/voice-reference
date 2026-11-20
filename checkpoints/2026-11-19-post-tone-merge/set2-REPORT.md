# Sales eval: set 1 vs set 2 (2026-11-19)

| | Set 1 | Set 2 |
|---|---|---|
| Source | "Sales Message Eval Set" artifact, run at `evals/sales/` | `~/Desktop/sales_messages.jsonl`, copied to `data/sales.jsonl` |
| Messages | 835 | 876 |
| Product category | finance, HR and ops tools | security and data tools |
| Weak/strong pairs | 22 | 25 (38 pair IDs in total) |

Both sets have the same schema and the same label mix: 51% strong, 29% average, 20–21% weak.

**Same method, isolated.** This folder uses unmodified copies of the set-1 scripts (`markers.py`, `make_pairs.py`, `score_A.py`, `score_B.py`). Two scripts are new here:
- `sample.py` draws the samples using the same rules and seeds as set 1.
- `compare_sets.py` produces the side-by-side comparison.

Nothing in `evals/sales/` was changed. For comparability, the rewriter read the ontology as it stood when set 1 was rewritten (checkpoint 1).

**Caveat (same as set 1):** the quality labels and buyer replies appear to have been generated together with the messages. The results below measure agreement with that labeler, not real buyer behavior.

## 1. Scripted markers (all messages): replicated

**When a message contains the marker, what share is labeled weak or strong:**

| Marker | Set 1 | Set 2 |
|---|---|---|
| Superlatives (share labeled weak) | 90% | 92% |
| Stock openers (share labeled weak) | 73% | 70% |
| Manufactured urgency (share labeled weak) | 73% | 89% |
| "Instead of" mechanism contrasts (share labeled strong) | 85% | 77% |
| Explicit opt-out (share labeled strong) | 87% | 70% |

**All clichés combined:**

| Measure | Set 1 | Set 2 |
|---|---|---|
| Precision (share of messages with any cliché that are weak) | 54% | 55% |
| Recall (share of weak messages that contain a cliché) | 56% | 52% |

**Did not replicate:**
- **Sentence-length spread (H10)** no longer separated weak from strong within pairs: 13 pairs vs 12 in set 2, against 20 vs 2 in set 1.
- **Weak messages are longer in set 2:** 98 words, against 78 in set 1. Strong messages were still the longer one in 21 of 25 pairs.

## 2. Content coding: replicated

Sample: all 25 weak/strong pairs plus 16 average messages, 66 in total. Two blind coders (Opus and Haiku) coded each message; they agreed at r ≥ 0.65 on 12 of 14 features.

**Reading the table:**
- **Separation** runs from 0.5 (no signal) to 1.0 (always separates strong from weak).
- Each cell gives Opus / Haiku.
- **Pairs** is the number of the 25 set-2 pairs where the strong message comes out ahead.

| Content feature | Set 1 separation | Set 2 separation | Set 2 pairs |
|---|---|---|---|
| Sentences about the buyer | 0.93 / 0.93 | 0.96 / 0.91 | 23 / 23 |
| Industry-specific pain | 0.91 / 0.98 | 0.90 / 0.94 | 20 / 22 |
| Smaller ask | 0.77 / 0.82 | 0.85 / 0.76 | 20 / 16 |
| Less pressure on the ask | 0.89 / 0.64 | 0.87 / 0.80 | 19 / 16 |
| Value offered before the ask | 0.84 / 0.84 | 0.80 / 0.78 | 15 / 14 |
| Mechanism explained | 0.84 / 0.86 | 0.72 / 0.74 | 11 / 13 |
| Fewer unsupported claims | 0.89 / 0.74 | 0.80 / 0.76 | 15 / 15 |
| Self-introduction first | no signal | no signal (0.52) | n/a |

The ask and pressure rows are shown so that higher means the strong message wins. In both sets, weak messages ask for more and push harder.

The H18–H21 content patterns and H06 hold on a second set of 876 different messages. The mechanism signal is weaker in set 2 but still clearly present.

## 3. Guarded rewrite: a different result from set 1

24 messages (12 weak, 12 average) were rewritten, and each pair was judged twice, once in each order.

**Quality grades** (0 = weak, 1 = average, 2 = strong; original → rewrite):

| Judge | Weak, set 1 | Weak, set 2 | Average, set 1 | Average, set 2 |
|---|---|---|---|---|
| Opus | 0.08 → 0.08 | **0.17 → 0.58** | 1.83 → 1.83 | 1.54 → 1.67 |
| Haiku | 0.67 → 0.62 | **0.62 → 0.96** | 1.62 → 1.67 | 1.25 → 1.46 |

**Preference that held in both orders** (rewrite / original / inconsistent):

| | Set 1 | Set 2 |
|---|---|---|
| Opus | 5 / 2 / 17 | 10 / 1 / 13 |
| Haiku | 3 / 4 / 17 | 9 / 4 / 11 |

On the 12 weak set-2 messages, the rewrite won in both orders 8 times with Opus and 7 times with Haiku.

**Why it differs.** Many weak set-2 messages are weak *because of* removable hype: "Great news!", "Byeee", "limited time", "Pretty cool, right?", exclamation stacks. Removing those lifts the grade. Set-1 weak messages were weak mostly in content (feature dumps, no buyer focus), which a rewrite cannot add.

**The cost:** part of that gain came from deleting claims and conditions, which is exactly what the guards forbid.

**Judgments rating the rewrite "same meaning":** 93 of 96 in set 1, against 85 of 96 in set 2 (Opus 42 of 48, Haiku 43 of 48). The remaining set-2 judgments rated it "partly".

**Changes flagged in both orders, by both judges:**
- **S10-0071: an offer condition was deleted.** "For a limited time" was removed, and the upgrade ask was softened.
- **S10-0013 and S10-0015: hype claims were removed.** Examples: "really exceptional deal", "amazing results", "super flexible". These are unsupported claims, but they are claims.
- **S10-0061, S10-0011 and S10-0041: "I'd love" became "I'd like".** Judges read this as a weaker ask. The guard says to keep ask strength, so the rewriter broke its own rule.
- **S09-0052 and S02-0077: indirect suggestions became direct questions or instructions.**
- **S06-0043, S06-0045 and S10-0023: closing invitations were dropped,** for example "let me know if you have questions".

## Takeaways

1. **The cliché markers and the content patterns are now replicated on two independent sets,** 1,711 messages in total. They are the most reliable parts of the ontology so far. This holds against these labelers, not against real buyers.
2. **H10 (sentence-length spread) did not replicate** as a quality signal on set 2. Consider downgrading it from `confirmed-AI-diff` for sales quality.
3. **A style rewrite can lift weak messages, but only when they are weak through hype,** and part of the lift comes from deleting claims. If deleting hype is wanted, it should be an explicit, flagged edit ("removed unsupported claim: …"), not something a meaning-preserving rewrite does silently.
4. **"I'd love" → "I'd like" is a recurring strength change.** It should be added to the deterministic drift check's word list.

## Files in this folder

| File | Contents |
|---|---|
| `compare.txt` | Scripted marker comparison |
| `B_results.txt` | Content-coding scores |
| `A_results.txt` | Rewrite and judge scores |
| `B_codings/`, `A_rewrites/`, `A_judgments/` | Raw outputs |
| `B_key.json`, `A_key.json`, `A_pair_key.json` | Sample keys |
