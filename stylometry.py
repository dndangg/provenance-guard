"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures ───────────────────────────────────────────────────────
# Each returns a RAW number. `style_signal` flips and scales them onto 0–1.

# Raw → AI-likeness anchors, picked by looking at the calibration inputs in
# the README. Between the two anchors the score slides linearly; outside, it
# clamps. They are judgement calls, not calibrated truth.
BURSTINESS_AI, BURSTINESS_HUMAN = 0.25, 0.75   # CV of sentence length
MATTR_AI, MATTR_HUMAN = 0.55, 0.95             # moving-average type-token ratio (wide on purpose: see STYLE_PARTS)
EXPRESSIVE_AI, EXPRESSIVE_HUMAN = 0.0, 3.0     # expressive marks per 100 words

MATTR_WINDOW = 40
EXPRESSIVE_MARKS = ";:—–()!?…"


def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def _ai_likeness(raw: float, ai_end: float, human_end: float) -> float:
    """Slide a raw measure onto 0–1 where the AI-ish end is 1 and the human-ish end is 0."""
    return _clamp((human_end - raw) / (human_end - ai_end))


def sentence_length_spread(text: str) -> float:
    """
    Burstiness: standard deviation of sentence length over the mean (words).

    Higher = lumpier = more human-like. Dividing by the mean makes a long text
    and a short one comparable. Returns None when there are fewer than two
    sentences: a single sentence has no rhythm to measure, and 0.0 would claim
    it is perfectly even.
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n]
    if len(lengths) < 2:
        return None
    mean = statistics.mean(lengths)
    return statistics.stdev(lengths) / mean if mean else 0.0


def type_token_ratio(text: str) -> float:
    """
    Vocabulary variety as a moving-average type-token ratio (MATTR).

    A plain unique/total ratio falls as text gets longer, so a long essay would
    always look repetitive. MATTR averages the ratio over a sliding window of
    MATTR_WINDOW words, which removes most of the length effect. Texts shorter
    than the window fall back to the plain ratio. Higher = more varied =
    more human-like. Returns None for empty text.
    """
    toks = words(text)
    if not toks:
        return None
    if len(toks) <= MATTR_WINDOW:
        return len(set(toks)) / len(toks)
    ratios = [
        len(set(toks[i:i + MATTR_WINDOW])) / MATTR_WINDOW
        for i in range(len(toks) - MATTR_WINDOW + 1)
    ]
    return sum(ratios) / len(ratios)


def punctuation_density(text: str) -> float:
    """
    Expressive punctuation per 100 words: semicolons, colons, dashes,
    parentheses, ! ? and ellipses.

    Full stops and commas are left out on purpose: everyone uses them, so they
    say little. The marks above vary far more between writers. Higher = more
    human-like.
    """
    n = len(words(text))
    if not n:
        return 0.0
    marks = sum(text.count(ch) for ch in EXPRESSIVE_MARKS)
    marks += len(re.findall(r"\s-\s|--|\.\.\.", text))
    return 100.0 * marks / n


# ── Combining them ───────────────────────────────────────────────────────────

# burstiness, vocabulary, punctuation. Vocabulary gets the small share because
# on my calibration inputs it did NOT separate the groups: the AI and formal
# samples had high variety (MATTR ~0.9) and Twain and the plain writer lower
# (~0.75). Five samples can't prove the direction is wrong, so I kept the
# hypothesis but stopped it from swinging the score.
STYLE_PARTS = (0.50, 0.15, 0.35)


def style_parts(text: str) -> dict:
    """The three AI-likeness components (0–1 each), for debugging."""
    spread = sentence_length_spread(text)
    variety = type_token_ratio(text)
    return {
        "burstiness": 0.5 if spread is None else _ai_likeness(spread, BURSTINESS_AI, BURSTINESS_HUMAN),
        "vocabulary": 0.5 if variety is None else _ai_likeness(variety, MATTR_AI, MATTR_HUMAN),
        "punctuation": _ai_likeness(punctuation_density(text), EXPRESSIVE_AI, EXPRESSIVE_HUMAN),
    }


def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.**

    Each measure is flipped so that "even / repetitive / plain" is high, scaled
    onto 0–1 with the anchors above, then blended 0.50 burstiness, 0.15
    vocabulary, 0.35 punctuation. Burstiness leads because it is the most
    stable of the three; punctuation is the easiest for a writer to change on
    purpose. With too little text to measure rhythm, that part is a neutral 0.5.
    """
    parts = style_parts(text)
    score = sum(w * p for w, p in zip(STYLE_PARTS, parts.values()))
    return round(_clamp(score), 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    spread, variety = sentence_length_spread(text), type_token_ratio(text)
    print(f"sentence_length_spread   {spread if spread is None else round(spread, 3)}   (higher = more human)")
    print(f"type_token_ratio (MATTR) {variety if variety is None else round(variety, 3)}   (higher = more human)")
    print(f"punctuation_density      {round(punctuation_density(text), 3)}   per 100 words (higher = more human)")
    print(f"AI-likeness of each part {style_parts(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
