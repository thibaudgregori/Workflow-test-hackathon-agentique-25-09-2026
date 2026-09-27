"""Prépare un n8n local VIERGE pour ce workflow, en une commande (Python 3.9+, rien à installer).

    export OPENAI_API_KEY=...          # votre clé : elle va dans l'identifiant OpenAI de n8n, nulle part ailleurs
    python3 preparer_n8n.py            # n8n sur http://127.0.0.1:5678, passerelle sur http://127.0.0.1:8080/v1

1. crée le compte propriétaire de test (identifiants générés, écrits dans .env.n8n-test, jamais commités) ;
2. crée une clé d'API n8n (même fichier) ;
3. importe workflow-4553.json ;
4. crée l'identifiant OpenAI : votre clé, Base URL = la passerelle Deadweight, en-tête x-deadweight-app ;
5. le branche sur le nœud « OpenAI Chat Model » et active le workflow ;
6. affiche l'adresse du chat, à passer à envoyer_demandes.py.
"""
import argparse
import http.cookiejar
import json
import os
import secrets
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
SECRETS = HERE / ".env.n8n-test"


class N8n:
    def __init__(self, url):
        self.url = url.rstrip("/")
        self.api_key = None
        self.http = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

    def call(self, method, path, body=None, public_api=False):
        headers = {"Content-Type": "application/json"}
        if public_api:
            headers["X-N8N-API-KEY"] = self.api_key
        req = urllib.request.Request(self.url + path, method=method, headers=headers,
                                     data=json.dumps(body).encode() if body is not None else None)
        try:
            with self.http.open(req, timeout=60) as r:
                text = r.read().decode()
        except urllib.error.HTTPError as e:
            sys.exit(f"erreur n8n {e.code} sur {method} {path} : {e.read().decode()[:300]}")
        except urllib.error.URLError as e:
            sys.exit(f"n8n injoignable sur {self.url} : {e.reason}. Lancez-le d'abord (voir README).")
        return json.loads(text) if text else {}


def main():
    ap = argparse.ArgumentParser(description="Prépare un n8n local vierge pour le workflow 4553")
    ap.add_argument("--n8n", default="http://127.0.0.1:5678")
    ap.add_argument("--passerelle", default="http://127.0.0.1:8080/v1")
    ap.add_argument("--app", default="n8n-4553", help="nom de l'application dans le rapport Deadweight")
    args = ap.parse_args()
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        sys.exit("OPENAI_API_KEY absente : chargez votre clé dans ce terminal d'abord.")

    n8n = N8n(args.n8n)
    email, password = "owner@deadweight.test", "Dw" + secrets.token_hex(8) + "!"
    n8n.call("POST", "/rest/owner/setup", {"email": email, "firstName": "Test", "lastName": "Deadweight",
                                           "password": password})
    n8n.call("POST", "/rest/login", {"emailOrLdapLoginId": email, "password": password})
    scopes = n8n.call("GET", "/rest/api-keys/scopes")["data"]
    created = n8n.call("POST", "/rest/api-keys", {"label": "deadweight", "scopes": scopes, "expiresAt": None})["data"]
    n8n.api_key = created.get("rawApiKey") or created.get("apiKey")
    SECRETS.write_text(f"N8N_URL={n8n.url}\nN8N_TEST_EMAIL={email}\nN8N_TEST_PASSWORD={password}\n"
                       f"N8N_API_KEY={n8n.api_key}\n", encoding="utf-8")
    SECRETS.chmod(0o600)
    print(f"1-2. compte de test et clé d'API n8n créés → {SECRETS.name} (non commité)")

    wf = json.loads((HERE / "workflow-4553.json").read_text(encoding="utf-8"))
    wf.pop("meta", None)
    created_wf = n8n.call("POST", "/api/v1/workflows", wf, public_api=True)
    wid = created_wf["id"]
    print(f"3. workflow importé : {wf['name']} (id {wid})")

    cred = n8n.call("POST", "/api/v1/credentials", public_api=True, body={
        "name": "OpenAI via Deadweight", "type": "openAiApi",
        "data": {"apiKey": key, "url": args.passerelle, "header": True, "headerName": "x-deadweight-app",
                 "headerValue": args.app, "allowedHttpRequestDomains": "all"}})
    print(f"4. identifiant OpenAI créé : Base URL = {args.passerelle}, x-deadweight-app = {args.app}")

    full = n8n.call("GET", f"/api/v1/workflows/{wid}", public_api=True)
    for node in full["nodes"]:
        if node["type"].endswith("lmChatOpenAi"):
            node["credentials"] = {"openAiApi": {"id": cred["id"], "name": cred["name"]}}
    n8n.call("PUT", f"/api/v1/workflows/{wid}", public_api=True,
             body={k: full[k] for k in ("name", "nodes", "connections", "settings")})
    # n8n 2.x : un workflow activé par l'API n'enregistre son webhook qu'après désactivation puis réactivation
    for action in ("activate", "deactivate", "activate"):
        n8n.call("POST", f"/api/v1/workflows/{wid}/{action}", public_api=True)
        time.sleep(1)
    trigger = next(n for n in full["nodes"] if n["type"].endswith("chatTrigger"))
    chat = f"{n8n.url}/webhook/{trigger['webhookId']}/chat"
    with SECRETS.open("a", encoding="utf-8") as f:
        f.write(f"N8N_WORKFLOW_ID={wid}\nN8N_CHAT_URL={chat}\n")
    print(f"5. identifiant branché sur « OpenAI Chat Model », workflow actif\n6. adresse du chat : {chat}")


if __name__ == "__main__":
    main()
