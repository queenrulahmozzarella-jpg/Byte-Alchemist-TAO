import json, datetime, os

LOGFILE = "byte_alchemist.log"

def log(msg: str):
    ts = datetime.datetime.utcnow().isoformat()
    s = f"[{ts}] {msg}"
    with open(LOGFILE,"a",encoding="utf-8") as f:
        f.write(s + "\n")
    print(s)

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
