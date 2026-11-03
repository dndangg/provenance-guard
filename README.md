# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

A writing site sends us a piece of text and the id of the person who posted it.
We send back a guess, a score, and a sentence a reader can understand. In order:

1. **The request arrives** at `POST /submit` in `app.py` as JSON with `text`
   and `creator_id`.
2. **Validation** (`app.py::submit`) checks both fields. Missing, empty, or
   enormous text is refused with a 4xx and a "rejected" line in the audit log,
   so bad input never reaches a model.
3. **Signal one** (`detector.py::model_signal`) runs GPT-2 on this machine and
   returns 0–1 for how predictable the wording is. Higher means more AI-like.
4. **Signal two** (`stylometry.py::style_signal`) measures the shape of the
   text (sentence rhythm, vocabulary variety, punctuation) and returns 0–1 on
   the same scale, without reading for meaning.
5. **The combining rule** (`scoring.py::combine_signals`) turns the two numbers
   into one. If the two signals disagree sharply it leans toward the one that
   reads more human.
6. **The label** (`scoring.py::score_to_label`) maps the combined score to one
   of three plain-English sentences and a short guess (`human`, `unsure`, `ai`).
7. **The audit log** (`audit.py::log_decision`) records the decision with all
   three scores and a status of `decided`, then the route returns the JSON. If
   the writer disagrees, `POST /appeal` appends an `under_review` entry next to
   it.

### Endpoint contracts

**`POST /submit`**

| In (JSON) | Type | Rules |
|---|---|---|
| `text` | string | required, not blank, at most 100,000 characters |
| `creator_id` | string | required, not blank |

| Out (200) | Type | Meaning |
|---|---|---|
| `content_id` | string | UUID. The handle for appeals and `GET /content/<id>` |
| `guess` | string | `human`, `unsure` or `ai` |
| `confidence` | number 0–1 | the combined score (higher = more AI-like). It is a score, not a calibrated probability |
| `label` | string | the sentence a reader sees |
| `model_score`, `style_score` | number 0–1 | the two signals, shown separately |
| `combined_score` | number 0–1 | same value as `confidence` |

Errors are always `{"error": "<code>", "message": "<sentence>"}`:
`400 invalid_request` (missing/blank/not a string), `400 invalid_text` (too
short to score), `413 text_too_large`, `503 detector_unavailable`.

**`POST /appeal`**

| In (JSON) | Type | Rules |
|---|---|---|
| `content_id` | string | must exist in the log |
| `reasoning` | string | required, not blank |

| Out (200) | Meaning |
|---|---|
| `content_id`, `status: "under_review"`, `message` | the appeal was recorded |

`400 invalid_request` for a missing field; `404 not_found` for an unknown
`content_id` (nothing is written to the log in that case).

**Stretch feature I'm adding:** `GET /content/<id>` returns one item's current
status (`decided` or `under_review`), its label, and any appeal reasoning.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the wording is to GPT-2 running locally
(perplexity), squashed onto 0–1 so that more predictable = more AI-like.

**Why that might differ between human and AI writing:** A language model writes
by picking likely next words, so its output tends to be easy for another model
to predict. People reach for the odd word, the specific detail, the abrupt turn.

**What it can't see:** Authorship. It only sees predictability, and plenty of
real people write predictably: someone using a second language, a young writer,
anyone being plain on purpose. Those writers are the ones this signal is most
likely to wrongly accuse. It also can't tell a famous text it has memorized
from a generated one.

### Signal two — the style signal

**What it measures:** The shape of the text, three ways: how much sentence
length varies (burstiness), how varied the vocabulary is inside a sliding window
of words (MATTR), and how often expressive punctuation (`; : — – ( ) ! ?`) shows up.

**Why that might differ between human and AI writing:** Generated prose tends
to march in sentences of similar length, reuse a narrower set of words, and
stick to commas and full stops. People write in lumps: a short sentence after a
long one, a stray dash, a parenthesis.

**What it can't see:** Meaning, and where the text came from. It only sees
shape, so anything that changes the shape without changing the substance fools
it: breaking sentences up, adding typos, pasting in a quotation, dropping in a
few dashes. It also misjudges short texts (a single sentence has no rhythm to
measure) and writers who are naturally even and plain.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:**

Take a weighted average of the two scores, leaning a little harder on the model
signal. Then check whether the two signals agree. If they are more than 0.30
apart, the average is not allowed to leave the "unsure" band: a definite label,
either way, needs both signals to point the same direction. Two methods
disagreeing *is* uncertainty, and on a writing site the cost of a confident
wrong answer lands on the writer.

**The numbers:**

`WEIGHT_MODEL_SIGNAL = 0.6`, `WEIGHT_STYLE_SIGNAL = 0.4`, `DISAGREEMENT_GAP = 0.30`,
`HUMAN_THRESHOLD = 0.40`, `AI_THRESHOLD = 0.70`. The AI bar (0.70) sits further
from the middle than the human bar (0.40 is 0.10 from 0.5, 0.70 is 0.20) so it
takes more evidence to accuse someone than to clear them. The model signal gets
0.6 because it reads the actual words; the style signal gets 0.4 because its
measures are crude and easy to change on purpose. Settings live in `config.py`.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

The U.S. Constitution preamble (human-written, and a text GPT-2 has seen
many times) scores `model_score = 0.985` but `style_score = 0.648`, a gap of
0.34. A plain average with my weights would be 0.850, an `ai` verdict on a
text people wrote. Because the gap exceeds 0.30, the rule holds it inside the
unsure band: it returns **0.69**. The same rule rescues the opposite split: a
short ornate human paragraph scored 0.084 on the model and 0.523 on style (gap
0.44), and is held at 0.41 (`unsure`) rather than being cleared with confidence.

**Calibration run** (live `POST /submit`; "plain human" was written for this
test, the Twain and Darwin passages are public-domain human writing):

| Input | model_score | style_score | combined | guess |
|---|---:|---:|---:|---|
| clearly AI (generic productivity paragraph) | 0.853 | 0.865 | 0.858 | ai |
| clearly human (Twain) | 0.461 | 0.319 | 0.404 | unsure |
| formal human (Darwin) | 0.672 | 0.882 | 0.756 | **ai (false positive)** |
| plain human (short, simple sentences) | 0.891 | 0.927 | 0.905 | **ai (false positive)** |
| lightly-edited AI (contractions, a typo, a dash) | 0.588 | 0.673 | 0.622 | unsure |

What this tells me: the AI and Twain texts are 0.45 apart, which is real
separation. But **both signals agree on the formal and the plain human texts**,
so the disagreement rule cannot help there. Agreement between two signals that
share a blind spot (even, plain, regular prose) is not corroboration. That is
the false-positive risk my thresholds do not remove, and `/appeal` is the
safety net. Also: the vocabulary-variety measure did not separate these
inputs (AI and formal texts had *higher* variety than Twain), so I gave it
only 0.15 of the style score. Settings for all of this are in `config.py` and
`stylometry.py`.

---

### The false-positive trace (written before building)

A student writes a plain, careful paragraph in their second language and posts
it. Short sentences, common words. Signal one finds it very predictable and
scores it high. Signal two sees even sentences and few dashes and scores it
mid-to-high. Without protection the average lands above 0.65 and the writer is
told their own work is AI-generated, with no clue what to do about it. This is
why (a) the AI label needs a higher bar than the human label, (b) the combining
rule refuses to go high unless *both* signals lean AI, (c) every label says what
the writer can do next, and (d) `/appeal` exists and always works.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.40 | This looks like it was written by a person. There's nothing you need to do. |
| unsure | 0.41 – 0.69 | We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time. |
| high-confidence AI | 0.70 – 1.00 | Our checks suggest this may have been written with the help of AI. These checks make mistakes, especially with plain or simple writing. If you wrote it yourself, please tell us and a person will review it. |

Exact boundaries: a score at or below 0.40 is `human`, at or above 0.70 is `ai`,
everything between is `unsure` (`scoring.py::score_to_label`, thresholds in
`config.py`). Sweeping 0.00 to 1.00 in steps of 0.01 gives 41 `human`, 29
`unsure`, 31 `ai`, with no gap. 0.51 is `unsure` and 0.95 is `ai`: the label
moves with the score, not at a flip at 0.5.

**Unit 8 update:** the `ai` line moved from 0.70 to 0.90 as my one improvement (see The Improvement), so the live ranges are now human 0.00-0.40, unsure 0.41-0.89, ai 0.90-1.00. The table above is the unit 7 version, left as written.

**Each label reached by a real `POST /submit`:**

| guess | text | model | style | combined |
|---|---|---:|---:|---:|
| human | a casual, uneven personal paragraph ("Honestly? I didn't want to move…") | 0.246 | 0.039 | 0.163 |
| unsure | Twain, *Huckleberry Finn* opening | 0.461 | 0.319 | 0.404 |
| ai | a generic productivity paragraph | 0.853 | 0.865 | 0.858 |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->
The person reading it might be the writer, so the first thing it says is that
we can't tell, and the second is that we're not saying it wasn't them. It then
tells them the two things they most want to know: they don't have to do
anything, and a person is available if they want one. It never mentions a
score or a threshold, because "0.55" would sound like a verdict.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "Effective time management is essential for achieving both personal and professional success. By prioritizing tasks, setting clear goals, and minimizing distractions, individuals can significantly improve their productivity. Furthermore, it is important to take regular breaks in order to maintain focus and avoid burnout. Ultimately, adopting a structured approach to time management enables people to accomplish more while maintaining a healthy work-life balance.", "creator_id": "sample_writer"}'
```

```json
{
  "combined_score": 0.8577,
  "confidence": 0.8577,
  "content_id": "daf60139-0341-43d9-838e-6b9224b594f7",
  "guess": "ai",
  "label": "Our checks suggest this may have been written with the help of AI. These checks make mistakes, especially with plain or simple writing. If you wrote it yourself, please tell us and a person will review it.",
  "model_score": 0.853,
  "style_score": 0.8648
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "daf60139-0341-43d9-838e-6b9224b594f7", "reasoning": "I wrote this myself for a workplace newsletter. I write in short, plain sentences."}'
```

```json
{
  "content_id": "daf60139-0341-43d9-838e-6b9224b594f7",
  "message": "Thank you. Your appeal is recorded and a person will review it.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

The original decision is untouched (still `decided`); the appeal sits after it:

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.8577,
      "content_id": "daf60139-0341-43d9-838e-6b9224b594f7",
      "creator_id": "sample_writer",
      "guess": "ai",
      "label": "Our checks suggest this may have been written with the help of AI. These checks make mistakes, especially with plain or simple writing. If you wrote it yourself, please tell us and a person will review it.",
      "model_score": 0.853,
      "status": "decided",
      "style_score": 0.8648,
      "timestamp": "2026-10-30T06:26:27+00:00"
    },
    {
      "content_id": "daf60139-0341-43d9-838e-6b9224b594f7",
      "creator_id": "sample_writer",
      "event": "appeal",
      "reasoning": "I wrote this myself for a workplace newsletter. I write in short, plain sentences.",
      "status": "under_review",
      "timestamp": "2026-10-30T06:26:27+00:00"
    }
  ]
}
```

**Other checks I ran by hand:** an appeal for an unknown `content_id` returned
`404` and wrote nothing; `GET /content/<id>` for the appealed item returned
`"status": "under_review"` with the reasoning, and `"decided"` for an item
nobody had appealed; eight bad bodies (missing `text`, `null`, empty,
whitespace-only, a number, 50,001 repeats of `"x "` (over 100,000 characters),
missing `creator_id`, and text too short to score) returned `400, 400, 400,
400, 400, 413, 400, 400`, never a 5xx, each leaving a `rejected` line in the log.

---

## How I Used AI

**Moment 1: the style signal**

- *What I asked for:* the second signal in `stylometry.py`, measuring sentence-length spread, word variety and punctuation without reading for meaning.
- *What came back:* a working first version. When I ran it over my calibration texts, the vocabulary part scored 0.0 for nearly everything, because its anchors (0.60–0.85) sat below the real values (0.75–0.91) and clamped. It also showed the AI sample had *higher* word variety than the Twain sample, the opposite of what I'd assumed.
- *What I changed:* I stopped treating that as a bug to tune away. I widened the anchors, cut the vocabulary share of the style score to 0.15, and wrote the finding down in `stylometry.py` and above instead of fitting the numbers to my five samples.

**Moment 2: the combining rule**

- *What I asked for:* a rule that keeps a wrongly-accused writer from getting a confident `ai`, where the two signals disagree.
- *What came back:* the first idea was to pull the average halfway toward the lower signal. I checked it against the Constitution preamble (model 0.985, style 0.648) and it still landed at 0.749, above my AI threshold.
- *What I changed:* I replaced it with a hard rule in `scoring.py::combine_signals`: if the signals are more than 0.30 apart, the score is held inside the unsure band. I also kept the finding that this rule does nothing when both signals agree on a plain human text.

**Moment 3 (unit 8): choosing the improvement**

- *What I asked for:* help deciding which single change the diagnosis pointed at.
- *What came back:* instead of a recommendation, a table built from the before run only, counting how many accused pieces survive each candidate AI line (0.70 to 0.92). It showed plain human writing (0.83-0.90) and clear AI text (0.80-0.91) overlapping almost completely, so no line avoids a trade.
- *What I changed:* I picked 0.90 myself, as the first value above the highest plain-human score, and wrote down in The Improvement and What's Still Broken that this is fitted to the same texts it is measured on and nearly switches the `ai` label off.

**Moment 4 (unit 8): the test harness**

- *What I asked for:* scenarios for my five criteria, and a way to run the appeal criterion, which `run_eval.py` could not (it only sends `/submit`).
- *What came back:* a `run_eval.py` extended to appeal against real content ids and read `/log` back, to sweep `score_to_label`, and to count log entries per request. Its first "after" run showed a 429 on a criterion 5 body.
- *What I changed:* I traced that to the attack run having used up my address's per-minute allowance (a body with no `creator_id` is counted against the address), not to my route, kept that run as evidence, and re-ran after the window cleared.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 6 per minute, 60 per day (`config.py`: `RATE_LIMIT_PER_MINUTE`, `RATE_LIMIT_PER_DAY`), on `POST /submit` only.

**Why those numbers and not others:**
A real writer posting their own work might submit, read the label, tweak a
paragraph and resubmit: a handful of tries in a minute at the very most, and
maybe a dozen pieces in a day. 6 a minute leaves room for that and a retry or
two. 60 a day is five times a busy human day. A script mapping my thresholds
needs hundreds of probes, each one moving the text slightly; at 6 a minute it
takes about 17 minutes for 100 probes and the day cap stops it at 60 from one
identity, which is not enough to find a threshold to two decimals. I did not go
lower because a 429 on a writer is a bad experience too, and I did not go
higher because every extra request is another probe.

**What a caller counts as:** the `creator_id` in the request body, falling back
to the caller's address when the body has none (this is the starter's
`rate_limit_key` in `app.py`, which I left alone). So the limit is per creator, not per address. That
changes two things. One household or one office sharing a connection no longer
shares a limit. But one script can rotate `creator_id`s and never hit it: every
row in `attacks.csv` does exactly that (`attacker_<id>`), which is why none of
those rows ever got a 429. And a request with no usable `creator_id` falls into
a single shared address bucket: RQ11 in the attack run got a 429 for that
reason without ever reaching my route.

**The run of status codes when I pushed past it:**

```
python run_attacks.py --flood 15
200 200 200 200 200 200 429 429 429 429 429 429 429 429 429
```

6 accepted, 9 rejected. Each of the 9 left a `rejected` / `rate_limited` line
in `logs/audit.jsonl` (the 429 entry is the last of the ten entries below).

---

## Attack Run — Before

Run before anything was fixed: `python run_attacks.py --set attack_set --label before`
(report: `results/attack_run_2026-10-30_0043_before.md`). **56 attacks: 37 HELD, 19 BROKE.**
The runner only auto-marks crashes (it found none: no 5xx, no dropped connection),
so held/broke is my call. I settled one rule after the first run (once I had seen the scores and the attack texts) and before filling in any verdicts, then applied it unchanged to the after run, so before and after are comparable but the rule was not set blind:

- AI-text attacks (EV01-10, PI01-03, PI05) are **HELD only if the label is `ai`**. `unsure` means the AI text got through.
- Human-text attacks (FP01-08, PI04, PI06) are **HELD if the label is not `ai`**.
- MF01-02 and RQ01-12 are **HELD on a 4xx**; MF03-08 are **HELD unless a confident `ai`/`human` verdict comes back for non-text**; the flood rows are **HELD if 429 appears**.

| Family | Held | Broke |
|---|---|---|
| evasion | 2 | 8 |
| false_positive | 3 | 5 |
| prompt_injection | 2 | 4 |
| malformed | 18 | 2 |
| flood_same_creator | 12 | 0 |
| **total** | **37** | **19** |

| ID | Family | What it targets | Status | Guess | Combined | Verdict |
|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | unsure | 0.438 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | unsure | 0.410 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | unsure | 0.574 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | ai | 0.707 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | human | 0.317 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | unsure | 0.492 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | unsure | 0.465 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | unsure | 0.474 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure | 0.675 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | ai | 0.919 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | unsure | 0.646 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | ai | 0.806 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | ai | 0.807 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | ai | 0.808 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | ai | 0.854 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | ai | 0.786 | BROKE |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | unsure | 0.690 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | unsure | 0.460 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | unsure | 0.456 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | human | 0.198 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | unsure | 0.520 | BROKE |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | unsure | 0.455 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | unsure | 0.495 | BROKE |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.615 | HELD |
| MF01 | malformed | text is only whitespace | 400 | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | unsure | 0.410 | HELD |
| MF04 | malformed | text is only punctuation | 200 | unsure | 0.410 | HELD |
| MF05 | malformed | text is a very long single word | 200 | unsure | 0.690 | HELD |
| MF06 | malformed | text is emoji only | 200 | unsure | 0.690 | HELD |
| MF07 | malformed | text is right-to-left script | 200 | ai | 0.814 | BROKE |
| MF08 | malformed | text is 60,000 characters | 200 | ai | 0.883 | BROKE |
| RQ01 | malformed | no text field at all | 400 | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | — | — | HELD |
| RQ05 | malformed | text is null | 400 | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.410 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.410 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.410 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.410 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.410 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.410 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |

Two notes on reading that table. First, my rule is strict: of the 8 broken
evasions only EV05 came back `human`; the other seven came back `unsure`, i.e.
undetected but not cleared. Second, RQ11 shows `429`: it was counted against my own
address and never reached the route, so it tells me nothing about how my route handles
that input.

**Ten audit log entries from the run**

Chosen for what they show: three plain/formal human texts accused (FP03, FP05,
FP06); AI text with an injected prefix cleared as human (PI02); two evasions
that split the signals (EV01, EV02); two non-text inputs given a verdict (MF07,
MF08); and two rejections (a 429 and a 400). A rejection carries fewer fields than a decision.

```json
[
 {
  "combined_score": 0.8069,
  "content_id": "52d9ca30-6af6-40a9-854f-586a57b74941",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "label": "Our checks suggest this may have been written with the help of AI. These checks make mistakes, especially with plain or simple writing. If you wrote it yourself, please tell us and a person will review it.",
  "model_score": 0.8051,
  "status": "decided",
  "style_score": 0.8095,
  "timestamp": "2026-10-30T06:43:19+00:00"
 },
 {
  "combined_score": 0.8535,
  "content_id": "e0c0e431-5dba-4d14-a436-59ce6acf77fa",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "label": "Our checks suggest this may have been written with the help of AI. These checks make mistakes, especially with plain or simple writing. If you wrote it yourself, please tell us and a person will review it.",
  "model_score": 0.8005,
  "status": "decided",
  "style_score": 0.9329,
  "timestamp": "2026-10-30T06:43:19+00:00"
 },
 {
  "combined_score": 0.7858,
  "content_id": "352bdd49-2840-4040-8332-99d9684a1b2e",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "label": "Our checks suggest this may have been written with the help of AI. These checks make mistakes, especially with plain or simple writing. If you wrote it yourself, please tell us and a person will review it.",
  "model_score": 0.8814,
  "status": "decided",
  "style_score": 0.6423,
  "timestamp": "2026-10-30T06:43:19+00:00"
 },
 {
  "combined_score": 0.1982,
  "content_id": "e4c24fb8-9d5f-418b-acf6-addba52eafe0",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "label": "This looks like it was written by a person. There's nothing you need to do.",
  "model_score": 0.2044,
  "status": "decided",
  "style_score": 0.1889,
  "timestamp": "2026-10-30T06:43:19+00:00"
 },
 {
  "combined_score": 0.4381,
  "content_id": "a1fa278e-d2f2-4c16-bb93-e93fa440ceb2",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "model_score": 0.1635,
  "status": "decided",
  "style_score": 0.85,
  "timestamp": "2026-10-30T06:43:18+00:00"
 },
 {
  "combined_score": 0.41,
  "content_id": "31abc9e7-6630-4df4-aa41-77be636729d9",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "model_score": 0.5943,
  "status": "decided",
  "style_score": 0.0144,
  "timestamp": "2026-10-30T06:43:18+00:00"
 },
 {
  "combined_score": 0.8138,
  "content_id": "0092f167-2d75-47de-9ce6-3a55678c31e1",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "label": "Our checks suggest this may have been written with the help of AI. These checks make mistakes, especially with plain or simple writing. If you wrote it yourself, please tell us and a person will review it.",
  "model_score": 0.9064,
  "status": "decided",
  "style_score": 0.675,
  "timestamp": "2026-10-30T06:43:20+00:00"
 },
 {
  "combined_score": 0.8827,
  "content_id": "d46d0452-1ff4-470d-a9e2-a7855def2dd9",
  "creator_id": "attacker_MF08",
  "guess": "ai",
  "label": "Our checks suggest this may have been written with the help of AI. These checks make mistakes, especially with plain or simple writing. If you wrote it yourself, please tell us and a person will review it.",
  "model_score": 0.9876,
  "status": "decided",
  "style_score": 0.7253,
  "timestamp": "2026-10-30T06:43:20+00:00"
 },
 {
  "creator_id": "unknown",
  "event": "rejected",
  "limit": "6 per 1 minute",
  "reason": "rate_limited",
  "status": "rejected",
  "timestamp": "2026-10-30T06:43:20+00:00"
 },
 {
  "creator_id": "attacker_RQ12",
  "event": "rejected",
  "message": "'text' must be a non-empty string.",
  "reason": "invalid_request",
  "status": "rejected",
  "timestamp": "2026-10-30T06:43:20+00:00"
 }
]
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:
FP03, a non-native English speaker writing carefully about their first month in a new
country, came back `ai` (combined 0.807; model 0.805, style 0.809). The label they
would have read: "Our checks suggest this may have been written with the help of AI. These
checks make mistakes, especially with plain or simple writing. If you wrote it yourself,
please tell us and a person will review it." That is a person who wrote every word, in a
second language, being told it looks machine-made, because they used common words in short
sentences. The label tells them what to do, but it is still an accusation, and it fell on
exactly the writer least able to argue.

---

## Run Log and Verdicts

`python run_eval.py --label before`, three trials, nothing changed in between
(`results/run_2026-10-30_0045_before.md` / `.json`). `scenarios.py` holds the
inputs. I extended `run_eval.py` (the starter only sends `/submit`) to also appeal
against real content ids and read `/log` back (criterion 4), sweep `score_to_label`
over 0.00-1.00 (criterion 3), and count how many log entries each request added
(criterion 5). The verdict numbers below are computed from the saved JSON, not eyeballed.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Plain human writing is almost never called AI | ≤ 1 of 10 human pieces `ai`, none of the 4 plain ones | 5/10 `ai` (4/4 plain) | 5/10 `ai` (4/4 plain) | 5/10 `ai` (4/4 plain) | **MISSED** |
| 2. Clearly-AI text scores well above clearly-human | mean gap ≥ 0.15 | 0.298 | 0.298 | 0.298 | **MET** |
| 3. Every label reachable; 0.51 ≠ 0.95 | sweep gives 3 guesses, 12+ real submissions cover all 3 | 3/3, 3/3 | 3/3, 3/3 | 3/3, 3/3 | **MET** |
| 4. An appeal always changes status and is recorded | 5 of 5, unknown id → 404, no log write | 5/5, 404 | 5/5, 404 | 5/5, 404 | **MET** |
| 5. Bad input never 5xx and never silent | 7 of 7 are 4xx with a `rejected` log line | 7/7 | 7/7 | 7/7 | **MET** |

All three trials were identical for every criterion, as expected: neither signal is random.

**Real output from one trial (trial 1), and which code produced it.**

*Criterion 1* — `app.py::submit` via `run_eval.py`; the four plain pieces and the Dickens passage (the 5 `ai` results):

```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6542,
    "model_score": 0.6379,
    "style_score": 0.6787,
    "content_id": "40c04dc6-6562-4501-af46-c93e0f5867a1",
    "log_entries_added": 1,
    "sent": "I went to the woods because I wished to live deliberately, to front on"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.637,
    "model_score": 0.6331,
    "style_score": 0.6429,
    "content_id": "d55b1260-4c10-4c94-8367-c092985a21ad",
    "log_entries_added": 1,
    "sent": "When we look to the individuals of the same variety or sub-variety of "
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8968,
    "model_score": 0.8755,
    "style_score": 0.9287,
    "content_id": "492ee70d-f7f9-48c4-95cf-b99c54dba047",
    "log_entries_added": 1,
    "sent": "I live in a small town. My school is near my house. Every day I walk t"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8818,
    "model_score": 0.8752,
    "style_score": 0.8916,
    "content_id": "15c88063-bb6c-453e-89ca-8a1e6a88fad7",
    "log_entries_added": 1,
    "sent": "We got a dog last year. His name is Max. He is brown and white. He lik"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8345,
    "model_score": 0.7695,
    "style_score": 0.932,
    "content_id": "bb19d04c-3a60-41c5-b188-929d9abca2eb",
    "log_entries_added": 1,
    "sent": "I work at a shop. The shop sells shoes. I start at nine in the morning"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8339,
    "model_score": 0.7763,
    "style_score": 0.9203,
    "content_id": "adf09b9a-a124-4ac4-9c19-ff5b8a8999e3",
    "log_entries_added": 1,
    "sent": "Last summer we went to the sea. The drive was long. My brother was sic"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8768,
    "model_score": 0.9613,
    "style_score": 0.75,
    "content_id": "29afb758-60e6-4e03-8d8a-b2272f1a470c",
    "log_entries_added": 1,
    "sent": "It was the best of times, it was the worst of times, it was the age of"
  }
]
```

*Criterion 2* — `scoring.py::combine_signals` (the `confidence` field). AI mean 0.853, human mean 0.555, gap 0.298:

```json
{
  "AI group confidences": [
    0.8577,
    0.9106,
    0.8746,
    0.8018,
    0.8221
  ],
  "human group confidences": [
    0.4041,
    0.1629,
    0.6783,
    0.8768,
    0.6542
  ]
}
```

*Criterion 3* — `scoring.py::score_to_label` (sweep), and `app.py::submit` (the 15 real submissions):

```json
{
  "sweep": {
    "sweep": {
      "human": {
        "first": 0.0,
        "last": 0.4,
        "count": 41
      },
      "unsure": {
        "first": 0.41,
        "last": 0.69,
        "count": 29
      },
      "ai": {
        "first": 0.7,
        "last": 1.0,
        "count": 31
      }
    },
    "guess_at_0.51": "unsure",
    "guess_at_0.95": "ai",
    "sent": "score_to_label sweep 0.00 to 1.00"
  },
  "guesses over 15 real submissions": [
    "ai",
    "human",
    "unsure"
  ]
}
```

*Criterion 4* — `app.py::appeal` and `audit.py::log_appeal`; one real appeal read back from `/log`, and the unknown-id appeal:

```json
[
  {
    "status": 200,
    "log_entries_added": 1,
    "content_id": "7c21628f-2793-4438-8a6c-399aaa8fce4e",
    "guess": "unsure",
    "confidence": 0.4041,
    "model_score": 0.4611,
    "style_score": 0.3186,
    "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
    "sent": "You don't know about me without you have read a book by the name of Th",
    "appeal_status": 200,
    "appeal_reply_status": "under_review",
    "decision_entries": 1,
    "decision_still_decided": true,
    "appeal_entries": 1,
    "appeal_entry_status": "under_review",
    "appeal_has_reasoning": true
  },
  {
    "sent": "appeal against unknown content_id",
    "appeal_status": 404,
    "log_entries_added": 0
  }
]
```

*Criterion 5* — `app.py::submit` / `_reject`; the seven bad bodies:

```json
[
  {
    "status": 400,
    "log_entries_added": 1,
    "sent": "{\"creator_id\": \"eval_bad_missing\"}"
  },
  {
    "status": 400,
    "log_entries_added": 1,
    "sent": "{\"text\": null, \"creator_id\": \"eval_bad_null\"}"
  },
  {
    "status": 400,
    "log_entries_added": 1,
    "sent": "(empty text)"
  },
  {
    "status": 400,
    "log_entries_added": 1,
    "sent": "   \n\t  "
  },
  {
    "status": 400,
    "log_entries_added": 1,
    "sent": "{\"text\": 5, \"creator_id\": \"eval_bad_number\"}"
  },
  {
    "status": 413,
    "log_entries_added": 1,
    "sent": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  },
  {
    "status": 400,
    "log_entries_added": 1,
    "sent": "{\"text\": \"A perfectly good sentence with no creator attached.\"}"
  }
]
```

**How I decided each verdict.**
1 is MISSED: the target was at most 1 and every trial produced 5, and the "none of the plain ones" clause failed too. 2 is MET: 0.298 against a 0.15 target in every trial, with the caveat below. 3 is MET: the sweep gives exactly `human`, `unsure`, `ai`, 0.51 and 0.95 differ, and 15 real submissions produced all three. 4 is MET: 5 of 5, the original entry stayed `decided`, and the unknown id wrote nothing. 5 is MET: all 7 returned 4xx (six 400s, one 413) and each added exactly one log line. 2 and 3 are weaker passes than they look: see the diagnoses.

**Diagnoses**

*Criterion 1 (MISSED), and the false_positive family (5 of 8 broke: FP02-FP06).*
The stage is **signal one and signal two together, with the combining rule unable to help**. Every one of
these inputs is plain or formal prose: short or evenly sized sentences, common words, almost no semicolons or dashes.
Signal one (GPT-2 perplexity) finds that vocabulary very predictable, so it scores the plain pieces 0.77-0.88 and the
formal ones 0.74-0.88. Signal two sees the same pieces as shape: low sentence-length spread (burstiness part scores 1.0) and zero
expressive punctuation (punctuation part scores 1.0), so it gives 0.64-0.93. Both lean hard towards AI **and they agree**, so my
disagreement guard (`DISAGREEMENT_GAP`) never fires, and a weighted average of two high numbers is a high number: 0.79-0.90
against an AI line of 0.70. The mechanism is that "predictable, even, plain" is a property of *plain writing*, and both signals read it as "machine".
The Dickens passage is the same story by a different route: its repeated "it was the ... it was the ..." clauses made it extremely predictable (model 0.961).
This is the blind spot I wrote down in Milestone 1 of the last unit, now confirmed as the dominant failure.

*Criterion 2 (MET), the weakness behind it.* The gap of 0.298 is real, but it is an average across groups
whose ranges overlap completely at the top: the plain human pieces score 0.83-0.90 and the AI pieces 0.80-0.91. The
mean passes because the human group also contains pieces the signals handle well (the casual one, Twain). It would be a mistake to read it as "AI text scores above human text". It reads "AI text scores above *expressive* human text."

*Evasion family (8 of 10 broke).* Two mechanisms, split by which stage did the damage:
- **One signal fooled, and the combining rule lets it drag the average down.** EV01 (typos) pushed the model score to 0.164, because misspellings are unexpected tokens and raise perplexity, while the style score stayed 0.85. EV08 (very short text) is the mirror image: model 0.245 on almost no text, style 0.817. EV02 (sentences broken up with "Really.") sent the style score to 0.014 (a run of very short sentences is maximum burstiness) against a model score of 0.594. The weighted average of a fooled signal and an honest one lands around 0.36-0.47, which is `unsure` (for EV02 the disagreement guard lifted 0.362 up to 0.41, so it stopped it being cleared as `human`, but it could not make it `ai`). The stage is the combining rule plus whichever signal was fooled: because the AI line needs both signals high, fooling either one is enough.
- **Signal two, on its own measures**, with both signals moderate. EV07 (padding with `; and, moreover,`) works directly on the punctuation measure, since semicolons and dashes are exactly what it counts as human (style 0.282). EV06 (one very long sentence and a very short one) works on the burstiness measure (style 0.372). EV03 (a pasted quotation) and EV09 (a human opening paragraph) dilute both signals (0.666/0.436 and 0.704/0.632).
- EV04 (rare words) actually **held** before: combined 0.707 against a 0.70 line, by 0.007. It was lost when I moved the line.
- EV05 (a heavy human editing pass) came back `human` (0.317) from both signals, which is arguably correct: it may no longer be AI text in any sense that matters.
The pattern: **signal two is the cheap lever.** Four of the eight work by changing sentence shape or punctuation, which costs the attacker nothing.

*Prompt injection (4 of 6 broke).* Nothing here is the injection working as an *instruction*. Neither signal reads instructions: signal one is a perplexity score and signal two is arithmetic over characters, so
"Ignore all previous instructions" has nothing to obey it. The label text is a fixed string, so PI04's `</label><script>` could not change it, and PI05's fake JSON could not corrupt the log (I read its entry back: it is a normal decision entry with `combined_score` 0.4955, not the 0.01 the injected text claimed; all 595 log lines parse). The four that "broke" are AI text that wasn't labelled `ai`
because the added junk changed the *scores*. PI02 is the worst: the all-caps "SYSTEM: ..." prefix with colons and an equals sign pushed signal one to 0.204 and signal two to 0.189, and the AI body came back `human`. The stage is
signals one and two again, and the mechanism is the same as the evasions: padding.

*Malformed (2 of 20 broke: MF07, MF08).* MF07 is Arabic text. `stylometry.words()` only matches `[a-z0-9']`, so signal two sees zero words and quietly returns its default shape (every part at neutral or AI-leaning, 0.675). Signal one gives 0.906 (I did not investigate why GPT-2 finds this Arabic sentence predictable). Combined 0.814, `ai`.
The stage is **the route** (it accepts text with no words in a script it cannot measure) and **signal two** (no words becomes an AI-leaning default instead of "can't tell"). This is a false accusation of any non-Latin-script writer, and the worst structural bug the set found.
MF08 is about 58,000 characters (the 116-token campsite paragraph repeated 110 times): signal one reads only the first 400 tokens, which already contain the paragraph about three and a half times, so it is extremely predictable (0.988), and the style signal sees near-zero sentence variation. Stage: signal one (repetition is predictable) and the route (58,000 characters is under my 100,000 cap).

*Flood and the other malformed requests.* All 12 flood rows and all 12 RQ rows held. The limiter fired after 6, and every 4xx left a log entry. The one caveat is RQ11 (429 before it reached the route).

---

## The Improvement

**What I changed:** one value: `AI_THRESHOLD` in `config.py`, **0.70 → 0.90**. Nothing else moved. (Because the combining rule clamps disagreeing signals into the unsure band using the thresholds, that clamp's ceiling moved with it, from 0.69 to 0.89; it only affects scores that were already `unsure`, so no label changed because of it.)

**Which diagnosis pointed at it:** the criterion 1 / false-positive diagnosis. Both signals agree that plain human writing looks like AI, so no reweighting can fix it and the guard cannot help; the only lever left is how much evidence the system asks for before it says "AI". Before moving anything I tabulated, from the before run alone, how many of each group sat above each candidate line:

| AI line | FP family `ai` (of 8) | 10 human pieces `ai` | 4 plain pieces `ai` | 5 clear-AI pieces `ai` | Evasions `ai` (of 10) |
|---|---|---|---|---|---|
| 0.70 | 5 | 5 | 4 | 5 | 2 |
| 0.75 | 5 | 5 | 4 | 5 | 1 |
| 0.80 | 4 | 5 | 4 | 5 | 1 |
| 0.85 | 1 | 3 | 2 | 3 | 1 |
| 0.90 | 0 | 0 | 0 | 1 | 1 |
| 0.92 | 0 | 0 | 0 | 0 | 0 |

The ranges overlap, so every line is a trade. I chose 0.90 because it is the first value above the highest score any plain human piece got (0.897), and criterion 1 says no plain piece may be called AI. This is a choice made by looking at the same texts it is then measured on, which flatters the result; see below.

### Attack Run — After

`python run_attacks.py --set attack_set --label after` (`results/attack_run_2026-10-30_0047_after.md`). **56 attacks: 43 HELD, 13 BROKE** (was 37 / 19).

| Family | Held before | Held after | Broke before | Broke after |
|---|---|---|---|---|
| evasion | 2 | 1 | 8 | 9 |
| false_positive | 3 | 8 | 5 | 0 |
| prompt_injection | 2 | 2 | 4 | 4 |
| malformed | 18 | 20 | 2 | 0 |
| flood_same_creator | 12 | 12 | 0 | 0 |
| **total** | **37** | **43** | **19** | **13** |

Side by side, every attack:

| ID | Family | What it targets | Before | Verdict | After | Verdict |
|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | unsure 0.438 | BROKE | unsure 0.438 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | unsure 0.410 | BROKE | unsure 0.410 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | unsure 0.574 | BROKE | unsure 0.574 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | ai 0.707 | HELD | unsure 0.707 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | human 0.317 | BROKE | human 0.317 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | unsure 0.492 | BROKE | unsure 0.492 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | unsure 0.465 | BROKE | unsure 0.465 | BROKE |
| EV08 | evasion | signal one: text below the token window | unsure 0.474 | BROKE | unsure 0.474 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | unsure 0.675 | BROKE | unsure 0.675 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | ai 0.919 | HELD | ai 0.919 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | unsure 0.646 | HELD | unsure 0.646 | HELD |
| FP02 | false_positive | human writing in a formal register | ai 0.806 | BROKE | unsure 0.806 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | ai 0.807 | BROKE | unsure 0.807 | HELD |
| FP04 | false_positive | a student essay written to a rubric | ai 0.808 | BROKE | unsure 0.808 | HELD |
| FP05 | false_positive | technical documentation written by a person | ai 0.854 | BROKE | unsure 0.854 | HELD |
| FP06 | false_positive | a person imitating a formal template | ai 0.786 | BROKE | unsure 0.786 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | unsure 0.690 | HELD | unsure 0.726 | HELD |
| FP08 | false_positive | very short genuine human submission | unsure 0.460 | HELD | unsure 0.460 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | unsure 0.456 | BROKE | unsure 0.456 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | human 0.198 | BROKE | human 0.198 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | unsure 0.520 | BROKE | unsure 0.520 | BROKE |
| PI04 | prompt_injection | attempt to make the label text hostile | unsure 0.455 | HELD | unsure 0.455 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | unsure 0.495 | BROKE | unsure 0.495 | BROKE |
| PI06 | prompt_injection | instruction plus real human text | unsure 0.615 | HELD | unsure 0.615 | HELD |
| MF01 | malformed | text is only whitespace | 400 | HELD | 400 | HELD |
| MF02 | malformed | text is a single character | 400 | HELD | 400 | HELD |
| MF03 | malformed | text is control characters | unsure 0.410 | HELD | unsure 0.410 | HELD |
| MF04 | malformed | text is only punctuation | unsure 0.410 | HELD | unsure 0.410 | HELD |
| MF05 | malformed | text is a very long single word | unsure 0.690 | HELD | unsure 0.839 | HELD |
| MF06 | malformed | text is emoji only | unsure 0.690 | HELD | unsure 0.868 | HELD |
| MF07 | malformed | text is right-to-left script | ai 0.814 | BROKE | unsure 0.814 | HELD |
| MF08 | malformed | text is 60,000 characters | ai 0.883 | BROKE | unsure 0.883 | HELD |
| RQ01 | malformed | no text field at all | 400 | HELD | 400 | HELD |
| RQ02 | malformed | no creator_id | 400 | HELD | 400 | HELD |
| RQ03 | malformed | text is a number | 400 | HELD | 400 | HELD |
| RQ04 | malformed | text is a list | 400 | HELD | 400 | HELD |
| RQ05 | malformed | text is null | 400 | HELD | 400 | HELD |
| RQ06 | malformed | creator_id is an object | 400 | HELD | 400 | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | HELD | 400 | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | HELD | 400 | HELD |
| RQ09 | malformed | body is empty | 400 | HELD | 400 | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | HELD | 400 | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | HELD | 429 | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | HELD | 400 | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | unsure 0.410 | HELD | unsure 0.410 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | unsure 0.410 | HELD | unsure 0.410 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | unsure 0.410 | HELD | unsure 0.410 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | unsure 0.410 | HELD | unsure 0.410 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | unsure 0.410 | HELD | unsure 0.410 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | unsure 0.410 | HELD | unsure 0.410 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | HELD | 429 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | HELD | 429 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | HELD | 429 | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | HELD | 429 | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | HELD | 429 | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | HELD | 429 | HELD |

**Criteria after** (`python run_eval.py --label after2`; `results/run_2026-10-30_0049_after2.md` / `.json`; same inputs, three trials, all identical):

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict before | Verdict after |
|---|---|---|---|---|---|---|
| 1. Plain human writing almost never called AI | ≤ 1 of 10, none of the plain | 0/10 (0/4 plain) | 0/10 (0/4 plain) | 0/10 (0/4 plain) | MISSED | **MET** |
| 2. AI scores well above human | mean gap ≥ 0.15 | 0.298 | 0.298 | 0.298 | MET | **MET** |
| 3. Every label reachable | 3 guesses, 12+ submissions | 3/3, 3/3 | 3/3, 3/3 | 3/3, 3/3 | MET | **MET** |
| 4. Appeal changes status, recorded | 5 of 5 | 5/5 | 5/5 | 5/5 | MET | **MET** |
| 5. Bad input never 5xx, never silent | 7 of 7 | 7/7 | 7/7 | 7/7 | MET | **MET** |

(A first "after" run, `results/run_2026-10-30_0048_after.md`, returned 429 instead of 400 for the last bad body in criterion 5: the attack run just before it had used up my address's per-minute allowance, and a body with no `creator_id` counts against the address. It still counted as 4xx and logged, and I re-ran after waiting out the window to get a clean `after2`.)

**Did it help, and how do I know:** It fixed what I aimed at: 5 false accusations on the attack set became 0 (FP02-FP06 went from `ai` to `unsure`), and criterion 1 went from 5/10 to 0/10. **But it did that by almost switching the `ai` label off.** Of 5 clearly-AI pieces, 4 stopped being labelled `ai` (only the 0.9106 one still is);
of 10 evasions, one is still caught (EV10, a pasted-twice paragraph at 0.919) and EV04 was lost. The trade is the one the unit warned about: **fewer wrong accusations, more AI text getting through, and in this case a lot more.** Two other things changed that are not improvements.
MF07 (Arabic) and MF08 (the 60,000-character repeat) now count as HELD, but only because their combined scores (0.814, 0.883) sit under the new line; the underlying bugs are unchanged, and a slightly different input would trip them again. And criterion 2 is unchanged because it measures the score, not the label, so it did not notice the trade at all.

---

## What's Still Broken

- **Plain and formal human writing is still scored as AI-like; it is just no longer labelled so.** FP02-06 sit at 0.79-0.85, one step under the new line. The fix is upstream of any threshold: a signal that does not read short, common-word sentences as machine. I stopped because moving a second thing would have broken the before/after comparison, and because I do not have a signal that separates them: the two I have share this blind spot.
- **The AI label is now close to unreachable** (4 of 5 clearly-AI pieces and 9 of 10 evasions are not labelled `ai`). I'd fix this with a third signal that does not share the plain-writing blind spot, so that agreement of three can justify a lower line. I stopped because that is a new feature, not one change.
- **Non-Latin text (MF07).** I'd reject or label as "can't assess" any text where `stylometry.words()` finds fewer than a few words. It is a route/validation fix, and the right place for it is before either signal runs. I stopped because it was not my one change.
- **Repetition (MF08, EV10).** Signal one reads only 400 tokens and repetition is exactly what it finds predictable. I'd de-duplicate or cap repeated spans before scoring.
- **Signal two is cheap to move** (EV02, EV03, EV06, EV07, EV09): sentence-shape and punctuation padding. I'd cap how much any one style measure can move the score, or replace punctuation counts with something harder to pad.
- **Per-creator limits are easy to walk around.** Rotating `creator_id` evades them (every attack row does). A real deployment needs an address limit as well.
- **The 0.90 line is fitted to the evidence it was measured on.** I chose it by looking at the same plain-human texts the criteria use, so criterion 1's 0/10 is not a clean generalisation test. The plain pieces were also written for the test, not by a real writer; I have not run the criteria on anyone's actual writing.
- **Criterion 2 does not see label changes.** It stayed MET while the AI label nearly vanished. I'd add a criterion about how many clearly-AI pieces are labelled `ai`.

**The trade I'd make if this ran for real:**
I'd keep the line high. A wrongly accused writer loses trust, time and perhaps standing, and the site loses a good contributor, while a missed AI paragraph costs the site very little. The people who pay for my choice are the readers and the other writers: more AI text gets through unlabelled, and "unsure" becomes where most real AI text lands.

---

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
