# Human Voice Ontology for B2B Communication

Comparative style analysis of three sources: classic correspondence, institutional analysts, and Latio, with an AI baseline (section 7), sales-message validation (section 8) and earnings-call speech (section 9). Compiled 2026-11-19; sales and earnings findings merged 2026-11-19.

---

## 0. Corpus and reference keys

Every pattern below cites one or more of these keys.

### Classic (public domain)

| Key | Document | Access |
|---|---|---|
| C-FR1 | Franklin, "Model of a Letter of Recommendation of a Person You Are Unacquainted With," Paris, 2 Apr 1777 (Founders Online Franklin/01-23-02-0365) | Read via the Penn transcription (web.sas.upenn.edu/bfranklin/?p=62). Founders Online blocked fetches. |
| C-LH | Lincoln to Gen. Joseph Hooker, 26 Jan 1863 | Full text, abrahamlincolnonline.org (Basler) |
| C-LG | Lincoln to Horace Greeley, 22 Aug 1862 | Full text, same source |
| C-LB | Lincoln to Mrs. Bixby, 21 Nov 1864 | Full text, same source |
| C-DG | Darwin to Asa Gray, 25 Apr [1855], DCP-LETT-1674 | Full text, Darwin Correspondence Project |
| C-PP13 | Austen, *Pride and Prejudice* ch. 13 (Mr. Collins's letter) | Gutenberg #1342 |
| C-PP19 | *P&P* ch. 19 (Collins's proposal) | Gutenberg #1342 |
| C-PP56 | *P&P* ch. 56 (Elizabeth and Lady Catherine) | Gutenberg #1342 |
| C-CN | Chekhov to his brother Nikolay, 1886 | Gutenberg #6408 |
| C-CS | Chekhov to Suvorin, 30 May 1888 | Gutenberg #6408 |
| C-AR | Aristotle, *Rhetoric* I.2, II.1, II.12–17, III.2–3, III.7 | Summarized from standard translations, not fetched this session |
| C-CI | Cicero, *Orator* §§70–90; *De Oratore* III.210–212 | Same: summarized, not fetched |

### Institutional (all public and published before late 2022, read via Wayback)

| Key | Document | Date |
|---|---|---|
| G-P1 | Gartner press release, "70% of Organizations Will Shift Their Focus From Big to Small and Wide Data By 2025" | 19 May 2021 |
| G-P2 | Gartner press release, "40% of Boards Will Have a Dedicated Cybersecurity Committee by 2025" | 28 Jan 2021 |
| G-P4 | Gartner press release, "Top Predictions for IT Organizations and Users in 2022 and Beyond" | 19 Oct 2021 |
| G-S1 | Smarter With Gartner, "5 Trends Drive the Gartner Hype Cycle for Emerging Technologies, 2020" | Aug 2020 content |
| G-S2 | Smarter With Gartner, "Gartner Top Strategic Technology Trends for 2021" | 19 Oct 2020 |
| G-H1 | Gartner Hype Cycle methodology page | Captured Jan 2020 |
| G-M1 | Gartner Magic Quadrant methodology page | Captured Jan 2021 |
| I-1 | IDC FutureScape press release, "Digital Supremacy" | 29 Oct 2019 |

### Latio (public posts on pulse.latio.tech and latio.com)

| Key | Document | Date |
|---|---|---|
| L-P1 | "What do I think about Wiz Code?" | Oct 2024 |
| L-P2 | "WTF is Cloud Detection and Response (CDR)?" | Jun 2024 |
| L-P3 | "The Great CNAPP Re-bundle" | Mar 2025 |
| L-P4 | "Emerging Categories: The Evolution of AI SOC" | Dec 2025 |
| L-P5 | "The 5 Security Features that will lead in 2026, and 3 that should" | Dec 2025 |
| L-P6 | "The Complete Guide to Preventing Open Source Malware" | Mar 2026 |
| L-P7 | "The Privatization of Vulnerability Management" | Jul 2026 |
| L-P8 | "The 2026 Latio AI Security Market Report is Live!" | Sep 2026 |
| L-P9 | "The New Normal: What the Recent Incidents Mean…" | Oct 2026 |
| L-P10 | Latio vendor listing: Wiz (latio.com/vendor/wiz) | Aug 2026 |

### Gaps in the corpus

- **Not covered:** Forrester (fetch failed), Trollope, Twain, a Franklin business letter or request to a superior, and Latio's PDF market reports.
- **Different reading method:** the Latio counts come from page summaries, so treat them as accurate to about ±20%. The Gartner counts come from a regex script run over the body text with boilerplate removed.
- **Sample size:** 8 institutional pieces, 10 Latio pieces, and about 10 classic documents. That is enough to describe each source's register. It is not enough for statistical claims.

---

### Tag scheme

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

## 1. Source profiles

### 1a. Classic correspondence and status dialogue

- **A. Lexical**
  - Effective letters use plain, concrete verbs. Hooker is built on short concrete verbs of placing, asking, risking and warning (C-LH); Greeley repeats one verb throughout (C-LG).
  - Hedges narrow the claim (partial dissatisfaction; ambition within limits) rather than soften the writer's stance (C-LH).
  - Courtesy formulas sit on top of dense content. Darwin layers repeated apologies for presumption over exact labels and a species count (C-DG).
  - The failed exemplar, Collins, is mostly formula, built on ceremonial abstract verbs of promoting, establishing and reconciling (C-PP13).
- **B. Structural**
  - Effective letters are 140–520 words (C-FR1 ≈140, C-LB ≈140, C-LH ≈370, C-DG ≈520).
  - Sentence length varies widely, and letters often end on a short command (C-LH).
  - The first sentence states the decision or the situation (C-LH, C-LG, C-LB, C-FR1). Darwin spends one sentence reconnecting, then asks in the second (C-DG).
  - Collins writes about 330 words in about 5 sentences, one of them about 150 words. His actual purpose comes near the end (C-PP13).
- **C. Rhetorical**
  - **Credibility** comes from how the writer knows something: an official record (C-LB), a stated hearsay basis (C-LH), a disclosed method plus an admitted lack of expertise (C-DG). Collins borrows credibility from his patron instead (C-PP13, C-PP19).
  - **Criticism** follows a fixed order: decision, specific qualified praise, specific charge, expectation, bounded support, consequence, directive (C-LH). Chekhov uses the same order, with an explicit candor marker before the hard part (C-CN).
  - **Pronouns:** "I" and "you" alternate clause by clause (C-LH). The first person owns the position (C-LG).
- **D. Calibration**
  - The endorsement is limited to what the writer actually knows (C-FR1).
  - Writers commit to revising when shown to be wrong (C-LG) and admit their own lack of expertise (C-DG).
  - Admitting "I don't understand" is treated as a strength (C-CS).
  - Collins certifies his own virtue, with no calibration at all (C-PP13).
- **E. Speech acts**
  - **Request to a senior stranger:** reconnect, name the favor, lower its cost, give exact instructions, flag any extra ask (C-DG).
  - **Superior to subordinate:** status is signaled through decisions, not titles; the salutation is a bare rank (C-LH)
  - **Refusing a superior:** short flat declaratives answer stacked rhetorical questions, and logic undercuts appeals to rank (C-PP56).
- **Classical theory** (summarized from standard translations, not fetched)
  - Clarity is the chief virtue of style, and art should be concealed (C-AR III.2).
  - "Frigidity" comes from excess epithets, strange compounds and inappropriate metaphor (C-AR III.3).
  - Style must fit the subject, the speaker and the audience (C-AR III.7; C-CI *Orator* §§70–74).
  - The plain style uses "careful negligence" (C-CI *Orator* §§76–90).

### 1b. Institutional analyst (Gartner, IDC)

- **A. Lexical**
  - Abstract enabling verbs are frequent: "enable" ×24 across the corpus, with 14 in G-S2; "drive" ×15.
  - Nominalization density runs 4.0–9.6 suffix-nouns per 100 words, highest in G-S2 and G-P2.
  - Buzz nouns: resilience, composable, agility, ecosystem.
  - Coined proprietary terms: Internet of Behavior, cybersecurity mesh (G-S2); "digital supremacy" (I-1).
  - Precise technique names also appear: few-shot learning, synthetic data (G-P1); EEG (G-S1).
  - Forecasts carry almost no hedges: "will" ×24 and "may" ×0 in G-P4. The hedges that do appear are mostly inside quotes (G-P2).
  - **Zero** instances of delve, landscape, navigate, journey, unlock, moreover, furthermore, or "in conclusion" anywhere in the corpus.
- **B. Structural**
  - Press releases have long, uniform sentences: means of 22–27 words, standard deviation about 7 (G-P1, G-P2, G-P4).
  - Paragraphs run 1.4–1.9 sentences in press releases.
  - Triplets are heavy: up to 16 per piece (G-S2).
  - List items follow a fixed template: label, colon, definition (G-S2), or definition, then an example signpost, then a list of related technologies (G-S1).
  - "Not X but Y" constructions are rare, about 3 in the corpus.
  - **Openings:** a statistic plus attribution in press releases (G-P1, G-P2, I-1); a concrete anecdote in explainers (G-S1, G-S2).
  - **Closings:** no summary. Pieces stop, then run into an upsell and boilerplate (G-P1, G-P2, G-P4).
- **C. Rhetorical**
  - Credibility comes from the institution plus a titled analyst, quoted 1–7 times per piece (G-P4 ×7).
  - Survey method is shown only once (n=265, G-P2).
  - Opinion and metaphor are delegated to quotes. The narration attributes beliefs, recommendations and expectations to the firm in the third person (G-S1, G-P2).
  - Criticism targets categories, never named vendors (G-S2, G-S1, G-M1).
  - No authorial "I" anywhere. Methodology pages are written in the second person, with "you" ×18 in G-M1.
- **D. Calibration**
  - Certainty is precise and dated: "By 2025, N%…" appears 10× in G-P4 and 16× in I-1. Forecasts sometimes give a baseline (G-P2, I-1).
  - Forecasts are often deliberately provocative and falsifiable (G-P4).
  - Supporting evidence is withheld behind the paywall (G-P4).
  - No commercial vendors are named in any press release or methodology page.
- **E. Speech acts**
  - Readers are addressed by role in the third person (security leaders, CIOs) (G-P2, G-P4).
  - Advice uses obligation verbs (must, need to, should) or an indirect subjunctive (the firm recommends that leaders consider…) (G-P2).
  - Status is signaled through full analyst titles and boilerplate superlatives (G-P1, G-P4, I-1).
- **Illustrative excerpt:** "By 2025, 40% of boards of directors will have a dedicated cybersecurity committee" (G-P2).

### 1c. Latio: two registers

The Latio writing moves through three stages, so they are profiled separately. The boundaries come from first-person rate measured in the raw text ("I/me/my" per 1,000 words):

| Stage | Posts | First-person rate |
|---|---|---|
| Early | L-P1–P3 | 17–25 |
| Transitional | L-P4–P5 | 12.5 and 6.8 |
| Late | L-P6–P9 | 0–2 |

**Register L-early (2024–early 2025; L-P1, L-P2, L-P3)**

- **A. Lexical**
  - Plain, physical verbs: bolted on, pour into, popped (L-P2, L-P3).
  - Dense, precise acronyms: CNAPP, ASPM, eBPF, DSPM (L-P1, L-P2).
  - Named vendors: about 26 in L-P1 and about 21 in L-P3.
  - Slang, pop-culture references and jokes, several per early piece (L-P1, L-P2, L-P3).
  - Mocks new category acronyms instead of adopting them (L-P3).
  - Few hedges, 0–4 per piece. Softening comes through first-person ownership phrases instead (L-P3).
- **B. Structural**
  - Sentences range from 3-word fragments to about 300 characters (L-P2).
  - Headers are often plain questions about audience and definition (L-P1).
  - Openings are personal anecdotes (L-P1, L-P2).
  - L-P1 closes with a TL;DR verdict and an emoji scorecard.
- **C. Rhetorical**
  - **Credibility:**
    - Years of hands-on practice (L-P2).
    - Money disclosed (L-P1).
    - Testing limits stated: says demos were brief (L-P1); has not tested every tool (L-P2).
    - Speculation flagged as a guess (L-P1).
  - **Opinions** are stated flatly and as the writer's own, including declaring a market winner by name (L-P3).
  - **Criticism** names the vendor and is balanced with praise in the same piece (L-P1, L-P3).
  - **Pronouns:** 42 uses of "I" in L-P1 and 34 in L-P2, counted in the raw text. That is 19.6 and 25.3 first-person words per 1,000.
- **D. Calibration**
  - Numbers are specific: acquisition dates, survey percentages (L-P1, L-P2).
  - Uncertainty is marked explicitly where it exists, with one or two plain markers per piece (L-P2, L-P3).
- **E. Speech acts**
  - Recommendations are segmented by the reader's situation, e.g. one tool for existing platform customers, others for developer-led teams (L-P1).
  - Anticipates vendor backlash openly (L-P2).
- **Illustrative excerpt:** "I have taken $0 from any CNAPP provider ever." (L-P1)

**Register L-transition (Dec 2025; L-P4, L-P5)**

- First person falls to 11 "I" in L-P4 and 6 in L-P5.
- Ownership markers remain: a first-person prediction (L-P5) and a vendor-access disclosure (L-P4).
- "It's clear that…" and "On the one hand…" scaffolding appears (L-P4).
- Contrast frames peak here: 4.4 per 1,000 words (section 7).

**Register L-late (2026; L-P6, L-P7, L-P8, L-P9, L-P10)**

- First person nearly disappears: "I" ×0 in L-P6 and L-P8, ×1 in L-P7 and ×2 in L-P9 (raw-text counts). An institutional "we" replaces it (L-P8, L-P9).
- Pieces become checklists: bold-label lists, then sections split into immediate actions and larger initiatives (L-P6).
- "It's clear that…" openers (L-P6, L-P9).
- Closers are moral aphorisms (L-P7, L-P9).
- Specificity is still high: 877,000 packages, version pins, CVE IDs (L-P6, L-P9).
- L-P8 is an exception: hype adjectives and no specifics.
- L-P10 is a bland third-person vendor profile.

**Implication:** L-early is the clearer reference register for "human practitioner" voice. L-transition and L-late show that a genuinely human-authored source can move toward institutional and AI-like structure. The cause is unknown (see 6.3, question 4). What can be observed is that the drift shows up together with templated formats such as checklists and announcements.

---

## 2. ai_markers

Each marker lists its category, what it looks like, where it was observed, and when it matters. The "observed" field cites the closest human-authored analogue in this corpus. No LLM text was sampled (see section 6).

### M01. Ceremonial preamble
- **Category:** structural
- **Tags:** `src: CF CL SL` · `ev: obs lab` · `ch: email dm voicemail` · `reg: stranger exec` · `status: confirmed-quality`
- **What it looks like:** one or more sentences of context, goodwill or self-positioning before the purpose of the message.
- **Observed:** Collins delays his purpose until near the end (C-PP13). Contrast the first-sentence decision in C-LH and C-LG.
- **When it matters:** fatal in a cold outreach first line and in executive messages. It is acceptable in condolence notes and in a single reconnecting clause (C-DG).
- **Sales check (section 8):** stock openers such as "hope this finds you well", "my name is" and "I wanted to reach out" appeared in 49 of 835 labelled sales messages. 73% of those were labelled weak, against a 20% base rate.
  - It works as a high-precision detector.
  - A self-introduction as such did not separate strong from weak in the content coding (0.52–0.55). The marker is the stock phrasing, not introducing yourself.

### M02. Self-certified virtue or sincerity
- **Category:** rhetorical
- **Tags:** `src: CF` · `ev: obs` · `ch: all` · `reg: all` · `status: corpus-only`
- **What it looks like:** the writer labels their own intent as good, helpful, excited or genuine.
- **Observed:** C-PP13 (the letter praises its own overtures).
- **When it matters:** fatal everywhere. It is the strongest insincerity signal in the classic set.

### M03. Formula-to-substance ratio inverted
- **Category:** framing
- **Tags:** `src: CF CL` · `ev: obs` · `ch: all` · `reg: all` · `status: corpus-only`
- **What it looks like:** courtesy formulas outnumber the concrete facts or instructions.
- **Observed:** C-PP13 (one concrete item: the date and time). Contrast C-DG, where heavy formula is acceptable because the substance is dense.
- **When it matters:** formula itself is not the problem. The ratio is.

### M04. Abstract enabling verbs and nominalization
- **Category:** lexical
- **Tags:** `src: IN CF AB ES` · `ev: obs meas` · `ch: email dm` · `reg: peer IC tech-buyer` · `status: revised: institutional-not-AI`
- **What it looks like:** enable, drive, facilitate, transform, plus -tion/-ity nouns as subjects. Density above about 7 per 100 words.
- **Observed:** G-S2 (9.6 per 100 words; "enable" ×14); G-P2 (8.5); C-PP13 (ceremonial abstract verbs).
- **When it matters:** acceptable in category definitions. Fatal in a peer or IC message, where the reader expects an actor and an action.
- **Baseline check (section 7):** **institutional marker, not an AI marker.**
  - The AI analyst texts used these verbs at 1.4 per 1,000 words, against 8.2 for Gartner.
  - Nominalization was about the same: 7.9 vs 6.8 per 100 words.
  - So weight the abstract verbs low as AI evidence, and keep nominalization density as a register signal.
- **Earnings check (section 9):** the same executives use 4.0 abstract verbs per 1,000 words in prepared remarks and 2.2 when answering live. Spoken versus scripted is a second axis, alongside institutional versus personal.

### M05. Reflexive triplets
- **Category:** structural
- **Tags:** `src: IN AB ES` · `ev: obs meas` · `ch: all` · `reg: all` · `status: confirmed-AI-diff`
- **What it looks like:** "X, Y, and Z" lists used for rhythm rather than because there are exactly three items.
- **Observed:** G-S2 (16 in one piece); G-P4 (9); G-H1 and G-M1 (3-bullet "help you" lists).
- **When it matters:** tolerable once per message. A repeated triplet cadence is a strong machine and institutional signal.
- **Baseline check (section 7):** **confirmed as one of the strongest AI markers.**
  - AI analyst texts: 16.7 triplets per 1,000 words, against 8.8 for Gartner.
  - AI practitioner texts: 10.1, against 3.3 for early Latio.
- **Earnings check (section 9):** triplets run at 5.1 per 1,000 words in prepared remarks and 2.1 live, and rose in 0 of 12 calls. AI answering live used 5.7.

### M06. Templated list items
- **Category:** formatting
- **Tags:** `src: IN PW` · `ev: obs` · `ch: email dm` · `reg: all` · `status: corpus-only`
- **What it looks like:** every item has the same shape: bold label, colon, definition, "For example…".
- **Observed:** G-S1, G-S2, L-P6, L-P7.
- **When it matters:** acceptable in reference docs and checklists. Fatal in email or LinkedIn DMs, where nobody formats like this.

### M07. Impersonal role address
- **Category:** framing
- **Tags:** `src: IN` · `ev: obs` · `ch: email dm` · `reg: stranger peer exec` · `status: corpus-only`
- **What it looks like:** "organizations," "leaders," "security teams" instead of "you" or a named person.
- **Observed:** G-S2 ("organizations" ×17); G-P2; G-P4.
- **When it matters:** fatal in one-to-one messages. Acceptable in public posts aimed at a segment.

### M08. Opinion laundered through attribution
- **Category:** rhetorical
- **Tags:** `src: IN` · `ev: obs` · `ch: all` · `reg: peer tech-buyer` · `status: corpus-only`
- **What it looks like:** the evaluative claim is put in someone else's mouth ("experts say," "Gartner believes," a quoted VP) rather than owned.
- **Observed:** G-P4 (metaphor appears only inside quotes); G-S1 and G-P2 ("Gartner recommends").
- **When it matters:** fatal when the sender is supposed to have a view, as in peer advice or a recommendation.

### M09. Unevidenced benefit claim
- **Category:** sales_cliche
- **Tags:** `src: IN PW SL` · `ev: obs code` · `ch: all` · `reg: tech-buyer procurement` · `status: confirmed-quality`
- **What it looks like:** a stack of outcomes (more innovation, lower cost, better partnerships) with no mechanism, number or example.
- **Observed:** G-S1; L-P8 ("hottest market," no specifics).
- **When it matters:** fatal for technical buyers and procurement.

### M10. Category-level criticism only
- **Category:** calibration
- **Tags:** `src: IN PW` · `ev: obs` · `ch: long-form dm` · `reg: peer tech-buyer` · `status: corpus-only`
- **What it looks like:** criticism aimed at "many tools" or "organizations that don't…" and never at a named product or practice.
- **Observed:** G-S2, G-S1, G-M1. Contrast the named criticism in L-P1 and L-P3.
- **When it matters:** reads as evasive to practitioners. Acceptable when naming someone would be a legal or political risk.

### M11. Uniform long sentences
- **Category:** structural
- **Tags:** `src: IN CF AB SL` · `ev: obs meas` · `ch: all` · `reg: all` · `status: revised: spread-not-length`
- **What it looks like:** mean sentence length of 22 words or more with a low standard deviation (about 7). No fragments, and no short sentence closing a paragraph.
- **Observed:** G-P1, G-P2, G-P4; C-PP13 (extreme case).
- **When it matters:** always a signal. Worst in short messages.
- **Baseline check (section 7):** **revised. This is an institutional marker; the AI version is different.**
  - The AI practitioner texts had *shorter* sentences than the humans: a mean of 15.3 words against 25.3 for early Latio.
  - They also had more short sentences: 13.5% against 6.1%.
  - What separated them was the spread. The standard deviation was 8.5 against 18.2, because the AI texts lack the long, clause-stacked sentences that humans mix in.
  - Detect low spread, not long average length. Do **not** "fix" AI text by adding short punchy sentences, because the AI already writes them.

### M12. Summarizing or moral close
- **Category:** structural
- **Tags:** `src: PW` · `ev: obs` · `ch: email dm` · `reg: all` · `status: corpus-only`
- **What it looks like:** the last line restates the point as a general principle or aphorism.
- **Observed:** L-P7, L-P9 (late register). Gartner does **not** do this (G-P1, G-P2, G-P4 just stop).
- **When it matters:** acceptable in long-form opinion. Fatal in email, where the close should be the ask.

### M13. "It's clear that…" or "On the one hand…" scaffolding
- **Category:** framing
- **Tags:** `src: PW` · `ev: obs` · `ch: all` · `reg: all` · `status: corpus-only`
- **What it looks like:** a stock frame announcing certainty or balance before the content.
- **Observed:** L-P4, L-P6, L-P9.
- **When it matters:** low severity alone. High severity when it opens the message.

### M14. Self-promotional superlatives
- **Category:** sales_cliche
- **Tags:** `src: IN PW SL` · `ev: obs lab` · `ch: email dm voicemail` · `reg: stranger exec` · `status: confirmed-quality`
- **What it looks like:** "world's leading," "premier," "most hyped," "hottest."
- **Observed:** G-P1, G-P4, I-1, L-P8.
- **When it matters:** fatal in outreach to strangers and to executives.
- **Sales check (section 8):** superlatives such as "industry-leading", "#1", "world-class", "innovative" and "trusted by" appeared in 29 of 835 labelled sales messages. 90% of those were labelled weak, against a 20% base rate.
  - This is the highest-precision marker tested.
  - It is rare, though, so it catches only a minority of weak messages.

### M15. Vague open-ended commitment
- **Category:** calibration
- **Tags:** `src: CF SL` · `ev: obs lab` · `ch: email dm` · `reg: all` · `status: partial: 45%-weak-precision`
- **What it looks like:** "happy to help however I can," "every possible amends," with no specifics.
- **Observed:** C-PP13 (unspecified promise of amends).
- **When it matters:** fatal as a closing line. Replace it with a bounded offer (see H06).

### M16. Hedge that softens stance rather than scope
- **Category:** calibration
- **Tags:** `src: AB` · `ev: inf meas` · `ch: all` · `reg: all` · `status: unsupported`
- **What it looks like:** "might potentially," "could possibly help" applied to the writer's own view, not to the limits of the evidence.
- **Observed:** **insufficient evidence in this corpus.** Gartner barely hedges (G-P4), and Latio's hedges mark scope (L-P2). This marker is included from general knowledge of LLM output and needs validation (see section 6).
- **Baseline check (section 7):** **not supported for the models sampled.** Hedge rates per 1,000 words:
  - AI analyst 1.6 vs Gartner 2.6.
  - AI practitioner 2.2 vs early Latio 2.7.
  - AI B2B messages 8.2 vs the classic letters 8.1.
  - Keep this marker only as a per-sentence check, not a rate.
- **When it matters:** —

### M18. Placeholder slots instead of specifics
- **Category:** calibration
- **Tags:** `src: AB SL` · `ev: meas lab` · `ch: email dm` · `reg: all` · `status: narrowed: authenticity-only`
- **What it looks like:** bracketed slots ([Name], [Tool], [X]) where a human writer would put a fact, or would leave the claim out.
- **Observed:** AI baseline B2B messages averaged 11.5 slots each, with Opus at 14.6 (section 7). No human text in the corpus has them.
- **When it matters:** this is a symptom of the real problem. The draft was written with no facts. A rewriter should treat each slot as a required input, and drop the sentence if the fact isn't available. It should never fill a slot with a generic stand-in.
- **Scope (section 8): an authenticity marker only, not a quality marker.**
  - In the labelled sales set, 68% of messages with placeholders were labelled strong, mostly call and video scripts that are meant to be filled in.
  - Use M18 to detect an unfinished draft (a slot that was never filled), not to grade the message.
  - Templates and scripts are exempt.

### M19. Institutional "we" in one-to-one messages
- **Category:** framing
- **Tags:** `src: AB CL ES` · `ev: meas obs` · `ch: email dm` · `reg: stranger peer` · `status: confirmed-AI-diff; guarded; exec-voice-exempt`
- **What it looks like:** "we," "our," "us" dominate a message sent from one person to another.
- **Observed:** AI baseline B2B messages used 31 per 1,000 words, against 3 in the classic letters (section 7). The classic writers speak as "I" (C-LH, C-LG).
- **When it matters:** fatal in a cold request or an intro, where the reader is deciding about a person. Acceptable in procurement, where the company is the party.
- **Exemption (section 9): the executive or company voice.** Executives speaking for their company use "we" at about 52 per 1,000 words, both scripted and live. Do not flag "we" when the writer is speaking as the company. Keep M19 for one-person-to-one-person requests.

### M20. Rhetorical contrast frames ("not X but Y," "not just," "it's not about X")
- **Category:** structural
- **Tags:** `src: AB PW SL` · `ev: meas lab` · `ch: all` · `reg: all` · `status: narrowed: rhetorical-only`
- **What it looks like:** a claim built by rejecting a strawman first.
- **Scope (narrowed, section 8):** flag only *rhetorical* contrasts, where the rejected view is a strawman nobody in the conversation holds. Do **not** flag *mechanism* contrasts that explain how something works, e.g. "managers approve instead of texting 14 people" or "reviews suggested edits rather than starting from a blank document".
  - In the labelled sales set, 85% of messages containing "instead of" or "rather than" were labelled strong and 0% weak, because those contrasts carry the mechanism (H20).
- **Observed:**
  - AI analyst texts: 2.7 per 1,000 words, against 0.4 for Gartner.
  - AI practitioner texts: 2.3, against 0.9 for early Latio.
  - Latio's transitional posts reach 4.4 (L-P4, L-P5; n=2), but the 2026 posts are back to 0.9 (L-P6, L-P7, L-P9). The rate is not a stable property of the late register.
- **When it matters:** one per piece is fine. Repeated use is a strong signal.

### M21. Missing named entities in expert content
- **Category:** calibration
- **Tags:** `src: AB PW` · `ev: meas` · `ch: long-form` · `reg: tech-buyer peer` · `status: confirmed-AI-diff; vendor-list-bias`
- **What it looks like:** an explainer, opinion piece or guide that discusses a market without naming any company, product or version.
- **Observed:** 8 of 9 AI practitioner texts named none of 42 checked security vendors, and the 9th named 2. Early Latio named 15 (L-P1), 5 (L-P2) and 9 (L-P3) from the same list (section 7).
- **When it matters:** fatal for technical buyers and practitioners. Of all the metrics measured, this was the largest single gap between the AI and practitioner texts.

### M22. Transformation hype verbs
- **Category:** sales_cliche
- **Tags:** `src: SL` · `ev: lab` · `ch: email dm voicemail call` · `reg: stranger exec` · `status: confirmed-quality (labeler only)`
- **What it looks like:** "transform your business", "unlock", "empower", "streamline", "revolutionize", "supercharge", "take X to the next level", "digital transformation".
- **Observed:** 12 of 835 labelled sales messages; 92% of them were labelled weak (section 8). The institutional version is M04.
- **When it matters:** fatal in outreach. It is rare, so it catches only a few weak messages.

### M23. Manufactured urgency and pressure on the ask
- **Category:** sales_cliche
- **Tags:** `src: SL` · `ev: lab code` · `ch: email dm call` · `reg: stranger` · `status: confirmed-quality (labeler only)`
- **What it looks like:**
  - Invented deadlines or scarcity ("time is running out", "spots filling fast", "offer expires").
  - Fixed meeting times offered before any interest is shown.
  - Assumed interest ("let's get 30 minutes on the calendar tomorrow").
- **Observed:**
  - Urgency phrasing: 22 of 835 sales messages, 73% labelled weak.
  - Ask pressure, coded blind: higher in the weak message in 18 of 22 matched weak/strong pairs (Opus coder). The Haiku coder agreed on direction but found it in only 7 pairs.
  - (Section 8.)
- **When it matters:** fatal in cold outreach. A real, stated deadline is a fact, not this marker.

### M24. Scripted register in a live channel
- **Category:** structural
- **Tags:** `src: ES AB` · `ev: meas code` · `ch: spoken call dm email` · `reg: all` · `status: confirmed-AI-diff`
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

### M17. Status signaled by title, not by decision
- **Category:** rhetorical
- **Tags:** `src: IN CF` · `ev: obs` · `ch: email` · `reg: exec` · `status: corpus-only`
- **What it looks like:** credibility asserted through rank, titles or affiliations rather than through what the writer did or decided.
- **Observed:** G-P4 (full analyst titles); C-PP13 and C-PP19 (patron). Contrast C-LH, where status shows in the stated decision.
- **When it matters:** fatal from vendor to executive.

---

## 3. human_patterns

Each pattern lists its category, a generic description, where it was observed, the registers it suits, and how it shows up in modern business writing.

### H01. Point first
- **Category:** structural
- **Tags:** `src: CL PW` · `ev: obs` · `ch: all` · `reg: all` · `status: corpus-only`
- **Description:** the first sentence carries the decision, the ask, or what the message responds to.
- **Observed:** C-LH, C-LG, C-LB, C-FR1. Latio's verdict-first TL;DR (L-P1).
- **Suits:** all registers, and especially exec.
- **Modern equivalent:** the email's opening line is the ask or the news, e.g. "Asking if you'd take 20 min on X." Context comes after.

### H02. Endorse only what you know
- **Category:** calibration
- **Tags:** `src: CL PW` · `ev: obs` · `ch: all` · `reg: peer tech-buyer stranger procurement` · `status: corpus-only`
- **Description:** the scope of a claim or recommendation is explicitly limited to the writer's actual knowledge, and the limit is stated.
- **Observed:** C-FR1 ("though I know nothing of him, not even his name"); C-DG (admits he is not a botanist); L-P1 (brief demos only; speculation flagged); L-P2 (hasn't tested every tool).
- **Suits:** peer, technical buyer, intro, procurement.
- **Modern equivalent:** "I've only seen their demo, not run it in prod." Or, in an intro: "I know her from one project, so judge for yourself."

### H03. Disclose interest up front
- **Category:** rhetorical
- **Tags:** `src: PW` · `ev: obs` · `ch: long-form email dm` · `reg: peer tech-buyer` · `status: corpus-only; coding-unreliable`
- **Description:** state the money, sponsorship or relationship that could bias the claim, before making it.
- **Observed:** L-P1 ("I have taken $0 from any CNAPP provider ever."); L-P4 (vendor-provided access disclosed in the opening); L-P3.
- **Suits:** peer, technical buyer, analyst-style posts.
- **Modern equivalent:** "Full disclosure: they're a customer of ours." Or: "No affiliation, just used it."

### H04. Credibility from method, not rank
- **Category:** rhetorical
- **Tags:** `src: CL PW` · `ev: obs` · `ch: all` · `reg: all` · `status: corpus-only`
- **Description:** cite how you know: what you ran, read, measured or were told, and by whom.
- **Observed:** C-LB (official record); C-LH (states how he heard it); C-DG (research purpose stated); L-P2 (years running the tool).
- **Suits:** all registers.
- **Modern equivalent:** "We ran it against 3 repos last quarter." Not: "As a leading provider…"

### H05. Specificity density
- **Category:** lexical
- **Tags:** `src: CL PW AB` · `ev: obs code` · `ch: all` · `reg: tech-buyer IC procurement` · `status: confirmed-AI-diff`
- **Description:** named entities, counts, versions and dates carry the message. Remove them and the message collapses.
- **Observed:** C-DG (exact labels, a species count); L-P1 (about 26 vendors, deal dates); L-P6 (877,000 packages, version pins); L-P9 (CVE IDs).
- **Suits:** technical buyer, IC, procurement.
- **Modern equivalent:** "Your Snyk renewal is in March," not "your current tooling."

### H06. Lower the cost of the ask
- **Category:** framing
- **Tags:** `src: CL SL` · `ev: obs code lab` · `ch: email dm` · `reg: stranger exec` · `status: confirmed-quality`
- **Description:** state the size of the request and make it cheap: from memory, yes or no, a short window.
- **Observed:** C-DG (asks for an answer from memory; says it should be little trouble).
- **Sales check (section 8): confirmed on 835 labelled sales messages.**
  - **A smaller ask separated strong messages from weak.** Separation was 0.77 / 0.82 for the two coders (where 0.5 means no difference). Weak messages asked for demos and long meetings.
  - **An explicit opt-out marked strong messages.** Messages with phrasing like "if not, no worries" or "tell me and I'll stop" were 87% strong.
- **Suits:** cold request, exec, stranger.
- **Modern equivalent:** "A one-line reply is plenty." Or: "Even 'not a fit' helps."

### H07. Flagged extra ask
- **Category:** speech_act
- **Tags:** `src: CL` · `ev: obs` · `ch: email dm` · `reg: peer stranger` · `status: corpus-only`
- **Description:** a second request is explicitly marked as additional and optional, not slipped in.
- **Observed:** C-DG (marks a final additional question as such).
- **Suits:** peer, stranger.
- **Modern equivalent:** "Separate, smaller question: …"

### H08. Specific praise, then specific criticism, then expectation
- **Category:** rhetorical
- **Tags:** `src: CL PW` · `ev: obs` · `ch: email dm` · `reg: peer friction subordinate` · `status: corpus-only`
- **Description:** qualified, concrete credit, then a named problem, then what is now expected, with support offered within stated limits.
- **Observed:** C-LH (the full sequence); C-CN; L-P1 (criticism by name, then still rates the product best in its category).
- **Suits:** cross-team friction, peer, superior to subordinate.
- **Modern equivalent:** "Your team shipped the migration early. The alert noise it added cost us two on-call nights. Can we agree on thresholds by Friday?"

### H09. Owned opinion
- **Category:** rhetorical
- **Tags:** `src: CL PW ES` · `ev: obs meas code` · `ch: all` · `reg: peer tech-buyer exec` · `status: confirmed-AI-diff (weak coder agreement)`
- **Description:** the evaluative claim is stated in the writer's own voice, flatly, without attributing it to experts or the institution.
- **Observed:** C-LG (first-person position statements); L-P3 (names a winner; first-person argument); L-P5 (first-person prediction).
- **Suits:** peer, technical buyer, exec (sparingly).
- **Modern equivalent:** "My take: build it in-house." Not: "Many experts suggest considering…"
- **Earnings check (section 9):** "I"-stance phrases ("I think", "my view") rise from 0.3 per 1,000 words in prepared remarks to 6.6 live. In blind coding, human answers own a view more often than AI answers. The two coders agree only weakly on this item (r = 0.43).

### H10. Uneven rhythm with a short landing
- **Category:** structural
- **Tags:** `src: CL PW AB SL ES` · `ev: obs meas` · `ch: all` · `reg: all-but-procurement` · `status: confirmed-AI-diff`
- **Description:** sentence length varies widely, and a short sentence or fragment closes the paragraph or message.
- **Observed:** C-LH (closes on a short command); C-LG (short declarative landing); L-P1 and L-P2 (3–4-word fragments).
- **Suits:** all except formal procurement.
- **Modern equivalent:** two medium sentences, then "Worth a look?" or "That's the whole ask."
- **Earnings check (section 9):** sentence-length spread is higher live than in prepared remarks in 10 of 12 calls. Live human answers measure 14.7, AI answers 10.3.

### H11. Status through decisions
- **Category:** speech_act
- **Tags:** `src: CL` · `ev: obs` · `ch: email` · `reg: exec` · `status: corpus-only`
- **Description:** authority is shown by what you decided or did. Titles are omitted, and the salutation is bare.
- **Observed:** C-LH (bare-rank salutation; opens by stating his decision).
- **Suits:** exec, superior to report.
- **Modern equivalent:** "We moved the launch to Q2." No title block or "As VP of…" preamble.

### H12. Short flat refusal
- **Category:** speech_act
- **Tags:** `src: CF` · `ev: obs` · `ch: email dm` · `reg: procurement friction` · `status: corpus-only`
- **Description:** decline in a few words, without stacked justification, and refuse the other party's framing.
- **Observed:** C-PP56 (Elizabeth's short declaratives against Lady Catherine's stacked rhetorical questions).
- **Suits:** procurement, friction, vendor pushback.
- **Modern equivalent:** "We won't do a 3-year term." One reason at most.

### H13. Segmented recommendation
- **Category:** calibration
- **Tags:** `src: PW RT` · `ev: obs` · `ch: long-form email` · `reg: tech-buyer peer` · `status: corpus-only`
- **Description:** the recommendation depends on the reader's situation. There is no single universal answer.
- **Observed:** L-P1 (existing customers vs. dev-first teams); C-CI (decorum: fit to audience).
- **Suits:** technical buyer, peer.
- **Modern equivalent:** "If you're already on Wiz, fine. If devs own it, look at Aikido."

### H14. Named criticism with fairness caveat
- **Category:** rhetorical
- **Tags:** `src: PW AB` · `ev: obs code` · `ch: long-form dm` · `reg: peer tech-buyer` · `status: confirmed-AI-diff`
- **Description:** criticize a named product or practice, and in the same breath acknowledge where it is strong.
- **Observed:** L-P1; L-P3 (explicit fairness caveat about a named competitor).
- **Suits:** peer, technical buyer.
- **Modern equivalent:** "Their SAST is weak; their CSPM is the best I've used."

### H15. Explicit uncertainty marker, used sparingly
- **Category:** calibration
- **Tags:** `src: CL PW ES` · `ev: obs meas` · `ch: all` · `reg: all` · `status: confirmed-AI-diff`
- **Description:** a single plain marker where the evidence is actually thin ("total guess," "not sure yet"); everything else is stated flatly.
- **Observed:** L-P1 (flags a guess as a guess); L-P2 (marks open questions); C-LG (commits to revising when shown wrong); C-CS.
- **Suits:** all registers.
- **Modern equivalent:** "Pure guess, but I think they get acquired." Every other claim stays unhedged.
- **Earnings check (section 9):** hedges run at 1.1 per 1,000 words in prepared remarks and 2.5 in live answers. AI answering live used 0.3.

### H16. Peer register markers
- **Category:** lexical
- **Tags:** `src: PW` · `ev: obs` · `ch: dm long-form` · `reg: peer IC` · `status: corpus-only`
- **Description:** occasional slang, humor or self-aware aside signals a peer relationship.
- **Observed:** L-P1, L-P2, L-P3.
- **Suits:** peer and IC only. Risky with exec and procurement.
- **Modern equivalent:** a single light aside per message at most, e.g. "(yes, another acronym)."

### H17. Concealed art
- **Category:** lexical
- **Tags:** `src: RT CL` · `ev: obs` · `ch: all` · `reg: all` · `status: corpus-only; sources-unverified`
- **Description:** ordinary words, few epithets, no ornamental metaphor. The writing should not look written.
- **Observed:** C-AR III.2–3 (summarized, not fetched); C-CI *Orator* §§76–90; exemplified in C-LB and C-LH.
- **Suits:** all registers.
- **Modern equivalent:** cut every adjective that isn't load-bearing.

### Content-level patterns (H18–H21)

These come from blind content coding of labelled sales messages (section 8). They are about *what* the message says. A rewrite cannot add them, because it is not allowed to invent facts, so they must be checked when the message is drafted.

In each pattern below:
- **Separation** runs from 0.5 (no difference between strong and weak messages) to 1.0 (always tells them apart).
- **Pairs** counts the 22 matched pairs (a weak and a strong message for the same scenario) where the strong message had the pattern and the weak one did not.
- Each figure is given as two numbers, one per coder: Opus / Haiku.

### H18. Buyer-centric sentences
- **Category:** framing
- **Tags:** `src: SL` · `ev: code lab` · `ch: email dm voicemail call` · `reg: stranger exec` · `status: confirmed-quality (labeler only)`
- **Description:** most sentences are about the buyer, their team or their situation. Fewer are about the seller or the product.
- **Observed:**
  - Separation 0.93 / 0.93.
  - Strong messages were higher in 20 / 21 of the pairs.
  - Strong messages averaged about 58% buyer-centric sentences, weak messages about 30% (section 8).
  - The classic analogue is Darwin's request, which is built around what Gray already knows (C-DG).
- **Suits:** all outreach.
- **Modern equivalent:** "Your team re-maps 22 clinics' books by hand each month", not "Ledgerline offers…".

### H19. Industry- or role-specific pain
- **Category:** calibration
- **Tags:** `src: SL` · `ev: code lab` · `ch: email dm voicemail call` · `reg: stranger exec` · `status: confirmed-quality (labeler only)`
- **Description:** names a problem that is specific to the buyer's industry or role, not a generic one.
- **Observed:**
  - Separation 0.91 / 0.98.
  - Pairs: 18 / 21.
  - Weak messages had it 0% of the time by the Opus count and 5% by the Haiku count.
- **Suits:** all outreach.
- **Modern equivalent:** "Fuel-card and freight-settlement matching", not "manual reconciliation".

### H20. Mechanism in the buyer's terms
- **Category:** calibration
- **Tags:** `src: SL` · `ev: code lab` · `ch: email dm call` · `reg: tech-buyer exec` · `status: confirmed-quality (labeler only)`
- **Description:** explains *how* the product produces the outcome, often as a contrast with how the buyer does it today. This is the mechanism contrast that M20 now exempts.
- **Observed:**
  - Separation 0.84 / 0.86.
  - Pairs: 15 / 16.
  - No weak message in the coded sample explained the mechanism.
- **Suits:** technical buyer, operator, exec (one sentence).
- **Modern equivalent:** "Managers approve swaps instead of texting 14 people."

### H21. Value before the ask
- **Category:** speech_act
- **Tags:** `src: SL` · `ev: code lab` · `ch: email dm` · `reg: stranger exec` · `status: confirmed-quality (labeler only)`
- **Description:** offers something useful that doesn't depend on getting a meeting: a resource, a sample, a read-only scan, or an anonymized example.
- **Observed:**
  - Separation 0.84 / 0.84.
  - Pairs: 15 / 15.
  - No weak message in the coded sample offered value before the ask.
  - The classic analogue is Darwin offering to cut Gray's effort (C-DG).
- **Suits:** cold outreach, exec, re-engagement.
- **Modern equivalent:** "I can send a one-page summary. No call needed."

### H22. Think-aloud answer
- **Category:** structural
- **Tags:** `src: ES` · `ev: meas code` · `ch: spoken call dm email` · `reg: exec peer tech-buyer` · `status: confirmed-AI-diff`
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
- **Modern equivalent:** "So, honestly, I think the slowdown is mostly timing, because two big deals slipped into January. The pipeline itself looks fine."

---

## 4. transformations

**Guards for any rewrite pipeline (from evals A and sales-A, section 8):**
- **Keep the strength of every ask, deadline, commitment and claim.** In particular, never change "I'd like" to "I need", never firm up or soften a deadline, and never turn a reported claim into a stated one.
- **Don't add enthusiasm** ("delighted").
- **Run a deterministic drift check before judging.** Compare modal verbs, hedges and quantifiers (would, could, may, might, typically, about, up to, roughly) between the original and the rewrite.
  - LLM judges caught a "would be" → "is" price change in only 1 of 4 runs.
  - They do catch large changes to an ask.
- **Judge each pair in both orders.** Single-order preferences were mostly position bias. Once counterbalanced, judges gave no stable preference in 17 of 24 pairs.
- **A style rewrite does not improve a weak message.** Quality grades were unchanged after rewriting. If H18–H21 are missing, the fix is to redraft, not to rewrite.
- **Contractions alone are not evidence of conversational text.** AI answering live used more contractions than executives did (34.8 vs 28.6 per 1,000 words). Weight discourse openers, owned stance (H09) and reasoning (H22) instead (section 9).
- **Do not carry spoken disfluencies into writing.** Discourse openers and owned stance transfer to a DM or a reply; "um", restarts and repairs do not. This is untested against written outcomes.

Each entry gives the AI marker, the human pattern that replaces it, and the conditions under which the swap applies.

1. **M01 ceremonial preamble → H01 point first**
   - **Applies:** always in email and DM.
   - **Exception:** keep one reconnecting clause if there is a real prior contact (C-DG).
2. **M02 self-certified virtue → H04 credibility from method**
   - **Applies:** all registers and channels.
   - **How:** delete the self-assessment and replace it with a fact about what was done.
3. **M03 inverted formula ratio → H05 specificity density**
   - **Applies:** all registers.
   - **How:** for every courtesy formula kept, there must be at least one concrete fact.
   - **Note:** formal procurement can keep more formula if it keeps the facts too.
4. **M04 abstract verbs → plain actor and action** (H17, H05)
   - **Applies:** peer, IC, technical buyer, all channels.
   - **Exception:** keep a term only when it is the reader's own category name.
5. **M05 reflexive triplet → the true count**
   - Use one or two items if that is how many exist; use a fragment for emphasis (H10).
   - **Applies:** all registers, and especially LinkedIn, where triplets read as templated.
6. **M06 templated list → prose with uneven items**
   - **Applies:** email and DM.
   - **Exception:** keep lists in docs, RFP responses and runbooks.
7. **M07 role address → "you" plus their specific situation** (H05)
   - **Applies:** one-to-one channels.
   - **Exception:** in public posts, address a segment but name a concrete scenario.
8. **M08 laundered opinion → H09 owned opinion**
   - **Applies:** peer, technical buyer.
   - **Exec variant:** pair the opinion with one fact (H04).
9. **M09 benefit stack → one outcome with a mechanism or number** (H05)
   - **Applies:** technical buyer, procurement.
   - **Variant:** if there is no number, add H02 (scope the claim).
10. **M10 category-only criticism → H14 named criticism with fairness caveat**
    - **Applies:** peer and analyst-style content.
    - **Do not apply:** when naming someone is a legal or political risk, or in exec outreach about a competitor.
11. **M11 uniform long sentences → H10 uneven rhythm**
    - **Applies:** all registers.
    - **Target:** at least one sentence under 6 words per paragraph in email.
12. **M12 moral close → H06 or H07 ask-close, or simply stop**
    - **Applies:** email and DM.
    - **Exception:** long-form posts may end on a forward-looking question (L-P3).
13. **M13 certainty scaffold → state the claim**
    - **How:** delete "It's clear that"; if the claim is not clear, use H15.
    - **Applies:** all registers.
14. **M14 superlatives → H03 disclosure or H04 method**
    - **Applies:** cold outreach and exec.
15. **M15 vague offer → H06 bounded offer**
    - **How:** "I can send the 2-page benchmark."
    - **Applies:** all registers.
16. **M16 stance hedge → H15 single scope marker**
    - **How:** remove the hedges from the opinion and add one marker where the evidence is thin.
    - **Applies:** all registers.
17. **M17 title-based status → H11 status through decisions**
    - **Applies:** exec and senior-to-junior.
    - **Note:** a signature block is fine; titles stay out of the body.
18. **M18 placeholder slots → H05 specificity density, or deletion**
    - **How:** each slot becomes a required input. If no fact is available, cut the sentence. Never fill it with a generic phrase.
    - **Applies:** all channels.
19. **M19 institutional "we" → first-person "I" with H04 method**
    - **Applies:** cold request, intro, peer, friction.
    - **Exception:** keep "we" when stating company terms in procurement.
    - **Guard:** swap only when "we" means the writer personally. In eval A, "we're evaluating" → "I'm evaluating" changed who was doing the evaluation.
20. **M20 rhetorical contrast → state the positive claim directly**
    - **How:** keep at most one rhetorical contrast per piece, and only when the contrasted view is one the reader actually holds.
    - **Do not apply:** to mechanism contrasts (H20). Leave those as they are.
    - **Applies:** all registers.
21. **M21 no named entities → H05 and H14**
    - **How:** name the products, versions or companies the claim is about, with H02 scoping for any you have not used.
    - **Applies:** technical buyer, peer, analyst-style posts.
    - **Do not apply:** in exec outreach that would read as attacking a competitor.
22. **M22 transformation hype → H20 mechanism, or delete**
    - **How:** replace "transform your business" with the one concrete thing the product changes. If the draft doesn't give that, delete the phrase. Do not invent a mechanism.
    - **Applies:** all outreach.
23. **M23 manufactured urgency → H06 smaller ask plus an opt-out, and H21 value before the ask**
    - **How:** remove invented deadlines and fixed times. Keep any real deadline exactly as stated.
    - **Applies:** cold outreach, follow-up.
    - **Note:** reducing the size of the ask changes meaning. A rewriter must not do it unless the user approves. Flag it as a redraft suggestion instead.
24. **M24 scripted register in a live channel → H22 think-aloud answer**
    - **How:**
      - Lead with the direct answer or view, then give the reason.
      - Keep the one figure the question asked for, and cut the rest. This is allowed only when the figures were not requested. Never cut a figure the asker wanted.
      - Remove stock forward-looking phrases. Keep any real guidance word for word.
    - **Applies:** DM, call, follow-up email, any live reply.
    - **Do not apply:** to written reports or prepared remarks.

**Draft-time checks (not rewrites).** Missing H18–H21 content can't be added by a style pass. Report it as a gap for the writer to fill:
- no buyer-specific trigger;
- no industry pain;
- no mechanism;
- nothing of value before the ask;
- no proof point.

---

## 5. speech_act_map

### 5.1 Cold request to a stranger

- **Classic:** Darwin to a senior specialist (C-DG):
  1. A one-sentence link to a prior meeting.
  2. The favor named.
  3. The cost lowered (answer from memory).
  4. Exact instructions.
  5. A flagged extra ask.
  6. A deferential close.
- **Institutional:** no person-to-person requests in the sample. Methodology pages use imperatives addressed to a generic "you" (G-M1). **Insufficient evidence for 1:1 requests.**
- **Latio:** no cold requests to individuals in the sample. CTAs are subscribe or install prompts (L-P6, L-P8). **Insufficient evidence.**
- **Best transfer:** Darwin's sequence, with the humility formulas compressed to one clause. Combine H01, H06, H05 and H07.

### 5.2 Introduction through a mutual contact

- **Classic:** Franklin's model recommends exactly as much as the writer can vouch for and hands judgment to the reader (C-FR1). Collins introduces himself through his patron's status, and the text presents this as hollow (C-PP13).
- **Institutional:** **insufficient evidence.**
- **Latio:** the closest analogue is disclosure of the relationship (L-P4), plus crediting others (L-P9).
- **Best transfer:** scoped endorsement (H02) plus the reason for connecting these two specific people (H05). Avoid inflated praise of the person being introduced.

### 5.3 Message to a senior executive

- **Classic:**
  - Lincoln writing downward shows what executives themselves write: decision first, status by action, bare salutation, short directive close (C-LH).
  - Elizabeth facing a superior: short declaratives, no deference to rank-based appeals (C-PP56).
- **Institutional:** addresses executives as a third-person role (G-P4), with obligation verbs and dated forecasts.
- **Latio:** not directly addressed to executives in the sample. Its framing of one category as the best place to spend budget (L-P5) is the closest.
- **Best transfer:** match the executive's own register. That means H01 and H11, one decision-relevant number (H05), and a short close (H10). The dated forecast format can carry one claim, but only with a source.

### 5.4 Raising cross-team friction

- **Classic:** Lincoln's sequence (decision, qualified praise, specific charge, expectation, bounded support, consequence, directive; C-LH). Chekhov adds a candor marker before the hard part (C-CN). Lincoln to Greeley: courteous surface, and he declines to fight each point (C-LG).
- **Institutional:** only category-level criticism (G-S2). Does not transfer to 1:1 friction.
- **Latio:** names the product, gives balanced praise, and states the problem flatly (L-P1, L-P3).
- **Best transfer:** H08 and H14 in a compressed version: one specific credit, one specific problem, one concrete ask with a date.

### 5.5 Commercial or procurement question

- **Classic:** C-PP56, refusing terms without stacked justification (H12). Darwin's exact instructions (C-DG) are a model for precise asks.
- **Institutional:** the MQ page frames decisions as questions and warns against picking a leader by default (G-M1). Useful framing, impersonal voice.
- **Latio:** prices are almost absent from body text (only a $0 disclosure, L-P1). **Insufficient evidence** on commercial negotiation.
- **Best transfer:** H12 for refusals, H05 for asks (named SKUs, terms, dates), and H13 for "depends on your situation" answers.

---

## 6. findings_vs_inferences

### 6.1 Observations (directly in the texts)

1. **Gartner (8-piece corpus):** zero instances of delve, landscape, navigate, journey, unlock, moreover, furthermore, or "in conclusion."
2. **Gartner forecasts are nearly unhedged:** "will" ×24, "may" ×0 (G-P4).
3. **Gartner uses heavy triplets and abstract verbs:** up to 16 triplets per piece; "enable" ×14 (G-S2).
4. **Gartner never names vendors and has no authorial "I"** in press releases or methodology pages (G-P1, G-P2, G-P4, G-H1, G-M1).
5. **Gartner pieces do not summarize.** They end in upsell and boilerplate (G-P1, G-P2, G-P4).
6. **Gartner contains human editing errors,** e.g. subject–verb disagreement (G-P1) and typos (G-S2, G-P4).
7. **Latio's register changed between 2024 and 2026.**
   - "I" went from 42 per piece (L-P1) through 11 and 6 (L-P4, L-P5) to 0 (L-P6, L-P8), counted in the raw text.
   - Checklist format and aphoristic closes increased (L-P6, L-P7, L-P9).
8. **Latio's early register** names 20+ vendors per piece, discloses money, and flags speculation (L-P1, L-P3).
9. **Classic letters that work** put the point in sentence one and run 140–520 words (C-LH, C-LG, C-LB, C-FR1, C-DG).
10. **Austen's padded, self-certifying speaker** has low sentence variance and borrowed status (C-PP13, C-PP19).

### 6.2 Inferences (interpretation)

1. **Hypothesis F, "Default AI prose resembles institutional analyst prose more than practitioner or literary prose": partially supported, and reframed.**
   - **Supported on structure:** triplets, templated lists, abstract enabling verbs, impersonal role address, short even paragraphs, and unevidenced benefit lists (G-S1, G-S2) all line up with common LLM output.
   - **Rejected on calibration and lexicon:**
     - Gartner is *over*-certain (dated, falsifiable percentages), not hedged.
     - Gartner coins proprietary terms rather than using stock vocabulary.
     - Gartner uses none of the LLM tic words.
     - Gartner stops instead of summarizing.
   - **Closest match on social posture:** Austen's Collins is a closer match than Gartner to LLM *social* posture: ceremonial preamble, self-certified goodwill, vague offers, low formula-to-substance ratio (C-PP13).
   - **Best-supported reframe:** default AI prose = institutional *structure* + Collins-like *ceremony* + a hedging habit that neither source shows strongly.
   - **Revised after the baseline (section 7): not supported as stated.**
     - **Genre decides.** The AI texts land closest to whatever genre they were asked to write, not to institutional prose in general.
     - **Distances (lower = more alike), on 16 standardized metrics:**
       - AI analyst texts: 4.44 from Gartner, 4.57 from late Latio, 4.82 from transitional Latio, 5.11 from early Latio.
       - AI practitioner texts: 4.68 from late Latio, 4.84 from early Latio, 5.50 from Gartner.
       - **These margins are small and not robust.** With the two December 2025 posts grouped into "late", late Latio came out closest to the AI analyst texts (4.32 vs 4.58 for Gartner). Splitting them out flipped the order.
     - **The sentence-rhythm match with Gartner is near-exact:** mean 20.7 vs 20.9 words, coefficient of variation 0.5 vs 0.5.
     - **Where AI differs from Gartner:**
       - About 2× the triplets.
       - About 7× the contrast frames.
       - One-sixth the abstract enabling verbs.
       - Fewer hedges.
     - **The "hedging habit" part of the reframe is not supported** for these models.
     - **Restated hypothesis:** AI prose shares institutional *rhythm and distance* (no vendors, no first-person stake), but it has its own *cadence markers* (triplets, contrast frames) that neither human source uses at that rate. No single human source is clearly closest: Gartner and 2026 Latio are within 0.15 of each other on this metric.
2. **The human signal is a ratio, not a single feature.** Darwin uses as much courtesy formula as Collins, but reads as genuine because specifics outweigh formula (C-DG vs C-PP13). Detectors should score substance per formula, not just flag formulas.
3. **Format drives voice more than authorship does.** Latio's checklist and announcement pieces (L-P6, L-P8) show institutional and AI-like traits in human-authored text. A rewrite system should strip those formats in 1:1 channels rather than treat their presence as proof of AI authorship.
4. **Disclosure and scoped endorsement (H02, H03) are the most transferable trust patterns across centuries.** They appear in both C-FR1 and L-P1.

### 6.3 Open questions (needs more data)

1. **The LLM baseline (section 7) covers Claude models only.**
   - No GPT, Gemini or Llama outputs were sampled.
   - There is one sample per model per prompt.
   - The texts were generated by subagents whose system prompt is oriented to coding, not by bare API calls.
   - The "tic words" result (zero across all corpora) may not hold for other model families or older models.
   - Next step: repeat with other providers through bare API calls, with 3–5 samples per prompt.
2. **Forrester and a second IDC sample are missing,** so cross-firm generalization is unsupported.
3. **Latio's PDF reports were not read.** It is unknown which register the report bodies follow.
4. **The cause of the Latio drift is unknown:** audience growth, team authorship, format, or tooling. **Insufficient evidence**, and not something this analysis should speculate about.
5. **Sources not checked against primary documents this session:**
   - Franklin's letter was checked only via a secondary transcription.
   - Aristotle and Cicero are summarized from memory of standard translations.
   - All of these should be verified before the patterns that cite them (H17, parts of H02) are treated as fully grounded.
6. **No real B2B email corpus.** The "modern business equivalent" lines are constructed illustrations, not observed messages. Validating them needs a sample of real, pre-2022 B2B emails rated by human recipients.
7. **Trollope and Twain status dialogue was not examined.**
8. **Real buyer outcomes are untested.** The sales evidence in section 8 comes from a dataset in which the quality labels and the buyer replies appear to have been generated along with the messages. M22, M23, H18–H21 and the sales checks on M01, M14, M18 and M20 have only been validated against that labeler. Validating them needs real sends with real reply and meeting data.
9. **Spoken evidence is from public, media-trained speech.** Earnings calls are legally constrained (safe-harbor rules), and vendor transcripts remove filler words. Private sales conversations may differ. M24 and H22 still need validating on real call recordings.

---

## 7. AI baseline: matched-prompt comparison (added 2026-11-19)

### 7.1 Method

- **Prompts:** 11 plain writing requests matched to the corpus genres:
  - 3 analyst prompts: a press release with a prediction, a trends article, a methodology page.
  - 3 practitioner prompts: a CDR explainer, a CNAPP market opinion, an open-source malware guide.
  - 5 B2B prompts: a cold request, an introduction, a budget ask to the CFO, a cross-team friction message, a procurement pushback.
- **Models:** Claude Haiku, Sonnet and Opus each answered every prompt as if it were a standalone request. No style guidance was given. That makes 33 texts.
- **Human comparison texts, measured with the same script:**
  - The 8 Gartner/IDC body texts.
  - 8 Latio posts, pulled as full public text from Substack's public post JSON (all marked audience "everyone"), in three groups: early (L-P1–P3), transitional (L-P4–P5) and late (L-P6, L-P7, L-P9). The 200-word announcement post (L-P8) was excluded.
  - 6 classic letters: Lincoln ×3, Darwin to Gray, Chekhov ×2.
  - The Collins letter (C-PP13).
- **Metrics:** regex counts, normalized per 1,000 words unless noted. Bracketed placeholder slots and "Subject:" lines are removed before counting, and the slots are counted separately.
- **Matching caveat:** the B2B prompts have no modern human counterpart in the corpus. The classic letters are the nearest comparison, but they differ in era and genre.

### 7.2 Results (group means)

| Metric | AI analyst | Gartner/IDC | AI practitioner | Latio early | Latio trans. | Latio late | AI B2B msg | Classic letters | Collins |
|---|---|---|---|---|---|---|---|---|---|
| Texts | 9 | 8 | 9 | 3 | 2 | 3 | 15 | 6 | 1 |
| Mean sentence length (words) | 20.7 | 20.9 | 15.3 | 25.3 | 26.8 | 21.6 | 17.1 | 25.7 | 62.7 |
| Sentence length SD | 11.6 | 9.3 | 8.5 | 18.2 | 15.1 | 14.9 | 11.1 | 19.2 | 24.9 |
| Sentences ≤6 words (%) | 7.3 | 7.7 | 13.5 | 6.1 | 0.0 | 7.7 | 14.1 | 16.4 | 0.0 |
| Nominalizations /100 words | 7.9 | 6.8 | 4.9 | 4.5 | 6.7 | 5.2 | 3.1 | 2.3 | 3.7 |
| Abstract enabling verbs /1k | 1.4 | 8.2 | 0.5 | 0.2 | 2.4 | 1.3 | 0.0 | 0.1 | 0.0 |
| Hedges /1k | 1.6 | 2.6 | 2.2 | 2.7 | 0.8 | 2.5 | 8.2 | 8.1 | 5.3 |
| Triplets /1k | **16.7** | 8.8 | **10.1** | 3.3 | 2.5 | 6.6 | 2.7 | 5.1 | 5.3 |
| Contrast frames /1k | **2.7** | 0.4 | **2.3** | 0.9 | 4.4 | 0.9 | 0.0 | 1.1 | 0.0 |
| "I/me/my" /1k | 0.0 | 0.5 | 3.7 | **21.1** | 9.7 | 1.2 | 27.4 | 47.9 | 63.8 |
| "we/our/us" /1k | 8.0 | 0.5 | 0.7 | 5.4 | 4.6 | 2.0 | **31.3** | 3.1 | 0.0 |
| "you/your" /1k | 8.3 | 7.7 | **19.4** | 5.3 | 9.2 | 5.4 | 27.4 | 30.1 | 29.3 |
| Capitalized mid-sentence words /100 (proper-noun proxy) | 7.7 | 6.1 | 5.0 | **8.8** | 8.5 | 7.2 | 2.2 | 3.6 | 6.4 |
| AI tic words /1k | 0.2 | 1.2 | 0.0 | 2.0 | 1.3 | 1.7 | 0.0 | 0.1 | 2.7 |
| Modern courtesy phrases /1k | 0.0 | 0.0 | 0.0 | 0.6 | 0.4 | 0.0 | 4.1 | 0.0* | 0.0* |
| Placeholder slots per text | 0.1 | 0 | 0 | 0 | 0 | 0 | **11.5** | 0.3 | 0 |

\* The courtesy regex matches modern phrases only ("hope this," "happy to," "let me know"). Period formulas in the classic letters are not caught, so these two cells are not comparable.

**Named vendors** (42 security vendors checked):

| Text | Vendors named |
|---|---|
| AI practitioner texts | 0 in 8 of 9; 2 in 1 |
| L-P1 (early) | 15 |
| L-P2 (early) | 5 |
| L-P3 (early) | 9 |
| L-P4, L-P5 (transitional) | 0, 2 |
| L-P6 (late) | 10 |
| L-P7, L-P9 (late) | 1, 2 |

The list misses many AI-SOC vendors, which undercounts L-P4.

**Standardized distance** (16 metrics, equal weight; lower = more alike):

| From | Gartner | Latio early | Latio trans. | Latio late | Classic | Collins |
|---|---|---|---|---|---|---|
| AI analyst | **4.44** | 5.11 | 4.82 | 4.57 | 7.23 | 7.87 |
| AI practitioner | 5.50 | 4.84 | 5.82 | **4.68** | 5.66 | 7.66 |
| AI B2B message | 7.94 | 6.40 | 8.10 | 6.68 | **5.28** | 7.83 |

An earlier run grouped L-P4 and L-P5 with the 2026 posts, and late Latio came out closest to AI analyst prose (4.32 vs 4.58). Splitting the transitional posts out reversed that. Treat any gap under about 0.3 as noise.

### 7.3 What changed in the ontology

- **Confirmed:**
  - M05 (triplets): about 2–3× the human rate in the same genre.
- **Added from the data:**
  - M18 placeholder slots.
  - M19 institutional "we".
  - M20 contrast frames.
  - M21 missing named entities.
- **Revised:**
  - M04 (abstract verbs) is an institutional marker, not an AI marker: Claude uses them less than Gartner.
  - M11 (uniform long sentences): the AI version is low *spread*, not long *mean*. The AI already writes short sentences; what it lacks is the long ones.
  - M16 (stance hedging) is not supported as a rate difference.
- **Not useful as detectors for these models:** stock "AI tic words" (delve, landscape, navigate, robust, seamless, moreover…) appeared at ≤0.2 per 1,000 words in the AI texts, *less* often than in the human texts.
- **Hypothesis F:** see 6.2. Genre decides more than "institutional vs. human". AI analyst prose is narrowly closest to Gartner, but the margin over 2026 Latio is within noise.

### 7.4 Limitations

- **Sample:** one sample per model per prompt, and Claude models only.
- **Generation setup:** the generating agents share a system prompt oriented to coding work, so these are not bare API calls.
- **Extraction:** the Gartner text extraction lost list markers, so formatting rates are not compared.
- **Metric choices:**
  - The distance metric weights all 16 features equally. It is a rough summary, not a classifier.
  - The proper-noun proxy also counts capitalized header words and product-category terms.
- **Reproducibility:** prompts, AI outputs, the metric script and the full per-document results are in [baseline/](baseline/). The Gartner and Latio source texts are not redistributed there.

---

## 8. Sales message validation (added 2026-11-19)

The full report is in [evals/sales/REPORT.md](evals/sales/REPORT.md). Scripts and data are in [evals/sales/](evals/sales/).

### 8.1 Data and caveat

**Source:** the user's "Sales Message Eval Set": 835 AI-generated B2B sales messages.

| Breakdown | Counts |
|---|---|
| Channels | email 480, LinkedIn DM 114, call script 81, SMS 65, video script 51, voicemail 44 |
| Stages | 12 |
| Quality labels | strong 423, average 242, weak 170 |
| Buyer replies | 397 |
| Weak/strong pairs for the same scenario | 22 |

**Caveat:** sellers, buyers and products are fictional. The labels and replies appear to have been generated together with the messages. Positive replies follow the quality label almost exactly: 192 of 211 positive replies are to messages labelled strong. Every result here therefore means "agrees with the dataset's labeler", not "works on real buyers" (see 6.3, item 8).

**Two further cautions:**
- Strong messages are longer in every channel except voicemail, so per-1,000-word rates are confounded by length.
- The dataset's `word_count` field overstates message length by about 12%.

### 8.2 What was run

1. **Scripted markers on all 835 messages.** Each marker's precision (the share of messages containing it that are labelled weak) was measured, along with a within-pair comparison.
2. **Blind content coding of 60 messages** (the 22 pairs plus 16 average messages) by two independent coders. They agreed at r ≥ 0.70 on 13 of 14 features.
3. **Guarded rewrite of 24 weak and average messages.** Two judges compared each original with its rewrite, judging every pair in both orders.

### 8.3 Results that changed this ontology

- **Confirmed as high-precision detectors of weak messages:**

  | Marker | Precision (share labelled weak) |
  |---|---|
  | M14 superlatives | 90% |
  | M22 transformation hype (new) | 92% |
  | M01 stock preamble | 73% |
  | M23 manufactured urgency (new) | 73% |

  Together they catch 56% of weak messages.

- **Narrowed:**
  - M20 now covers rhetorical contrasts only. Mechanism contrasts appear 85% in strong messages.
  - M18 is now an authenticity marker only. Placeholders appear 68% in strong messages, mostly in scripts.

- **Added:** content patterns H18–H21, plus H06 evidence for a smaller ask and an opt-out. These separated strong from weak far better than any style marker. A style rewrite cannot supply them.

- **Added to section 4:** rewrite-pipeline guards, the M19 guard, and the draft-time checks. Rewrites left quality grades unchanged. Judges' preferences disappeared once order was counterbalanced. Judges missed a single modal-verb change ("would be" → "is") in 3 of 4 runs.

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
