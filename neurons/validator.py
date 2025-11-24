import json, sys
from byte_alchemist.utils import log
from sklearn.metrics import accuracy_score

def score_response(candidate_code: str, gold_tests: dict) -> float:
    """
    Lightweight scoring: gold_tests is a dict containing e.g. {"contains": ["def foo", "return"]}
    This is intentionally simple — validators should use unit tests or static analysis.
    """
    score = 0.0
    try:
        total = len(gold_tests.get("contains", []))
        if total == 0:
            return 0.0
        hits = sum(1 for token in gold_tests["contains"] if token in candidate_code)
        score = hits / total
    except Exception as e:
        log(f"Validator scoring error: {e}")
    return float(score)

def handle_request(req_bytes: bytes) -> bytes:
    # payload: {"candidate_code": "...", "gold_tests": {"contains": ["def foo"]}}
    try:
        payload = json.loads(req_bytes.decode("utf-8"))
        code = payload.get("candidate_code", "")
        tests = payload.get("gold_tests", {})
        sc = score_response(code, tests)
        return json.dumps({"score": sc}).encode("utf-8")
    except Exception as e:
        log(f"Validator error: {e}")
        return json.dumps({"error": str(e)}).encode("utf-8")

if __name__ == "__main__":
    req = sys.stdin.buffer.read()
    sys.stdout.buffer.write(handle_request(req))
