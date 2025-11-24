import json, sys
from byte_alchemist.agent import ByteAlchemistAgent
from byte_alchemist.utils import log

agent = ByteAlchemistAgent()

def handle_request(req_bytes: bytes) -> bytes:
    """
    The subnet template usually calls miners with bytes (JSON). This function
    reads the prompt and returns the response bytes.
    Expected payload: {"prompt": "...", "max_length": 400}
    """
    try:
        payload = json.loads(req_bytes.decode("utf-8"))
        prompt = payload.get("prompt", "")
        max_len = payload.get("max_length", 512)
        result = agent.respond(prompt, max_length=max_len)
        return json.dumps({"result": result}).encode("utf-8")
    except Exception as e:
        log(f"Miner error: {e}")
        return json.dumps({"error": str(e)}).encode("utf-8")

if __name__ == "__main__":
    # useful for local testing: read stdin and write stdout
    req = sys.stdin.buffer.read()
    sys.stdout.buffer.write(handle_request(req))
