"""One-off merge of the post-checkpoint-4 findings into human-voice-ontology.md (approved by the user 2026-11-19):
set-2 replication (evals/set2/REPORT.md), the tone-position reframe (tone/README.md), and the spoken-script findings.

Every anchor is asserted, so a mismatch aborts without writing. Tags are applied afterwards by tag_ontology.py.
"""
import sys

P = sys.argv[1]
s = open(P, encoding='utf8').read()

def ins_after(anchor, add):
    global s
    assert s.count(anchor) == 1, f'anchor not unique/missing: {anchor[:70]}'
    s = s.replace(anchor, anchor + add, 1)

def ins_before(anchor, add):
    global s
    assert s.count(anchor) == 1, f'anchor not unique/missing: {anchor[:70]}'
    s = s.replace(anchor, add + anchor, 1)

# --- new marker M25 (after M24) ---
ins_before('### M17. Status signaled by title, not by decision', """### M25. Written register in a spoken channel
- **Category:** structural
- **What it looks like:** a call script, voicemail or video script that reads like an email:
  - almost no discourse openers ("So…", "Look…", "Yeah…");
  - no first-person stance ("I think");
  - few stance markers ("I mean", "kind of");
  - sentence lengths more uniform than people actually speak.
- **Observed (section 10):** 362 AI-written call, voicemail and video scripts from both sales sets, scored against live executive speech. They sit at 0.32 on the AI → human scale.

  | Measure | Scripts | Live speech | AI default |
  |---|---|---|---|
  | Discourse openers per 1,000 words | 3.5 | 26.6 | 6.2 |
  | First-person stance per 1,000 words | 0.9 | 7.2 | 1.3 |
  | Sentence-length spread (SD) | 8.6 | 13.1 | 10.3 |

  On all three measures the scripts fall short of even the AI default. They do avoid other AI tells: figures (14.8 per 1,000 words, against 11.9 human) and stock forward-looking phrases (none).
- **When it matters:** any text meant to be spoken (call openers, voicemails, video scripts). It does not apply to email.
- **Caveat:** the human target is executives answering analysts, which is only a partial stand-in for sales reps. "You" was excluded as a register mismatch: reps use it at 44 per 1,000 words, executives at 12. Real sales-call recordings would be the proper target.

""")

# --- replication notes on existing items ---
ins_after("  Together they catch 56% of weak messages.", """

  **Replicated on a second, independent set** (876 messages, different products; `evals/set2/`):

  | Marker | Precision, set 1 | Precision, set 2 |
  |---|---|---|
  | Superlatives (share labeled weak) | 90% | 92% |
  | Stock preamble (share labeled weak) | 73% | 70% |
  | Manufactured urgency (share labeled weak) | 73% | 89% |
  | Mechanism contrasts (share labeled strong) | 85% | 77% |
  | Opt-out (share labeled strong) | 87% | 70% |
  | Any cliché: precision / recall | 54% / 56% | 55% / 52% |

  The content patterns also replicated (two coders, matched pairs):
  - buyer-centric sentences: separation 0.91–0.96, strong message ahead in 23 of 25 pairs;
  - industry pain: 0.90–0.94;
  - smaller ask and less pressure: about 0.8;
  - value before the ask: about 0.8;
  - mechanism: 0.72–0.74, weaker than in set 1.

  These findings now rest on 1,711 messages, still against dataset labels only.""")
ins_after("- **Earnings check (section 9):** sentence-length spread is higher live than in prepared remarks in 10 of 12 calls. Live human answers measure 14.7, AI answers 10.3.", """
- **Sales check (sections 8 and 10):** **not a sales-quality signal.** Sentence-length spread separated weak from strong pairs in set 1 (20 vs 2) but not in set 2 (13 vs 12). It remains an AI-vs-human tone feature: in held-out tone scoring it is discriminative in the live-speech and practitioner situations.""")

# --- section 4 guards ---
ins_after("- **Do not carry spoken disfluencies into writing.** Discourse openers and owned stance transfer to a DM or a reply; \"um\", restarts and repairs do not. This is untested against written outcomes.", """
- **Add "I'd love" → "I'd like" to the drift check's word list.** The set-2 rewriter made this change in three messages despite the guard, and both judges read it as a weaker ask.
- **Deleting hype is an edit, not a rewrite.** In set 2, rewriting lifted weak messages' grades (Opus 0.17 → 0.58), but part of the lift came from deleting claims and conditions ("limited time", "amazing results"). A meaning-preserving rewrite must not do this silently. Surface it as a flagged edit, e.g. "removed unsupported claim: …".
- **Sounding human and being a good pitch are separate axes.** Score them separately:
  - tone position (section 10);
  - content checks (H18–H21).

  Weak spoken scripts scored *more* human (0.43) than strong ones (0.28) because they are chattier ("honestly", "you know", more hedges).""")
ins_after("    - **Do not apply:** to written reports or prepared remarks.", """
25. **M25 written register in a spoken channel → H22 think-aloud answer**
    - **How:**
      - Open some sentences with a discourse marker ("So…", "Look…").
      - Add at most one owned view ("I think…") where the original states a position.
      - Vary sentence length.

      Keep every fact, figure and ask.
    - **Applies:** call scripts, voicemails, video scripts.
    - **Do not apply:** to email. Never add "um", restarts or filler (see the guard above).""")

# --- open questions ---
ins_after("9. **Spoken evidence is from public, media-trained speech.**", "")
anchor9 = s[s.index("9. **Spoken evidence is from public, media-trained speech.**"):]
end9 = anchor9.index("\n") + s.index("9. **Spoken evidence is from public, media-trained speech.**")
s = s[:end9] + """
10. **No real human target for sales writing.** Both sales sets are AI-generated, including the "strong" messages. The tone scorer's `sales_outreach` situation can measure deviation from the AI default, but not position toward a human target. Real sent emails and DMs, and real sales-call recordings, would supply it.
11. **A 19th-century proxy target reverses some directions.** Scored against classic letters, more lists of three and more contrast frames count as "human", the opposite of every modern comparison. Proxy targets from another era should not be used to direct rewrites.""" + s[end9:]

# --- section 10 ---
s = s.rstrip('\n') + """

---

## 10. Tone position: AI default → human target (added 2026-11-19)

**Reframe (user, 2026-11-19).** Judge a message not as good or bad, but by how far it has moved from the AI default toward how a human sounds **in that situation**. Each marker and pattern in this ontology is read as a feature with a direction (AI side vs human side) for a given situation. Overshooting past the human target is also a fault: it sounds forced.

**Tool:** [tone/](tone/README.md). It is isolated from the rest of the code and reuses the existing measurement code read-only.

**How a message is scored, per feature:**

| Output | Meaning |
|---|---|
| `z_ai` | Standard deviations from the AI default mean |
| `position` | (value − AI mean) / (human mean − AI mean). 0 = AI default, 1 = human target |
| Overshoot | Past the human target by more than 2 human standard deviations |

The overall position is the effect-size-weighted mean of the per-feature positions. Only features where AI and human clearly differ (|d| ≥ 0.5) count toward it.

**Situations.** The held-out AUC comes from document-level 70/30 splits, repeated 20 times:

| Situation | AI reference | Human target | Held-out AUC |
|---|---|---|---|
| `live_exec_answer` | 72 AI answers | 207 live executive answers (ES) | 0.98 |
| `practitioner_post` | 9 AI texts | early Latio (PW) | 0.94 |
| `analyst_report` | 9 AI texts | Gartner/IDC (IN) | 0.89 |
| `one_to_one_message` | 15 AI messages | classic letters (CL), **proxy** | 1.00 |
| `sales_outreach` | 1,711 AI sales messages | none yet | n/a |

**Results on the sales sets:**
- **Against the AI sales reference:** 83–85% of features fall in the typical AI range. Strong messages are *more* AI-typical than weak ones, because weak ones deviate through hype. Deviation alone is not humanness; the direction has to come from a human target.
- **Spoken scripts against live speech:** they sit at 0.32. This is the basis for M25.
- **Against the letters proxy:** about 0.4, but unreliable (see 6.3, item 11).

**What this changes:** markers and patterns should eventually carry per-situation directions and reference values, not just a status. `tone/references/*.json` holds these for the five situations above. New human corpora each add a situation: real sent sales emails and DMs, sales-call recordings, and books by genre (BK).
"""
s = s.replace(
    "earnings-call speech (section 9). Compiled 2026-11-19; sales and earnings findings merged 2026-11-19.",
    "earnings-call speech (section 9) and tone-position scoring (section 10). Compiled 2026-11-19; sales, earnings, set-2 and tone findings merged 2026-11-19.")
open(P, 'w', encoding='utf8').write(s)
print('merged')
