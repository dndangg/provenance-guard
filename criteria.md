# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. Plain human writing is almost never called AI

Of 10 pieces of human writing I submit, at least 4 of them deliberately plain
(short sentences, common words), at most 1 gets the guess `ai`, and none of
the plain ones do.

**Why this target:**

Wrongly accusing a writer costs that person far more than a missed AI text
costs the site, so I allow one error in ten at most. I carve the plain pieces
out separately because plain writing is exactly what a predictability model
punishes, and I don't want the allowed error to be spent entirely on them.

---

## 2. Clearly-AI text scores well above clearly-human text

Across 5 clearly AI-generated samples and 5 clearly human-written samples, the
mean `combined_score` of the AI group is at least 0.15 higher than the mean of
the human group, in every trial.

**Why this target:**

Perfect separation is impossible, so I'm not asking for it. 0.15 is about the
width of my "unsure" band's lower half: a smaller gap would mean the scores
carry no more information than noise. I use the mean, not each sample,
because one odd sample shouldn't decide whether the signals work.

---

## 3. Every label is reachable, and 0.51 is not 0.95

Sweeping `combined_score` from 0.00 to 1.00 in steps of 0.01 produces exactly
three distinct guesses (`human`, `unsure`, `ai`) with no gap and no value that
returns anything else, and 0.51 and 0.95 produce different guesses. Separately,
12 real submissions of varied text produce at least one of each guess.

**Why this target:**

A label that can never appear is a promise the system can't keep. The sweep
proves the ranges have no holes; the real submissions prove the signals can
actually move far enough to land in each band, which the sweep alone can't.

---

## 4. An appeal always changes status and is always recorded

For 5 appeals against 5 real `content_id`s: all 5 return `200` with
`status: "under_review"`; `GET /log` shows 5 new appeal entries with the
reasoning text; the 5 original decision entries are unchanged. An appeal
against an unknown `content_id` returns `404` and writes nothing to the log.

**Why this target:**

The appeal is the only recourse a wrongly accused writer has, so the target is
all-or-nothing: 5 of 5, not "most". Keeping the original entry untouched means
a reviewer can see what the system said before the writer pushed back.

---

## 5. Bad input never crashes the service and never vanishes

Each of these 7 request bodies returns a `4xx` and never a `5xx`, and each
leaves a `rejected` entry in `logs/audit.jsonl`: `text` missing; `text` null;
`text` an empty string; `text` only whitespace; `text` a number; `text` of
100,001 characters (expecting `413`); and `creator_id` missing.

**Why this target:**

A crash on malformed input is one of the most common real failures, and an
oversized or blank request that quietly disappears looks like a quiet
afternoon. 7 of 7 because each one is a deterministic check with no model
noise: there's no excuse for a partial score.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
