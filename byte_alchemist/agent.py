import json
from .model import CodeGenerator
from .config import Config
from .utils import log, ensure_dir

cfg = Config()

class ByteAlchemistAgent:
    def __init__(self, model_name: str = cfg.model_name):
        self.gen = CodeGenerator(model_name=model_name)
        ensure_dir("outputs")
        log("ByteAlchemistAgent initialized")

    def respond(self, prompt: str, max_length: int = cfg.max_length):
        code = self.gen.generate(prompt, max_length=max_length)
        # minimal postprocessing: ensure returns only the code portion
        return {"code": code, "metadata": {"len": len(code)}}
