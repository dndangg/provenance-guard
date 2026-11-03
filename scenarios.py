"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

# Criteria (see criteria.md):
#   1  human writing almost never called AI          -> "human writing"
#   2  AI text scores well above human text          -> "clearly AI" + "clearly human"
#   3  every label reachable, 0.51 != 0.95           -> "all labels" + "label sweep"
#   4  an appeal always changes status and is logged -> "appeals"
#   5  bad input never crashes and is never silent   -> "bad input"
#
# The first 6 "human writing" texts are public-domain or casual human prose; the
# last 4 are deliberately plain (short sentences, common words). The plain ones
# were written for this test, NOT pulled from a real writer. Criterion 1 is
# really about *your* writing, so swap your own pieces in before you trust it.
# Scenario names must differ in their first 12 characters: run_eval.py builds
# each creator_id from them, and a shared creator_id shares a rate limit.

HUMAN_PIECES = [
    "You don't know about me without you have read a book by the name of The Adventures of Tom Sawyer; but that ain't no matter. That book was made by Mr. Mark Twain, and he told the truth, mainly. There was things which he stretched, but mainly he told the truth. That is nothing. I never seen anybody but lied one time or another, without it was Aunt Polly, or the widow, or maybe Mary.",
    "Honestly? I didn't want to move. Everything I knew was in that tiny flat \u2014 the chipped blue mug, the radiator that clanked all winter (it still does, I assume), my neighbour's terrible singing. But the new job was in Leeds, and rent in London was eating me alive. So: boxes, tape, a lot of swearing.",
    "It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife. However little known the feelings or views of such a man may be on his first entering a neighbourhood, this truth is so well fixed in the minds of the surrounding families, that he is considered as the rightful property of some one or other of their daughters.",
    "It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, it was the season of Darkness, it was the spring of hope, it was the winter of despair.",
    "I went to the woods because I wished to live deliberately, to front only the essential facts of life, and see if I could not learn what it had to teach, and not, when I came to die, discover that I had not lived.",
    "When we look to the individuals of the same variety or sub-variety of our older cultivated plants and animals, one of the first points which strikes us, is, that they generally differ much more from each other, than do the individuals of any one species or variety in a state of nature.",
    "I live in a small town. My school is near my house. Every day I walk to school with my friend. We talk about our classes and our families. After school I do my homework. Then I help my mother cook dinner. I like to cook rice and vegetables.",
    "We got a dog last year. His name is Max. He is brown and white. He likes to run in the park. Every morning I take him for a walk. He eats a lot. He sleeps on my bed. I love him very much.",
    "I work at a shop. The shop sells shoes. I start at nine in the morning. I help the people who come in. I find the right size for them. At lunch I eat with my coworker. I go home at five. It is a good job.",
    "Last summer we went to the sea. The drive was long. My brother was sick in the car. The beach was very nice. We swam and ate ice cream. The water was cold. We stayed for three days. I want to go again.",
]

AI_PIECES = [
    "Effective time management is essential for achieving both personal and professional success. By prioritizing tasks, setting clear goals, and minimizing distractions, individuals can significantly improve their productivity. Furthermore, it is important to take regular breaks in order to maintain focus and avoid burnout. Ultimately, adopting a structured approach to time management enables people to accomplish more while maintaining a healthy work-life balance.",
    "Climate change is one of the most pressing challenges facing our world today. It is caused primarily by the burning of fossil fuels, which releases greenhouse gases into the atmosphere. Moreover, deforestation and industrial agriculture contribute significantly to rising global temperatures. To address this issue, governments, businesses, and individuals must work together to adopt sustainable practices and reduce carbon emissions.",
    "Artificial intelligence has the potential to transform numerous industries in the coming years. In healthcare, AI-powered tools can assist doctors in diagnosing diseases more accurately and efficiently. In education, personalized learning platforms can adapt to the needs of individual students. However, it is crucial to consider the ethical implications of these technologies and ensure they are developed responsibly.",
    "A healthy lifestyle is built on three key pillars: balanced nutrition, regular exercise, and adequate sleep. Eating a variety of fruits, vegetables, and whole grains provides the body with essential nutrients. Additionally, engaging in at least thirty minutes of physical activity each day can improve cardiovascular health. By prioritizing these habits, individuals can enhance their overall well-being and quality of life.",
    "Effective communication is a fundamental skill in any workplace environment. It involves not only conveying information clearly but also listening actively to others. Furthermore, strong communication fosters collaboration, builds trust, and reduces misunderstandings among team members. As a result, organizations that prioritize communication tend to achieve better outcomes and higher employee satisfaction.",
]

SCENARIOS = [
    {"name": "human writing", "criterion": 1, "texts": HUMAN_PIECES},
    {"name": "clearly AI", "criterion": 2, "texts": AI_PIECES},
    # the five most clearly-human pieces: Twain, the casual one, Austen, Dickens, Thoreau
    {"name": "clearly human", "criterion": 2,
     "texts": [HUMAN_PIECES[i] for i in (0, 1, 2, 3, 4)]},
    # 15 real submissions spanning the range (10 human + 5 AI); criterion 3 needs >= 12
    {"name": "all labels", "criterion": 3, "texts": HUMAN_PIECES + AI_PIECES},
    # no HTTP: sweeps combined_score 0.00-1.00 through scoring.score_to_label
    {"name": "label sweep", "criterion": 3, "sweep": True},
    # submit, then appeal against the returned content_id, then read /log back.
    # Also appeals once against an id that doesn't exist.
    {"name": "appeals", "criterion": 4, "appeal": True, "texts": HUMAN_PIECES[:5]},
    {"name": "bad input", "criterion": 5, "bodies": [
        {"creator_id": "eval_bad_missing"},
        {"text": None, "creator_id": "eval_bad_null"},
        {"text": "", "creator_id": "eval_bad_empty"},
        {"text": "   \n\t  ", "creator_id": "eval_bad_blank"},
        {"text": 5, "creator_id": "eval_bad_number"},
        {"text": "x" * 100_001, "creator_id": "eval_bad_huge"},
        {"text": "A perfectly good sentence with no creator attached."},
    ]},
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        if scenario.get("sweep"):  # no requests are sent for a sweep
            continue

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
