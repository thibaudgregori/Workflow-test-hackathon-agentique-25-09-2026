# Workflow 4 — Tri des tickets de support

Un appel `gpt-4o-mini` par ticket, qui rend sa catégorie : `facturation`, `compte`, `technique` ou
`livraison`. C'est le classifieur le plus répandu en entreprise, et le cas d'école de Deadweight : un
modèle payé pour choisir entre quatre mots.

- `generer_tickets.py` → `tickets.jsonl` : 160 tickets réalistes (graine fixe), sans étiquette ;
- `triage.py` : le workflow, un appel par ticket, résultat dans `out/tri.jsonl`.

## Lancer

    python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
    export OPENAI_API_KEY=...                        # jamais dans le code
    export OPENAI_BASE_URL=http://127.0.0.1:8080/v1  # la passerelle Deadweight
    .venv/bin/python triage.py                       # 160 appels, environ 2 minutes, < 0,01 $

Ce que Deadweight en a fait (rapport, preuve, PR) : `docs/retours-tests-workflows.md` dans le repo DeadWeight.
