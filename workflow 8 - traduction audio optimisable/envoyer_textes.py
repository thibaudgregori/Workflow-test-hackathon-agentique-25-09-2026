"""Envoie les textes français de textes.jsonl au traducteur audio, un par un (Python 3.9+).

    python3 envoyer_textes.py --a 1          # test de fumée : le premier texte seulement
    python3 envoyer_textes.py                # les 30 textes

Chaque texte : 1 traduction gpt-4o (4 langues), 4 voix Gradium, puis 4 relectures gpt-4o (une par langue).
La réponse du webhook (traductions et notes de relecture) est enregistrée dans out/reponses/TNN.json.
Adresse du webhook lue dans .env.n8n-traduction-v2 (preparer_n8n.py).

GARDE-FOU : dans le modèle 12382, une traduction jugée insuffisante repart vers l'agent de traduction
sans limite (son réglage maxRetries n'est branché nulle part). En pratique la boucle plante au 2e tour
(« No prompt specified ») ; au cas où elle tournerait, au-delà de --max-minutes (3 par défaut) le script
arrête lui-même l'exécution dans n8n et passe au texte suivant.
"""
import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
WF5 = HERE.parent / "workflow 5 - n8n 4553 guerrilla marketing" / ".env.n8n-test"


def env_file(path):
    if not path.exists():
        return {}
    return dict(l.split("=", 1) for l in path.read_text(encoding="utf-8").splitlines() if "=" in l)


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


def resume(answer):
    """« English 9/10, German 8/10 … » à partir de la réponse du webhook."""
    try:
        items = json.loads(answer)
    except ValueError:
        return answer[:120].decode(errors="replace")
    items = items if isinstance(items, list) else [items]
    notes = [f"{(i.get('output') or {}).get('qualityScore', '?')}/10" for i in items]
    return f"{len(items)} relecture(s) : " + ", ".join(notes)


def main():
    ap = argparse.ArgumentParser(description="Envoie les textes au traducteur audio n8n")
    ap.add_argument("--de", type=int, default=1)
    ap.add_argument("--a", type=int, default=30)
    ap.add_argument("--max-minutes", type=float, default=3, help="au-delà, l'exécution est arrêtée")
    conf = {**env_file(WF5), **env_file(HERE / ".env.n8n-traduction-v2")}
    ap.add_argument("--url", default=conf.get("N8N_TRADUCTION_WEBHOOK"))
    args = ap.parse_args()
    if not args.url:
        sys.exit("adresse du webhook inconnue : lancez preparer_n8n.py, ou passez --url")
    textes = [json.loads(l) for l in (HERE / "textes.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    out = HERE / "out" / "reponses"
    out.mkdir(parents=True, exist_ok=True)
    for t in textes[args.de - 1:args.a]:
        req = urllib.request.Request(args.url, data=json.dumps({"text": t["texte"]}).encode(), method="POST",
                                     headers={"Content-Type": "application/json"})
        t0 = time.time()
        try:
            with urllib.request.urlopen(req, timeout=args.max_minutes * 60) as r:
                answer = r.read()
            (out / f"{t['id']}.json").write_bytes(answer)
            status = "200  " + resume(answer)
        except urllib.error.HTTPError as e:
            status = f"{e.code}  {e.read().decode(errors='replace')[:150]}"
        except (urllib.error.URLError, TimeoutError) as e:
            if "timed out" in str(e) or isinstance(e, TimeoutError):
                status = f"ARRÊTÉ après {args.max_minutes:g} min ({stop_running(conf)} exécution arrêtée dans n8n)"
            else:
                status = f"échec : {e}"
        print(f"{t['id']}  {time.time() - t0:5.1f} s  {status}\n     « {t['texte'][:70]}… »", flush=True)


if __name__ == "__main__":
    main()
