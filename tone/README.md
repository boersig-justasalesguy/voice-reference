# Tone scorer: AI default → human target

This tool measures how far a message has moved away from how an AI writes by default, toward how people actually write or speak **in that situation**. It does not grade messages as good or bad.

```
AI default  0 ───────────────●──────── 1  human target
```

## Use

```bash
python3 -I tone/tone.py --list
```

```bash
python3 -I tone/tone.py --situation live_exec_answer my_message.txt
```

```bash
cat my_message.txt | python3 -I tone/tone.py --situation practitioner_post --json
```

**Output** for each feature:
- **value:** the feature's rate in the message, per 1,000 words.
- **AI mean and human mean:** the averages for that situation.
- **z_ai:** how many standard deviations the message is from the AI default.
- **position:** where it sits from 0 (AI default) to 1 (human target).

On top of that, an **overall position** with a verdict, plus warnings when a feature *overshoots* the human target. Going too far past it sounds forced too.

## Situations

| Situation | AI reference | Human target | Held-out AUC |
|---|---|---|---|
| `live_exec_answer` | 72 Claude answers to real analyst questions | 207 live executive answers, 12 earnings calls | 0.98 |
| `practitioner_post` | 9 AI texts in practitioner genres (chunked) | 3 early Latio posts (chunked) | 0.94 |
| `analyst_report` | 9 AI texts in analyst genres (chunked) | 8 Gartner/IDC pieces (chunked) | 0.89 |
| `one_to_one_message` | 15 AI business messages | 6 classic letters (**proxy**: 19th century) | 1.00 |
| `sales_outreach` | 1,711 AI sales messages | **none yet**, so it reports deviation from the AI default only | n/a |

**What the AUC measures.** Each situation was rebuilt 20 times from 70% of its documents, and the remaining 30% were scored. AUC is the chance that a held-out human text scores closer to human than a held-out AI text. Results are in `validation.json`.

## How it works

1. **Features** (`features.py`) are 19 measures already used elsewhere in this project: lists of three, numbers, discourse openers, stance markers, first-person stance, hedges, contractions, sentence-length spread and so on. The tool reuses the existing measurement code read-only and modifies none of it.
2. **References** (`build_refs.py` → `references/*.json`) store, for each situation:
   - the mean and spread of every feature for AI text and for human text;
   - the effect size *d* between the two;
   - which features are *discriminative*, meaning |d| ≥ 0.5.

   They contain statistics only, no source text.
3. **Scoring** (`tone.py`):

   | Output | Formula |
   |---|---|
   | z_ai | (value − AI mean) / AI SD |
   | position | (value − AI mean) / (human mean − AI mean) |
   | overall position | \|d\|-weighted mean of the positions on discriminative features |

## Limits

- **Only some situations have a real human target.** For `sales_outreach` (cold email, DMs) there is no human data, because both sales sets are AI-generated. Adding a few hundred real sent messages would create that target:

  ```bash
  python3 -I tone/build_refs.py --human-root <dir>
  ```

  after adding a situation entry for them.
- **`one_to_one_message` uses 19th-century letters as its human target.** It catches the AI fingerprint, but "human" there means *a letter from 1863*, not a modern email.
- **Small human samples.** Analyst and practitioner targets come from 8 and 3 documents. Earnings answers come from 12 public, media-trained calls with filler words removed by the transcript vendor.
- **Narrow AI reference.** The AI side is Claude models only, from a small set of prompts. The held-out AI texts share prompts with the training ones, so AUC may be optimistic.
- **Short messages are noisy.** Under about 60 words, per-1,000-word rates swing a lot, and the tool warns you.
- **This measures tone, not quality.** A message can be fully human in tone and still be a bad pitch. For the content side, use the sales eval content patterns (ontology H18–H21).
- **Rebuilding references needs the human corpora,** which are kept outside the repo for copyright reasons. The saved `references/*.json` files are enough to score messages without them.
