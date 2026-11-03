#!/usr/bin/env python3
"""
Provenance Guard — the web service.

    python app.py

Then, in another terminal:

    curl -X POST http://127.0.0.1:5000/ping \
      -H "Content-Type: application/json" \
      -d '{"message": "hello"}'

That's the example route. It works right now, before you've written anything.
**Leave it alone** — it's your control. When something breaks later, check that
`/ping` still answers: if it does, the problem is in your handler; if it
doesn't, it's the service itself.

Routes:

    POST /ping        the worked example. Already works. Don't edit it
    POST /submit      score a piece of text
    POST /appeal      a writer disputes a result
    GET  /content/<id>  one item's current status
    GET  /log         the audit log. Already works
    GET  /health      is the service up, and is the model loaded
"""

import uuid

from flask import Flask, jsonify, request

import audit
import config
import detector
import scoring
import stylometry

app = Flask(__name__)


# ── Rate limiting — UNIT 8 ────────────────────────────────────────────────────
# Off until you turn it on. In unit 8, Milestone 1:
#
#   1. Set RATE_LIMITING_ENABLED = True in config.py (or AI201_RATE_LIMITS=1)
#   2. Choose your numbers there
#   3. Uncomment the @limiter.limit(...) line on /submit below
#
# The order doesn't matter. While limiting is off, that decorator is a no-op
# that quietly does nothing, so uncommenting it early costs you nothing — but
# it also means no 429 until you've done step 1.
#
# The storage backend is preconfigured, which stops Flask-Limiter printing a
# warning on every start. In-memory is right for one laptop and wrong for
# anything real — a restart forgets every count.

class _LimiterOff:
    """
    Stands in for the real limiter while rate limiting is off.

    It makes @limiter.limit(...) a decorator that returns the route
    untouched, so uncommenting the line before you flip the setting is
    harmless instead of a crash on startup.
    """

    def limit(self, *args, **kwargs):
        return lambda view: view


limiter = _LimiterOff()
if config.RATE_LIMITING_ENABLED:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address

    def rate_limit_key():
        """
        Who a request counts against.

        Falling back to the caller's address is the easy version. Unit 8's
        stretch asks about per-creator limits instead — and the difference
        matters: one script can look like a thousand callers, and one household
        can look like one.
        """
        payload = request.get_json(silent=True)
        # A body that parses as JSON but isn't an object — a bare list or
        # string — has no .get. Without this guard the key function raises
        # BEFORE the route runs, and a malformed request becomes a 500 that
        # looks like your handler crashed when your handler never ran.
        if not isinstance(payload, dict):
            return get_remote_address()
        creator = payload.get("creator_id")
        return creator if isinstance(creator, str) and creator.strip() else get_remote_address()

    limiter = Limiter(
        key_func=rate_limit_key,
        app=app,
        storage_uri=config.RATE_LIMIT_STORAGE,
        default_limits=[],
    )

    @app.errorhandler(429)
    def rate_limited(exc):
        """
        A rejected request still leaves a trace.

        ⚠️ An attack that shows up only as an absence is one you'll never find.
        """
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            payload = {}
        audit.log_rejection(
            creator_id=payload.get("creator_id", "unknown"),
            reason="rate_limited",
            limit=str(exc.description),
        )
        return jsonify({
            "error": "rate_limited",
            "message": "Too many submissions. Try again shortly.",
            "limit": str(exc.description),
        }), 429


# ── The worked example. Already works. Don't edit. ────────────────────────────

@app.post("/ping")
def ping():
    """
    Everything a route needs, in six lines.

    JSON arrives as a dict. You pull things out of it. You return a dict and
    the framework turns it into a response. That's the whole idea.
    """
    payload = request.get_json(silent=True) or {}
    return jsonify({
        "ok": True,
        "you_sent": payload.get("message"),
        "service": "provenance-guard",
    })


@app.get("/health")
def health():
    """Is the service up, and has the model been downloaded yet?"""
    import detector

    loaded = detector._model is not None
    return jsonify({
        "ok": True,
        "detector_model": config.DETECTOR_MODEL,
        "detector_loaded": loaded,
        "rate_limiting": config.RATE_LIMITING_ENABLED,
        "log_entries": len(audit.read_entries()),
    })


# ── Submissions and appeals ───────────────────────────────────────────────────

MAX_TEXT_CHARS = 100_000


def _reject(creator_id, reason: str, message: str, status: int):
    """Refuse a request, leave a trace in the audit log, and tell the caller why."""
    who = creator_id.strip() if isinstance(creator_id, str) and creator_id.strip() else "unknown"
    audit.log_rejection(creator_id=who, reason=reason, message=message)
    return jsonify({"error": reason, "message": message}), status


@app.post("/submit")
@limiter.limit(f"{config.RATE_LIMIT_PER_MINUTE}/minute;{config.RATE_LIMIT_PER_DAY}/day")
def submit():
    """
    Take a piece of text, decide about it, log the decision, answer.

    Expects {"text": "...", "creator_id": "..."}. Bad input gets a 4xx and a
    "rejected" line in the log; a crash on malformed input is not an option.
    """
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return _reject(None, "invalid_request", "Send a JSON object with 'text' and 'creator_id'.", 400)

    text = payload.get("text")
    creator_id = payload.get("creator_id")

    if not isinstance(text, str) or not text.strip():
        return _reject(creator_id, "invalid_request", "'text' must be a non-empty string.", 400)
    if len(text) > MAX_TEXT_CHARS:
        return _reject(creator_id, "text_too_large",
                       f"'text' must be at most {MAX_TEXT_CHARS:,} characters.", 413)
    if not isinstance(creator_id, str) or not creator_id.strip():
        return _reject(None, "invalid_request", "'creator_id' must be a non-empty string.", 400)
    creator_id = creator_id.strip()

    try:
        model_score = detector.model_signal(text)
    except detector.DetectorUnavailable as exc:
        return jsonify({"error": "detector_unavailable", "message": str(exc)}), 503
    except ValueError as exc:  # too short to score
        return _reject(creator_id, "invalid_text", str(exc), 400)

    style_score = stylometry.style_signal(text)
    combined_score = scoring.combine_signals(model_score, style_score)

    # Milestone 5 replaces the label placeholder.
    guess, label = scoring.score_to_label(combined_score)

    content_id = str(uuid.uuid4())
    audit.log_decision(
        content_id=content_id,
        creator_id=creator_id,
        guess=guess,
        model_score=model_score,
        style_score=style_score,
        combined_score=combined_score,
        label=label,
    )
    return jsonify({
        "content_id": content_id,
        "guess": guess,
        "confidence": combined_score,
        "label": label,
        "model_score": model_score,
        "style_score": style_score,
        "combined_score": combined_score,
    })


@app.post("/appeal")
def appeal():
    """
    A writer says we got it wrong. Record it next to the decision and confirm.

    Expects {"content_id": "...", "reasoning": "..."}. An unknown content_id is
    a 404 and writes nothing, so a typo can't create a ghost appeal.
    """
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        payload = {}
    content_id = payload.get("content_id")
    reasoning = payload.get("reasoning")

    if not isinstance(content_id, str) or not content_id.strip():
        return jsonify({"error": "invalid_request",
                        "message": "'content_id' must be a non-empty string."}), 400
    if not isinstance(reasoning, str) or not reasoning.strip():
        return jsonify({"error": "invalid_request",
                        "message": "'reasoning' must be a non-empty string."}), 400

    content_id = content_id.strip()
    decision = _decision_for(content_id)
    if decision is None:
        return jsonify({"error": "not_found",
                        "message": "We have no submission with that content_id."}), 404

    audit.log_appeal(
        content_id=content_id,
        creator_id=decision["creator_id"],
        reasoning=reasoning.strip(),
    )
    return jsonify({
        "content_id": content_id,
        "status": "under_review",
        "message": "Thank you. Your appeal is recorded and a person will review it.",
    })


def _decision_for(content_id: str):
    """The original decision entry for a content id, or None if it never existed."""
    for entry in audit.entries_for(content_id):
        if entry.get("event") is None and entry.get("status") in ("decided", "under_review"):
            return entry
    return None


@app.get("/content/<content_id>")
def content_status(content_id):
    """Stretch: one item's current status, label, and any appeals."""
    decision = _decision_for(content_id)
    if decision is None:
        return jsonify({"error": "not_found",
                        "message": "We have no submission with that content_id."}), 404
    appeals = [e for e in audit.entries_for(content_id) if e.get("event") == "appeal"]
    return jsonify({
        "content_id": content_id,
        "status": "under_review" if appeals else decision["status"],
        "guess": decision["guess"],
        "label": decision["label"],
        "appeals": [{"timestamp": a["timestamp"], "reasoning": a["reasoning"]} for a in appeals],
    })


# ── Already works ─────────────────────────────────────────────────────────────

@app.get("/log")
def get_log():
    """
    The audit log, most recent last.

        curl "http://127.0.0.1:5000/log?limit=10"

    You need this in unit 8 to paste entries into your README, and you need it
    now to see whether your logging is actually working.
    """
    limit = request.args.get("limit", type=int)
    entries = audit.read_entries(limit=limit)
    return jsonify({"count": len(entries), "entries": entries})


def main():
    print(f"Provenance Guard on http://{config.HOST}:{config.PORT}")
    print(f"  detector model:  {config.DETECTOR_MODEL}")
    print(f"  rate limiting:   {'ON' if config.RATE_LIMITING_ENABLED else 'off (unit 8)'}")
    print(f"  audit log:       {config.AUDIT_LOG}")
    print()
    print("Check it's alive:")
    print(f'  curl -X POST http://{config.HOST}:{config.PORT}/ping \\')
    print('    -H "Content-Type: application/json" \\')
    print("    -d '{\"message\": \"hello\"}'")
    print()
    # debug=True hands out an interactive debugger, so it's local-only — see config.py
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)


if __name__ == "__main__":
    main()
