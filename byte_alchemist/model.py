from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from .config import Config
from .utils import log

cfg = Config()

class CodeGenerator:
    def __init__(self, model_name: str = cfg.model_name, device: str = cfg.device):
        log(f"Initializing model {model_name} on {device}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        if device == "cuda" and torch.cuda.is_available():
            self.model = self.model.cuda()
        self.pipe = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer, device=0 if device=="cuda" else -1)

    def generate(self, prompt: str, max_length: int = cfg.max_length, temperature: float = cfg.generation_temperature):
        # returns generated string
        out = self.pipe(prompt, max_length=max_length, do_sample=False, temperature=temperature)
        generated = out[0]["generated_text"]
        log(f"Generated length={len(generated)}")
        return generated
