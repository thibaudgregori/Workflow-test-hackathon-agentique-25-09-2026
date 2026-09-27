"""Envoie les demandes de demandes.jsonl au chat du workflow, une par une (Python 3.9+, rien à installer).

    python3 envoyer_demandes.py --de 1 --a 1       # test de fumée : la première demande seulement
    python3 envoyer_demandes.py --de 1 --a 15      # session 1
    python3 envoyer_demandes.py --de 16 --a 30     # session 2, au moins 2 h plus tard

L'adresse du chat est lue dans .env.n8n-test (écrit par preparer_n8n.py), ou passée par --chat.
Chaque demande déclenche environ 19 appels gpt-4.1-mini et prend quelques minutes.

GARDE-FOU : le modèle 4553 n'a aucune limite à sa boucle « idée refusée → nouvelle idée ». Au premier
essai, une seule demande a tourné 12 minutes et fait 357 appels (0,37 $). Au-delà de --max-minutes
(5 par défaut), le script arrête lui-même l'exécution dans n8n et passe à la demande suivante.
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


def settings():
    env = HERE / ".env.n8n-test"
    if not env.exists():
        return {}
    return dict(line.split("=", 1) for line in env.read_text(encoding="utf-8").splitlines() if "=" in line)


def stop_running(conf):
    """Arrête les exécutions encore en cours de ce workflow ; rend leur nombre."""
    if not conf.get("N8N_API_KEY"):
        return 0
    api, headers = conf["N8N_URL"] + "/api/v1/executions", {"X-N8N-API-KEY": conf["N8N_API_KEY"]}
    url = f"{api}?status=running&workflowId={conf.get('N8N_WORKFLOW_ID', '')}&limit=50"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
        running = json.load(r)["data"]
    for execution in running:
        req = urllib.request.Request(f"{api}/{execution['id']}/stop", method="POST", headers=headers)
        urllib.request.urlopen(req, timeout=30).read()
    return len(running)


def main():
    ap = argparse.ArgumentParser(description="Envoie les demandes au chat n8n")
    ap.add_argument("--de", type=int, default=1)
    ap.add_argument("--a", type=int, default=30)
    ap.add_argument("--max-minutes", type=float, default=5, help="au-delà, l'exécution est arrêtée")
    conf = settings()
    ap.add_argument("--chat", default=conf.get("N8N_CHAT_URL"))
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
            with urllib.request.urlopen(req, timeout=args.max_minutes * 60) as r:
                r.read()
                status = r.status
        except urllib.error.HTTPError as e:
            status = f"{e.code} {e.read().decode()[:120]}"
        except (urllib.error.URLError, TimeoutError) as e:
            if "timed out" in str(e) or isinstance(e, TimeoutError):
                status = f"ARRÊTÉE après {args.max_minutes:g} min ({stop_running(conf)} exécution arrêtée dans n8n)"
            else:
                status = f"échec : {e}"
        print(f"{d['id']}  {status}  {time.time() - t0:5.0f} s  {d['texte'][:60]}", flush=True)


if __name__ == "__main__":
    main()
