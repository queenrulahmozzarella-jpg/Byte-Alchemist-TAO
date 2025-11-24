from fastapi import FastAPI
from pydantic import BaseModel
from .agent import ByteAlchemistAgent
from .config import Config
from .utils import log

app = FastAPI(title="Byte-Alchemist-TAO Agent API")
cfg = Config()
agent = ByteAlchemistAgent()

class PromptRequest(BaseModel):
    prompt: str
    max_length: int = cfg.max_length

@app.get("/health")
def health():
    return {"status": "ok", "agent": "Byte-Alchemist-TAO"}

@app.post("/generate")
def generate(req: PromptRequest):
    log(f"API /generate called with prompt len={len(req.prompt)}")
    resp = agent.respond(req.prompt, max_length=req.max_length)
    return resp

# To run: uvicorn byte_alchemist.api:app --host 0.0.0.0 --port 8000
