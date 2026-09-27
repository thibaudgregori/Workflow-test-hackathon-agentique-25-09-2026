"""Envoie les demandes de demandes.jsonl au chat du workflow, une par une (Python 3.9+, rien à installer).

    python3 envoyer_demandes.py --de 1 --a 1       # test de fumée : la première demande seulement
    python3 envoyer_demandes.py --de 1 --a 15      # session 1
    python3 envoyer_demandes.py --de 16 --a 30     # session 2, au moins 2 h plus tard

L'adresse du chat est lue dans .env.n8n-test (écrit par preparer_n8n.py), ou passée par --chat.
Chaque demande déclenche environ 19 appels gpt-4.1-mini et prend quelques minutes.
"""
import argparse
import json
import secrets
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent


def chat_url():
    env = HERE / ".env.n8n-test"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            if line.startswith("N8N_CHAT_URL="):
                return line.split("=", 1)[1]
    return None


def main():
    ap = argparse.ArgumentParser(description="Envoie les demandes au chat n8n")
    ap.add_argument("--de", type=int, default=1)
    ap.add_argument("--a", type=int, default=30)
    ap.add_argument("--chat", default=chat_url())
    args = ap.parse_args()
    if not args.chat:
        sys.exit("adresse du chat inconnue : lancez preparer_n8n.py, ou passez --chat")
    demandes = [json.loads(l) for l in (HERE / "demandes.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    for d in demandes[args.de - 1:args.a]:
        body = {"action": "sendMessage", "sessionId": f"{d['id']}-{secrets.token_hex(3)}", "chatInput": d["texte"]}
        req = urllib.request.Request(args.chat, data=json.dumps(body).encode(), method="POST",
                                     headers={"Content-Type": "application/json"})
        t0 = time.time()
        try:
            with urllib.request.urlopen(req, timeout=900) as r:
                r.read()
                status = r.status
        except urllib.error.HTTPError as e:
            status = f"{e.code} {e.read().decode()[:120]}"
        except (urllib.error.URLError, TimeoutError) as e:
            status = f"échec : {e}"
        print(f"{d['id']}  {status}  {time.time() - t0:5.0f} s  {d['texte'][:60]}", flush=True)


if __name__ == "__main__":
    main()
