from dataclasses import dataclass

@dataclass
class Config:
    model_name: str = "facebook/opt-125m"   # default small model for local testing; swap for code models
    device: str = "cuda"                  # or "cpu"
    max_length: int = 512
    generation_temperature: float = 0.0
    api_host: str = "0.0.0.0"
    api_port: int = 8000
