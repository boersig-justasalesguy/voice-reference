# Earnings-call speech: results (2026-11-19)

**Question:** how do B2B executives talk when they're unscripted, and how does that compare with (a) the same people reading prepared remarks, and (b) AI answering the same live questions?

## Data

**Transcripts:** 12 earnings calls from 11 B2B tech companies.

| Calls | Companies |
|---|---|
| Software | Cloudflare (2 calls), Q2, Atlassian, Tyler, N-able, Zendesk, AudioEye |
| Payments | Fiserv |
| Infrastructure | Digital Realty, Inphi, Cambium |

- **Dates:** 10 calls are from 2019–2021 and one is from 2023.
- **Sources:** company investor-relations sites or SEC filings. No paywalled aggregators were used.

**Rights note:** 10 of the transcripts were produced by FactSet or Refinitiv/Thomson Reuters and carry those vendors' copyright. They are used here only for local statistical analysis. The transcript text stays in the session's private scratch area and is not copied into this folder. Only scripts, statistics and AI outputs are stored here, and no quotation runs longer than 15 words.

**Transcript caveat:** vendor transcripts are lightly cleaned. Filler words ("um", "uh") are mostly removed, so real speech is *more* disfluent than measured here.

**Parsing:** the transcripts were split into speaker turns. Each turn was tagged by section (prepared remarks or Q&A) and by role (operator, executive, analyst).

- Q&A: 200 analyst-question → executive-answer exchanges.
- Prepared remarks: 2,000–4,000 words of executive speech per call. Zendesk and Atlassian have short prepared sections.

**AI baseline:** 24 exchanges (2 per call) were sampled. Claude Haiku, Sonnet and Opus each answered the same analyst question as the executive. They were given that call's prepared remarks as their only facts, so unlike earlier baselines, the AI was not working without information.

## 1. Same executives, prepared remarks vs live answers (12 calls)

All figures are per 1,000 words.

| Measure | Prepared | Live | Calls where live > prepared |
|---|---|---|---|
| Discourse openers ("So", "Look", "Yeah") | 2.2 | 27.0 | 12 of 12 |
| Stance markers ("I think", "you know", "kind of") | 1.4 | 16.1 | 12 of 12 |
| "I" | 4.4 | 15.5 | 12 of 12 |
| Sentences of 6 words or fewer | 5.5% | 18.5% | 12 of 12 |
| Contractions | 9.8 | 34.4 | 11 of 12 |
| "You" | 4.1 | 13.1 | 11 of 12 |
| First-person stance ("I think", "my view") | 0.3 | 6.6 | 11 of 12 |
| Self-repairs and restarts | 0.5 | 2.7 | 10 of 12 |
| Sentence-length spread (SD) | 10.3 | 13.4 | 10 of 12 |
| Hedges | 1.1 | 2.5 | 9 of 12 |
| Triplets ("X, Y and Z") | 5.1 | 2.1 | **0 of 12** |
| Numbers | 50.2 | 14.2 | **0 of 12** |
| Forward-looking stock phrases ("we expect", "going forward") | 4.6 | 1.9 | 2 of 12 |
| Nominalizations per 100 words | 4.5 | 3.1 | 2 of 12 |
| "We" | 51.8 | 53.9 | 7 of 12 (unchanged) |

**What this shows:**

- **The same person sounds like two different writers.** Prepared remarks have the institutional and AI fingerprint from earlier evals: triplets, figures and nominalizations. Live answers drop all of it.
- **"We" stays high in both.** Executives speak for the company even off-script. In an executive's voice, "we" is natural, so the M19 marker (institutional "we") shouldn't be applied there.

## 2. Human vs AI answers to the same analyst questions (24 exchanges, 72 AI answers)

**Scripted speech metrics.** Rates are per 1,000 words; the last row is the standard deviation of sentence length.

| Measure | Human live | AI (all) | Haiku | Sonnet | Opus | Same as prepared remarks |
|---|---|---|---|---|---|---|
| Discourse openers | 24.2 | 6.2 | 1.9 | 4.8 | 11.9 | 2.2 |
| Stance markers | 11.9 | 2.8 | 1.6 | 2.7 | 4.1 | 1.4 |
| First-person stance | 5.7 | 1.3 | 0.5 | 1.4 | 2.0 | 0.3 |
| Triplets | 1.4 | **5.7** | 6.1 | 6.5 | 4.6 | 5.1 |
| Numbers | 14.8 | **36.5** | 44.4 | 35.8 | 29.3 | 50.2 |
| Forward-looking stock phrases | 2.0 | **4.1** | 4.1 | 3.5 | 4.8 | 4.6 |
| Hedges | 1.4 | 0.3 | 0.0 | 0.4 | 0.5 | 1.1 |
| Repairs | 2.7 | 1.1 | 2.4 | 0.6 | 0.2 | 0.5 |
| Contractions | 28.6 | 34.8 | 33.0 | 38.8 | 32.7 | 9.8 |
| Sentence spread (SD) | 14.7 | **10.3** | 9.4 | 9.0 | 12.3 | 10.3 |

**Blind content coding of all 96 answers.** Human and AI answers were shuffled together and coded by Opus and Haiku separately; cells show Opus / Haiku. Agreement is the correlation between the two coders.

| What the answer does | Human | Haiku | Sonnet | Opus | Agreement (r) |
|---|---|---|---|---|---|
| Dumps 3+ figures nobody asked for | 0% / 8% | 71% / 71% | 75% / 67% | 71% / 67% | 0.77 |
| Sounds composed in real time (0–2) | 2.0 / 1.96 | 0.25 / 0.75 | 0.12 / 0.83 | 0.38 / 0.62 | 0.75 |
| Pivots to a talking point | 4% / 38% | 54% / 67% | 67% / 79% | 58% / 71% | 0.57 |
| States an owned view | 71% / 42% | 12% / 0% | 25% / 4% | 54% / 0% | 0.43 |
| Explains why or how | 88% / 88% | 46% / 62% | 67% / 79% | 75% / 88% | 0.76 |
| Uses a concrete example | 42% / 33% | 62% / 54% | 67% / 62% | 88% / 83% | 0.70 |
| Share of sub-questions answered | 0.73 / 0.73 | 0.65 / 0.69 | 0.73 / 0.71 | 0.89 / 0.81 | 0.81 |
| Declines or deflects | 12% / 25% | 62% / 67% | 96% / 92% | 46% / 46% | 0.90 |

**What this shows:**

- **Asked to speak live, the AI produces prepared remarks with contractions.** On the structural measures (triplets, number density, forward-looking phrasing, sentence rhythm), the AI answers sit with the scripted remarks, not the live speech. Contractions are the only spoken feature the AI adopts fully, so a contraction count is a poor test of "sounds spoken".
- **The AI is not worse at answering the question.** Opus covered more sub-questions than the humans did and gave more concrete examples. The difference is how it answers:
  - It recites figures (about 70% of AI answers, against 0–8% of human ones).
  - It pivots to talking points.
  - It reads as composed rather than thought aloud.
- **Humans reason aloud and own their views.**
  - They explain why or how in 88% of answers.
  - They state an owned view in 42–71% of answers, depending on the coder. The coders agree only weakly on this item, but both put humans clearly above the AI.
  - They hedge more and correct themselves mid-sentence.
- **The AI's higher deflection rate is partly an artifact of the setup.** The models were told to use only facts from the prepared remarks. Read the deflection row as an effect of the instruction, not of the models' style.

## 3. Proposed ontology changes (tagged; not merged)

Tags use the ontology's tag scheme (see "Tag scheme" before section 1). `ES` is the earnings-speech corpus.

### 3.1 New items

**M24. Scripted register in a live channel**
- **Category:** structural
- **Tags:** `src: ES AB` · `ev: meas code` · `ch: spoken call dm email` · `reg: all` · `status: confirmed-AI-diff`
- **What it looks like:** a reply or spoken answer that reads like prepared remarks:
  - figures recited without being asked for;
  - triplets;
  - stock forward-looking phrases ("we expect", "going forward");
  - an even sentence rhythm;
  - pivots to a talking point.
- **Evidence:** AI answers to live analyst questions put the prepared-remarks register on the page:

  | Measure | AI | Live humans | Prepared remarks |
  |---|---|---|---|
  | Triplets per 1,000 words | 5.7 | 1.4 | 5.1 |
  | Figures per 1,000 words | 36.5 | 14.8 | 50 |
  | Sentence-length spread | 10.3 | 14.7 | 10.3 |

  Coded blind, about 70% of AI answers recite figures nobody asked for, against 0–8% of human answers (two coders, r = 0.77). AI pivots to a talking point in 54–79% of answers, against 4–38% for humans.
- **When it matters:** fatal in any reply that is supposed to be live: a DM, a call answer, a follow-up email. Acceptable in a written report or prepared remarks.

**H22. Think-aloud answer**
- **Category:** structural
- **Tags:** `src: ES` · `ev: meas code` · `ch: spoken call dm email` · `reg: exec peer tech-buyer` · `status: confirmed-AI-diff`
- **Description:** the answer is built in this order:
  1. a discourse opener ("So…", "Look…");
  2. an owned view;
  3. a reason ("because…");
  4. at most one figure;
  5. a short landing.
- **Evidence:**
  - Within the same executives, every one of 12 calls has far more discourse openers when live (2.2 → 27 per 1,000 words), more stance markers (1.4 → 16.1) and more "I" (4.4 → 15.5). Figures and triplets never rise.
  - Coded blind, humans explain why or how in 88% of answers (AI: 46–88%) and state an owned view in 42–71% (AI: 0–54%).
- **Suits:** any reply that should sound like a person thinking, not a document.
- **Modern equivalent:** "So, honestly, I think the slowdown is mostly timing, because two big deals slipped into January. The pipeline itself looks fine."

### 3.2 Changes to existing items

| Item | Change | Tag change |
|---|---|---|
| M05 triplets | Add the ES evidence: prepared 5.1 vs live 2.1 per 1,000 words; triplets rose in 0 of 12 calls. | `src` + ES |
| M04 abstract verbs | Add the ES evidence: abstract verbs fall from 4.0 prepared to 2.2 live. | `src` + ES |
| M19 institutional "we" | Exempt the executive or company voice. Executives use "we" at about 52 per 1,000 words both scripted and live. Keep M19 for one-person-to-one-person requests. | `src` + ES; `status` → `confirmed-AI-diff; guarded; exec-voice-exempt` |
| H09 owned opinion | Add the ES evidence: "I"-stance rises from 0.3 prepared to 6.6 live, and in coding humans own a view more often than AI. The two coders agree only weakly on this item (r = 0.43). | `src` + ES; `ev` + meas code; `status` → `confirmed-AI-diff (weak coder agreement)` |
| H10 uneven rhythm | Add the ES evidence: spread is higher live than prepared in 10 of 12 calls; AI 10.3 vs human live 14.7. | `src` + ES |
| H15 uncertainty marker | Add the ES evidence: live hedges are 2.5 per 1,000 words vs 1.1 prepared; AI 0.3. | `src` + ES; `status` → `confirmed-AI-diff` |

### 3.3 Section 4 guards

| Guard | Tags |
|---|---|
| **Contractions are not evidence of conversational tone.** AI uses more contractions than live executives (34.8 vs 28.6 per 1,000 words). Weight discourse openers, owned stance and reasoning instead. | `src: ES AB` · `ev: meas` · `status: confirmed-AI-diff` |
| **Do not carry disfluencies into writing.** Discourse openers and owned stance transfer to a DM or reply; "um", restarts and repairs do not. | `src: ES` · `ev: inf` · `status: untested` (no written-outcome data) |

## Limitations

- **Small sample:** 12 calls, and 24 exchanges for the head-to-head comparison.
- **Unusual group:** executives are media-trained, and earnings calls are legally constrained (safe-harbor rules on forward-looking statements). This is how executives talk in public, not how they talk in a private sales conversation.
- **Cleaned transcripts:** vendor transcripts remove filler words, so disfluency is undercounted for the humans.
- **One model family:** the AI baseline is Claude only. The instruction to use only facts from the prepared remarks shapes both deflection and number use.
- **Automatic parsing:** speaker roles were inferred from transcript labels. Three speakers in two calls had roles marked unknown, and turns were rebuilt for the two scanned filings (Tyler and N-able).

## Files

Scripts and outputs here:
- `parse.py`, `speech.py`, `score.py`, `score_coding.py`
- `exchange_key.json`, `coding_key.json`
- `ai_prompts/`, `ai_answers/`, `codings/`
- `results.json`

The transcript text and pooled human answers are in the session's private scratch area and are not redistributed.
