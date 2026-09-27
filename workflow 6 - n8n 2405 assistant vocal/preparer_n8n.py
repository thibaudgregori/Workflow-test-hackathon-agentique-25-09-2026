"""Installe l'assistant vocal dans le n8n local déjà préparé pour le workflow 5 (Python 3.9+).

    read -s OPENAI_API_KEY && export OPENAI_API_KEY      # votre clé OpenAI
    read -s GRADIUM_API_KEY && export GRADIUM_API_KEY    # votre clé Gradium
    python3 preparer_n8n.py

Réutilise l'adresse et la clé d'API n8n de ../workflow 5 …/.env.n8n-test (ou N8N_URL et N8N_API_KEY).
1. identifiant OpenAI : votre clé, Base URL = la passerelle Deadweight, en-tête x-deadweight-app ;
2. identifiant Gradium : en-tête x-api-key = votre clé (Gradium ne passe pas par Deadweight) ;
3. import de workflow-2405-openai-gradium.json, identifiants branchés, activation ;
4. écrit .env.n8n-voice (identifiants du workflow et adresse du webhook, jamais commité).
Vos clés ne sont écrites que dans n8n : ni dans ce dossier, ni dans la sortie.
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
WF5 = HERE.parent / "workflow 5 - n8n 4553 guerrilla marketing" / ".env.n8n-test"
OUT = HERE / ".env.n8n-voice"


def env_file(path):
    if not path.exists():
        return {}
    return dict(l.split("=", 1) for l in path.read_text(encoding="utf-8").splitlines() if "=" in l)


def main():
    ap = argparse.ArgumentParser(description="Installe l'assistant vocal 2405 (OpenAI + Gradium) dans n8n")
    ap.add_argument("--passerelle", default="http://127.0.0.1:8080/v1")
    ap.add_argument("--app", default="n8n-voice", help="nom de l'application dans le rapport Deadweight")
    args = ap.parse_args()
    conf = env_file(WF5)
    url = (os.environ.get("N8N_URL") or conf.get("N8N_URL") or "http://127.0.0.1:5678").rstrip("/")
    api_key = os.environ.get("N8N_API_KEY") or conf.get("N8N_API_KEY")
    missing = [n for n, v in (("OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY")),
                              ("GRADIUM_API_KEY", os.environ.get("GRADIUM_API_KEY")),
                              ("clé d'API n8n (workflow 5 ou N8N_API_KEY)", api_key)) if not v]
    if missing:
        sys.exit("manquant : " + ", ".join(missing))
    if OUT.exists():
        sys.exit(f"déjà fait : voir {OUT.name}. Pour recommencer, supprimez-le.")

    def call(method, path, body=None):
        req = urllib.request.Request(url + "/api/v1" + path, method=method,
                                     data=json.dumps(body).encode() if body is not None else None,
                                     headers={"Content-Type": "application/json", "X-N8N-API-KEY": api_key})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                text = r.read().decode()
        except urllib.error.HTTPError as e:
            sys.exit(f"erreur n8n {e.code} sur {method} {path} : {e.read().decode()[:300]}")
        except urllib.error.URLError as e:
            sys.exit(f"n8n injoignable sur {url} : {e.reason}")
        return json.loads(text) if text else {}

    openai = call("POST", "/credentials", {"name": f"OpenAI via Deadweight ({args.app})", "type": "openAiApi", "data": {
        "apiKey": os.environ["OPENAI_API_KEY"], "url": args.passerelle, "header": True,
        "headerName": "x-deadweight-app", "headerValue": args.app, "allowedHttpRequestDomains": "all"}})
    print(f"1. identifiant OpenAI : Base URL = {args.passerelle}, x-deadweight-app = {args.app}")
    gradium = call("POST", "/credentials", {"name": "Gradium", "type": "httpHeaderAuth",
                                             "data": {"name": "x-api-key", "value": os.environ["GRADIUM_API_KEY"]}})
    print("2. identifiant Gradium : en-tête x-api-key")

    wf = json.loads((HERE / "workflow-2405-openai-gradium.json").read_text(encoding="utf-8"))
    wf.pop("meta", None)
    for node in wf["nodes"]:
        if node["type"].endswith((".openAi", "lmChatOpenAi")):
            node["credentials"] = {"openAiApi": {"id": openai["id"], "name": openai["name"]}}
        if node["name"].startswith("Gradium"):
            node["credentials"] = {"httpHeaderAuth": {"id": gradium["id"], "name": gradium["name"]}}
    wid = call("POST", "/workflows", wf)["id"]
    # n8n 2.x : un workflow activé par l'API n'enregistre son webhook qu'après désactivation puis réactivation
    for action in ("activate", "deactivate", "activate"):
        call("POST", f"/workflows/{wid}/{action}")
        time.sleep(1)
    path = next(n for n in wf["nodes"] if n["type"].endswith(".webhook"))["parameters"]["path"]
    webhook = f"{url}/webhook/{path}"
    OUT.write_text(f"N8N_URL={url}\nN8N_WORKFLOW_ID={wid}\nN8N_VOICE_WEBHOOK={webhook}\n", encoding="utf-8")
    OUT.chmod(0o600)
    print(f"3. workflow importé et actif : {wf['name']} (id {wid})\n4. adresse du webhook : {webhook}")


if __name__ == "__main__":
    main()
