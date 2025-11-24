# forward.py
# Minimal forward implementation: pipelines payload straight through
def forward(request: bytes) -> bytes:
    # request already JSON bytes, just return it
    return request
