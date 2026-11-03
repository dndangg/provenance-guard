# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-10-30 00:47
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `f4bbc85b-75ac-4638-b812-4fb49d426c21` | unsure | 0.438 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `501ad3b2-43da-4825-83b4-30c3819afb9d` | unsure | 0.410 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `5d3cd65b-9069-44a4-81eb-6ec82ff108fd` | unsure | 0.574 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `9e5f26b5-8d3b-402e-8907-b07a8132462e` | unsure | 0.707 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `b1d9eefb-c303-4172-80a9-ef03d3a8a3cd` | human | 0.317 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `240ac685-334f-4926-b530-1ef2becf8a6d` | unsure | 0.492 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `0c32661c-a17e-4722-9f83-82f7f47a47fb` | unsure | 0.465 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `e5912bae-a52b-4520-8ddd-2b9eb84b2d80` | unsure | 0.474 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `29e5c7c4-37e5-4ff4-a330-32ac947354d3` | unsure | 0.675 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `976f2df8-a133-4740-a9a0-f56f87e4146d` | ai | 0.919 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `b22f5db0-9024-4efb-b61f-4f3117fbe53a` | unsure | 0.646 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `b222e88d-23b9-4638-9c79-24f3c86329bc` | unsure | 0.806 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `79d6fe5a-7e80-46a1-aea1-495ce3795f3c` | unsure | 0.807 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `de71b629-d1ed-4b04-9ee9-5f976cfb4421` | unsure | 0.808 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `4f77defb-4bac-4f93-9e00-27ca1a30bc25` | unsure | 0.854 | HELD |
| FP06 | false_positive | a person imitating a formal template | 200 | `0b696a56-b5d5-45f7-8f0c-d484fc9dce4e` | unsure | 0.786 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `16d730c9-ea97-40ed-bc15-f4320ba5b38b` | unsure | 0.726 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `83a5b799-685a-46dc-972d-78c154de7992` | unsure | 0.460 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `151f7c7c-9eca-45bb-ac49-8c1964240085` | unsure | 0.456 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `d2779bae-2a5f-4655-998c-5ab619ef05b4` | human | 0.198 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `a2fb90ad-d076-44a6-9fc8-c610f4a1bf9b` | unsure | 0.520 | BROKE |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `fdafbe2e-4717-4bfd-8141-af748ddbdbcd` | unsure | 0.455 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `61cf3700-0e67-4c34-bf4d-368eaf56c4e8` | unsure | 0.495 | BROKE |
| PI06 | prompt_injection | instruction plus real human text | 200 | `ba88fd2f-64a1-4599-99c1-f7e3a55c5044` | unsure | 0.615 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `1fa09a16-3923-4fb0-83a9-06c1f4d2f2c6` | unsure | 0.410 | HELD |
| MF04 | malformed | text is only punctuation | 200 | `8a94cd8e-ffec-4ef3-a2cf-a2a672a81099` | unsure | 0.410 | HELD |
| MF05 | malformed | text is a very long single word | 200 | `b30fe77f-fbee-491b-9651-ff5bb2ae83fe` | unsure | 0.839 | HELD |
| MF06 | malformed | text is emoji only | 200 | `29724d6c-b4da-4626-a3e4-3375a82492ab` | unsure | 0.868 | HELD |
| MF07 | malformed | text is right-to-left script | 200 | `b3da88e8-d03d-4815-b857-d811d9d9306d` | unsure | 0.814 | HELD |
| MF08 | malformed | text is 60,000 characters | 200 | `d72aab5f-8163-4b05-8a0c-d289ff2946e3` | unsure | 0.883 | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `205970ab-c2ad-4829-92d2-03d6d781aa59` | unsure | 0.410 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b730d1e6-eb58-4749-bef3-e1dde859ffef` | unsure | 0.410 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `27f98630-031b-4307-8408-314483555176` | unsure | 0.410 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3ff600a1-7cd9-4487-9d90-afb2fe78a105` | unsure | 0.410 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `192b2a05-6ab6-4d81-8467-500bddd240cb` | unsure | 0.410 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9c88c1ab-2314-4f34-8371-1d510a5829b8` | unsure | 0.410 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

## Verdicts

| Family | HELD | BROKE |
|---|---|---|
| evasion | 1 | 9 |
| false_positive | 8 | 0 |
| prompt_injection | 2 | 4 |
| malformed | 20 | 0 |
| flood_same_creator | 12 | 0 |
| **total** | **43** | **13** |

Rule used (settled after the first run, before verdicts were filled in, and applied unchanged to both runs): AI-text attacks (EV, PI01-03, PI05) are HELD only
if labelled `ai`; human-text attacks (FP, PI04, PI06) are HELD if not labelled `ai`; MF01-02 and RQ* are HELD
on a 4xx; MF03-08 are HELD unless they get a confident `ai`/`human` verdict on non-text; the flood rows are HELD if 429 appears.

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "f4bbc85b-75ac-4638-b812-4fb49d426c21",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.4381,
  "model_score": 0.1635,
  "style_score": 0.85,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "501ad3b2-43da-4825-83b4-30c3819afb9d",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.41,
  "model_score": 0.5943,
  "style_score": 0.0144,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "5d3cd65b-9069-44a4-81eb-6ec82ff108fd",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5743,
  "model_score": 0.6662,
  "style_score": 0.4365,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "9e5f26b5-8d3b-402e-8907-b07a8132462e",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.7068,
  "model_score": 0.6114,
  "style_score": 0.85,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "b1d9eefb-c303-4172-80a9-ef03d3a8a3cd",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.3174,
  "model_score": 0.3212,
  "style_score": 0.3117,
  "label": "This looks like it was written by a person. There's nothing you need to do.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "240ac685-334f-4926-b530-1ef2becf8a6d",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4923,
  "model_score": 0.5727,
  "style_score": 0.3716,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "0c32661c-a17e-4722-9f83-82f7f47a47fb",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.4647,
  "model_score": 0.5862,
  "style_score": 0.2825,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "e5912bae-a52b-4520-8ddd-2b9eb84b2d80",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.474,
  "model_score": 0.2452,
  "style_score": 0.8172,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "29e5c7c4-37e5-4ff4-a330-32ac947354d3",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.6755,
  "model_score": 0.7042,
  "style_score": 0.6325,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "976f2df8-a133-4740-a9a0-f56f87e4146d",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.9187,
  "model_score": 0.9792,
  "style_score": 0.828,
  "label": "Our checks suggest this may have been written with the help of AI. These checks make mistakes, especially with plain or simple writing. If you wrote it yourself, please tell us and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "b22f5db0-9024-4efb-b61f-4f3117fbe53a",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.6456,
  "model_score": 0.6175,
  "style_score": 0.6878,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "b222e88d-23b9-4638-9c79-24f3c86329bc",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.8065,
  "model_score": 0.7387,
  "style_score": 0.9083,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "79d6fe5a-7e80-46a1-aea1-495ce3795f3c",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.8069,
  "model_score": 0.8051,
  "style_score": 0.8095,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "de71b629-d1ed-4b04-9ee9-5f976cfb4421",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.8079,
  "model_score": 0.8329,
  "style_score": 0.7705,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "4f77defb-4bac-4f93-9e00-27ca1a30bc25",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.8535,
  "model_score": 0.8005,
  "style_score": 0.9329,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "0b696a56-b5d5-45f7-8f0c-d484fc9dce4e",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.7858,
  "model_score": 0.8814,
  "style_score": 0.6423,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "16d730c9-ea97-40ed-bc15-f4320ba5b38b",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.7263,
  "model_score": 0.8816,
  "style_score": 0.4933,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "83a5b799-685a-46dc-972d-78c154de7992",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.4602,
  "model_score": 0.3223,
  "style_score": 0.667,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "151f7c7c-9eca-45bb-ac49-8c1964240085",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.4562,
  "model_score": 0.4625,
  "style_score": 0.4467,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "d2779bae-2a5f-4655-998c-5ab619ef05b4",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.1982,
  "model_score": 0.2044,
  "style_score": 0.1889,
  "label": "This looks like it was written by a person. There's nothing you need to do.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "a2fb90ad-d076-44a6-9fc8-c610f4a1bf9b",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5196,
  "model_score": 0.5943,
  "style_score": 0.4075,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "fdafbe2e-4717-4bfd-8141-af748ddbdbcd",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.455,
  "model_score": 0.4998,
  "style_score": 0.3877,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "61cf3700-0e67-4c34-bf4d-368eaf56c4e8",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4955,
  "model_score": 0.6401,
  "style_score": 0.2786,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "ba88fd2f-64a1-4599-99c1-f7e3a55c5044",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.6147,
  "model_score": 0.5583,
  "style_score": 0.6993,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "1fa09a16-3923-4fb0-83a9-06c1f4d2f2c6",
  "creator_id": "attacker_MF03",
  "guess": "unsure",
  "confidence": 0.41,
  "model_score": 0.0,
  "style_score": 0.6,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "8a94cd8e-ffec-4ef3-a2cf-a2a672a81099",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.41,
  "model_score": 0.0112,
  "style_score": 0.675,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "b30fe77f-fbee-491b-9651-ff5bb2ae83fe",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.8386,
  "model_score": 0.9976,
  "style_score": 0.6,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "29724d6c-b4da-4626-a3e4-3375a82492ab",
  "creator_id": "attacker_MF06",
  "guess": "unsure",
  "confidence": 0.8681,
  "model_score": 0.9969,
  "style_score": 0.675,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "b3da88e8-d03d-4815-b857-d811d9d9306d",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.8138,
  "model_score": 0.9064,
  "style_score": 0.675,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 200,
  "content_id": "d72aab5f-8163-4b05-8a0c-d289ff2946e3",
  "creator_id": "attacker_MF08",
  "guess": "unsure",
  "confidence": 0.8827,
  "model_score": 0.9876,
  "style_score": 0.7253,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "205970ab-c2ad-4829-92d2-03d6d781aa59",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.41,
  "model_score": 0.0287,
  "style_score": 0.6,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "b730d1e6-eb58-4749-bef3-e1dde859ffef",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.41,
  "model_score": 0.0287,
  "style_score": 0.6,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "27f98630-031b-4307-8408-314483555176",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.41,
  "model_score": 0.0287,
  "style_score": 0.6,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "3ff600a1-7cd9-4487-9d90-afb2fe78a105",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.41,
  "model_score": 0.0287,
  "style_score": 0.6,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "192b2a05-6ab6-4d81-8467-500bddd240cb",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.41,
  "model_score": 0.0287,
  "style_score": 0.6,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "9c88c1ab-2314-4f34-8371-1d510a5829b8",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.41,
  "model_score": 0.0287,
  "style_score": 0.6,
  "label": "We can't tell for sure how this was written, and we aren't saying it wasn't you. If you wrote it yourself, you don't need to do anything. You can ask a person to take a look at any time.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
