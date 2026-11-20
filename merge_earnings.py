"""One-off merge of the approved earnings-call findings (evals/earnings/REPORT.md section 3) into human-voice-ontology.md.

Every anchor is asserted, so a mismatch aborts without writing. Tags are applied afterwards by tag_ontology.py.
"""
import sys

P = sys.argv[1]
s = open(P, encoding='utf8').read()

def ins_after(anchor, add):
    global s
    assert s.count(anchor) == 1, f'anchor not unique/missing: {anchor[:60]}'
    s = s.replace(anchor, anchor + add, 1)

def ins_before(anchor, add):
    global s
    assert s.count(anchor) == 1, f'anchor not unique/missing: {anchor[:60]}'
    s = s.replace(anchor, add + anchor, 1)

# --- new marker M24 (after M23) ---
ins_before('### M17. Status signaled by title, not by decision', """### M24. Scripted register in a live channel
- **Category:** structural
- **What it looks like:** a reply or spoken answer that reads like prepared remarks:
  - figures recited without being asked for;
  - triplets;
  - stock forward-looking phrases ("we expect", "going forward");
  - an even sentence rhythm;
  - a pivot to a talking point.
- **Observed (section 9):** AI answers to live analyst questions land in the prepared-remarks register, not the live register.

  | Per 1,000 words | AI answers | Live human answers | Prepared remarks |
  |---|---|---|---|
  | Triplets | 5.7 | 1.4 | 5.1 |
  | Figures | 36.5 | 14.8 | 50 |

  - Sentence-length spread (SD) matches the prepared remarks: 10.3 for both, against 14.7 for live answers.
  - In blind coding, about 70% of AI answers recite figures nobody asked for, against 0–8% of human answers (two coders, r = 0.77).
  - AI answers pivot to a talking point in 54–79% of cases, against 4–38% for human answers.
- **When it matters:** fatal in any reply that is supposed to be live: a DM, a call answer, a follow-up email. Acceptable in a written report or prepared remarks.

""")

# --- new human pattern H22 (after H21) ---
ins_after('- **Modern equivalent:** "I can send a one-page summary. No call needed."', """

### H22. Think-aloud answer
- **Category:** structural
- **Description:** the answer is built in this order:
  1. a discourse opener ("So…", "Look…");
  2. an owned view;
  3. a reason ("because…");
  4. at most one figure;
  5. a short landing.
- **Observed (section 9):**
  - The same executives sound different live than when reading prepared remarks. In 12 of 12 calls, live answers had more discourse openers (2.2 → 27 per 1,000 words), more stance markers (1.4 → 16.1) and more "I" (4.4 → 15.5). Figures and triplets did not rise in any call.
  - Coded blind, human answers explain why or how in 88% of cases (AI: 46–88%) and state an owned view in 42–71% (AI: 0–54%).
- **Suits:** any reply that should sound like a person thinking, not a document.
- **Modern equivalent:** "So, honestly, I think the slowdown is mostly timing, because two big deals slipped into January. The pipeline itself looks fine.\"""")

# --- evidence added to existing items ---
ins_after("  - So weight the abstract verbs low as AI evidence, and keep nominalization density as a register signal.", """
- **Earnings check (section 9):** the same executives use 4.0 abstract verbs per 1,000 words in prepared remarks and 2.2 when answering live. Spoken versus scripted is a second axis, alongside institutional versus personal.""")
ins_after("  - AI practitioner texts: 10.1, against 3.3 for early Latio.", """
- **Earnings check (section 9):** triplets run at 5.1 per 1,000 words in prepared remarks and 2.1 live, and rose in 0 of 12 calls. AI answering live used 5.7.""")
ins_after("- **When it matters:** fatal in a cold request or an intro, where the reader is deciding about a person. Acceptable in procurement, where the company is the party.", """
- **Exemption (section 9): the executive or company voice.** Executives speaking for their company use "we" at about 52 per 1,000 words, both scripted and live. Do not flag "we" when the writer is speaking as the company. Keep M19 for one-person-to-one-person requests.""")
ins_after('- **Modern equivalent:** "My take: build it in-house." Not: "Many experts suggest considering…"', """
- **Earnings check (section 9):** "I"-stance phrases ("I think", "my view") rise from 0.3 per 1,000 words in prepared remarks to 6.6 live. In blind coding, human answers own a view more often than AI answers. The two coders agree only weakly on this item (r = 0.43).""")
ins_after('- **Modern equivalent:** two medium sentences, then "Worth a look?" or "That\'s the whole ask."', """
- **Earnings check (section 9):** sentence-length spread is higher live than in prepared remarks in 10 of 12 calls. Live human answers measure 14.7, AI answers 10.3.""")
ins_after('- **Modern equivalent:** "Pure guess, but I think they get acquired." Every other claim stays unhedged.', """
- **Earnings check (section 9):** hedges run at 1.1 per 1,000 words in prepared remarks and 2.5 in live answers. AI answering live used 0.3.""")

# --- section 4 guards + transformation 24 ---
ins_after("If H18–H21 are missing, the fix is to redraft, not to rewrite.", """
- **Contractions alone are not evidence of conversational text.** AI answering live used more contractions than executives did (34.8 vs 28.6 per 1,000 words). Weight discourse openers, owned stance (H09) and reasoning (H22) instead (section 9).
- **Do not carry spoken disfluencies into writing.** Discourse openers and owned stance transfer to a DM or a reply; "um", restarts and repairs do not. This is untested against written outcomes.""")
ins_after("Flag it as a redraft suggestion instead.", """
24. **M24 scripted register in a live channel → H22 think-aloud answer**
    - **How:**
      - Lead with the direct answer or view, then give the reason.
      - Keep the one figure the question asked for, and cut the rest. This is allowed only when the figures were not requested. Never cut a figure the asker wanted.
      - Remove stock forward-looking phrases. Keep any real guidance word for word.
    - **Applies:** DM, call, follow-up email, any live reply.
    - **Do not apply:** to written reports or prepared remarks.""")

# --- open question + section 9 ---
ins_after("Validating them needs real sends with real reply and meeting data.", """
9. **Spoken evidence is from public, media-trained speech.** Earnings calls are legally constrained (safe-harbor rules), and vendor transcripts remove filler words. Private sales conversations may differ. M24 and H22 still need validating on real call recordings.""")
s = s.rstrip('\n') + """

---

## 9. Earnings-call speech (added 2026-11-19)

The full report is in [evals/earnings/REPORT.md](evals/earnings/REPORT.md). Scripts are in [evals/earnings/](evals/earnings/).

**Data:** 12 earnings calls from 11 B2B technology companies: 10 calls from 2019–2021 and 1 from 2023, taken from company IR sites and SEC filings.
- 10 of the transcripts were produced by FactSet or Refinitiv. Their text is used only for local statistics and is not redistributed.
- The source code for this corpus is `ES`.

**Two comparisons:**
1. The same executives' prepared remarks against their live answers.
2. Claude Haiku, Sonnet and Opus answering 24 of the same analyst questions, given that call's prepared remarks as facts. That makes 72 AI answers.

All 96 answers (24 human, 72 AI) were coded blind by two coders.

**What changed in this ontology:**
- **Added:** M24 (scripted register in a live channel) and H22 (think-aloud answer).
- **ES evidence added to existing items:** M04, M05, H09, H10 and H15.
- **M19:** now exempts the executive or company voice.
- **Section 4:** two guards (contractions; disfluencies) and transformation 24.
- **Open questions:** 6.3 item 9 added.
"""
s = s.replace(
    "with an AI baseline (section 7) and sales-message validation (section 8). Compiled 2026-11-19; sales findings merged 2026-11-19.",
    "with an AI baseline (section 7), sales-message validation (section 8) and earnings-call speech (section 9). Compiled 2026-11-19; sales and earnings findings merged 2026-11-19.")
open(P, 'w', encoding='utf8').write(s)
print('merged')
