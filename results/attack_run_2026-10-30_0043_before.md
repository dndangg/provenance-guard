# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-10-30 00:43
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `a1fa278e-d2f2-4c16-bb93-e93fa440ceb2` | unsure | 0.438 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `31abc9e7-6630-4df4-aa41-77be636729d9` | unsure | 0.410 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `6f3e72fb-449d-4b4a-87d1-23c48dbb78c2` | unsure | 0.574 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `16d1c64d-40db-4e16-b25f-e79d2bd75034` | ai | 0.707 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `f289d0f6-8c0b-456d-8cde-1837728fac97` | human | 0.317 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `0a35f6d2-3a23-4039-8fe5-be7f52dde4bf` | unsure | 0.492 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `ebb459dc-4dbb-4331-9b8a-b591b4ff4726` | unsure | 0.465 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `4fa62e96-b725-4394-9491-82d9d73a0f71` | unsure | 0.474 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `890b2bb2-798b-44c0-a382-80149d32ce82` | unsure | 0.675 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `c9accbfb-e93f-417c-847d-397caf1f04b9` | ai | 0.919 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `815d3b51-0bb9-4ea7-b096-7ae5c946f6b6` | unsure | 0.646 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `a4e56a90-e4ad-4747-b7d5-a4e5f8e94532` | ai | 0.806 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `52d9ca30-6af6-40a9-854f-586a57b74941` | ai | 0.807 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `517b4636-a471-4acc-bc6a-27f2607ce5b9` | ai | 0.808 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | `e0c0e431-5dba-4d14-a436-59ce6acf77fa` | ai | 0.854 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `352bdd49-2840-4040-8332-99d9684a1b2e` | ai | 0.786 | BROKE |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `e41de83d-6ec7-4413-a9f3-4af78a7da8be` | unsure | 0.690 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `3a07b560-9f0b-43f7-9a84-6dd96f3efd3d` | unsure | 0.460 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `6f135b6d-f303-4051-a3e8-1f61f2bd0dba` | unsure | 0.456 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `e4c24fb8-9d5f-418b-acf6-addba52eafe0` | human | 0.198 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `0e4c40c4-3be6-4d19-8a8c-90db9ce9ad6f` | unsure | 0.520 | BROKE |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `bbb26ae7-0469-475a-b958-fac30ae3b65b` | unsure | 0.455 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `f9a5b732-434f-4e70-a7f9-55aecc775d62` | unsure | 0.495 | BROKE |
| PI06 | prompt_injection | instruction plus real human text | 200 | `4396eec3-adfe-4034-8033-d1ab9a52b701` | unsure | 0.615 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `58f24b84-78e8-4e62-9af7-7f7f13fd9c0a` | unsure | 0.410 | HELD |
| MF04 | malformed | text is only punctuation | 200 | `87293520-c340-4670-9b97-ef470f6e0e57` | unsure | 0.410 | HELD |
| MF05 | malformed | text is a very long single word | 200 | `6b771847-784b-4405-b1be-bcbaf1d3c316` | unsure | 0.690 | HELD |
| MF06 | malformed | text is emoji only | 200 | `b4da5607-1b70-41e5-929f-3590709cbf7b` | unsure | 0.690 | HELD |
| MF07 | malformed | text is right-to-left script | 200 | `0092f167-2d75-47de-9ce6-3a55678c31e1` | ai | 0.814 | BROKE |
| MF08 | malformed | text is 60,000 characters | 200 | `d46d0452-1ff4-470d-a9e2-a7855def2dd9` | ai | 0.883 | BROKE |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `dd89eb30-e8c4-40af-b119-6201a7ec3e4b` | unsure | 0.410 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3d327c3d-2357-4f4b-a9e3-25a5ca03f96d` | unsure | 0.410 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `da62233b-352e-41a2-8442-5c086836de5e` | unsure | 0.410 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4fdc1692-c8ea-45a2-86f6-2268972dbd0b` | unsure | 0.410 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f3901d60-7a11-488a-8655-0a606bde1bfa` | unsure | 0.410 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a45942ff-2db8-4360-8842-844cc6bbda74` | unsure | 0.410 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

## Verdicts

| Family | HELD | BROKE |
|---|---|---|
| evasion | 2 | 8 |
| false_positive | 3 | 5 |
| prompt_injection | 2 | 4 |
| malformed | 18 | 2 |
| flood_same_creator | 12 | 0 |
| **total** | **37** | **19** |

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
  "content_id": "a1fa278e-d2f2-4c16-bb93-e93fa440ceb2",
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
  "content_id": "31abc9e7-6630-4df4-aa41-77be636729d9",
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
  "content_id": "6f3e72fb-449d-4b4a-87d1-23c48dbb78c2",
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
  "content_id": "16d1c64d-40db-4e16-b25f-e79d2bd75034",
  "creator_id": "attacker_EV04",
  "guess": "ai",
  "confidence": 0.7068,
  "model_score": 0.6114,
  "style_score": 0.85,
  "label": "Our checks suggest this may have been written with the help of AI. These checks make mistakes, especially with plain or simple writing. If you wrote it yourself, please tell us and a person will review it.",
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
  "content_id": "f289d0f6-8c0b-456d-8cde-1837728fac97",
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
  "content_id": "0a35f6d2-3a23-4039-8fe5-be7f52dde4bf",
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
  "content_id": "ebb459dc-4dbb-4331-9b8a-b591b4ff4726",
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
  "content_id": "4fa62e96-b725-4394-9491-82d9d73a0f71",
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
  "content_id": "890b2bb2-798b-44c0-a382-80149d32ce82",
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
  "content_id": "c9accbfb-e93f-417c-847d-397caf1f04b9",
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
  "content_id": "815d3b51-0bb9-4ea7-b096-7ae5c946f6b6",
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
  "content_id": "a4e56a90-e4ad-4747-b7d5-a4e5f8e94532",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.8065,
  "model_score": 0.7387,
  "style_score": 0.9083,
  "label": "Our checks suggest this may have been written with the help of AI. These checks make mistakes, especially with plain or simple writing. If you wrote it yourself, please tell us and a person will review it.",
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
  "content_id": "52d9ca30-6af6-40a9-854f-586a57b74941",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.8069,
  "model_score": 0.8051,
  "style_score": 0.8095,
  "label": "Our checks suggest this may have been written with the help of AI. These checks make mistakes, especially with plain or simple writing. If you wrote it yourself, please tell us and a person will review it.",
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
  "content_id": "517b4636-a471-4acc-bc6a-27f2607ce5b9",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.8079,
  "model_score": 0.8329,
  "style_score": 0.7705,
  "label": "Our checks suggest this may have been written with the help of AI. These checks make mistakes, especially with plain or simple writing. If you wrote it yourself, please tell us and a person will review it.",
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
  "content_id": "e0c0e431-5dba-4d14-a436-59ce6acf77fa",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.8535,
  "model_score": 0.8005,
  "style_score": 0.9329,
  "label": "Our checks suggest this may have been written with the help of AI. These checks make mistakes, especially with plain or simple writing. If you wrote it yourself, please tell us and a person will review it.",
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
  "content_id": "352bdd49-2840-4040-8332-99d9684a1b2e",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.7858,
  "model_score": 0.8814,
  "style_score": 0.6423,
  "label": "Our checks suggest this may have been written with the help of AI. These checks make mistakes, especially with plain or simple writing. If you wrote it yourself, please tell us and a person will review it.",
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
  "content_id": "e41de83d-6ec7-4413-a9f3-4af78a7da8be",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.69,
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
  "content_id": "3a07b560-9f0b-43f7-9a84-6dd96f3efd3d",
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
  "content_id": "6f135b6d-f303-4051-a3e8-1f61f2bd0dba",
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
  "content_id": "e4c24fb8-9d5f-418b-acf6-addba52eafe0",
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
  "content_id": "0e4c40c4-3be6-4d19-8a8c-90db9ce9ad6f",
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
  "content_id": "bbb26ae7-0469-475a-b958-fac30ae3b65b",
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
  "content_id": "f9a5b732-434f-4e70-a7f9-55aecc775d62",
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
  "content_id": "4396eec3-adfe-4034-8033-d1ab9a52b701",
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
  "content_id": "58f24b84-78e8-4e62-9af7-7f7f13fd9c0a",
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
  "content_id": "87293520-c340-4670-9b97-ef470f6e0e57",
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
  "content_id": "6b771847-784b-4405-b1be-bcbaf1d3c316",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.69,
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
  "content_id": "b4da5607-1b70-41e5-929f-3590709cbf7b",
  "creator_id": "attacker_MF06",
  "guess": "unsure",
  "confidence": 0.69,
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
  "content_id": "0092f167-2d75-47de-9ce6-3a55678c31e1",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.8138,
  "model_score": 0.9064,
  "style_score": 0.675,
  "label": "Our checks suggest this may have been written with the help of AI. These checks make mistakes, especially with plain or simple writing. If you wrote it yourself, please tell us and a person will review it.",
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
  "content_id": "d46d0452-1ff4-470d-a9e2-a7855def2dd9",
  "creator_id": "attacker_MF08",
  "guess": "ai",
  "confidence": 0.8827,
  "model_score": 0.9876,
  "style_score": 0.7253,
  "label": "Our checks suggest this may have been written with the help of AI. These checks make mistakes, especially with plain or simple writing. If you wrote it yourself, please tell us and a person will review it.",
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
  "content_id": "dd89eb30-e8c4-40af-b119-6201a7ec3e4b",
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
  "content_id": "3d327c3d-2357-4f4b-a9e3-25a5ca03f96d",
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
  "content_id": "da62233b-352e-41a2-8442-5c086836de5e",
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
  "content_id": "4fdc1692-c8ea-45a2-86f6-2268972dbd0b",
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
  "content_id": "f3901d60-7a11-488a-8655-0a606bde1bfa",
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
  "content_id": "a45942ff-2db8-4360-8842-844cc6bbda74",
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
