# Workflow 5 — n8n 4553 : essaim de 18 agents marketing

Workflow n8n officiel [4553](https://n8n.io/workflows/4553), « Generate guerrilla marketing campaign
plans with AI swarm intelligence ». Demande de test : issue #3.

Pour chaque description de projet envoyée dans le chat :
1. **Idea Generator** puis **Market Analyst**, puis un **Information Extractor** qui répond « idée
   acceptée : oui / non » ; si non, retour à l'Idea Generator (boucle) ;
2. si oui, **16 agents** rédigent chacun une section du plan (introduction, objectifs, persona,
   budget, KPIs, risques…) à partir de la même idée ;
3. fusion en `marketing_plan.md`.

Tous les agents partagent un seul nœud « OpenAI Chat Model », `gpt-4.1-mini` : environ **19 appels par
demande**.

## Fichiers

- `workflow-4553.json` : le workflow, **sans identifiants**. Seul changement : le déclencheur de chat
  est ouvert (`public`, mode webhook) pour recevoir les demandes depuis le terminal.
- `demandes.jsonl` : 30 descriptions de projets variées (secteurs, villes, budgets).
- `preparer_n8n.py` : configure un n8n local vierge en une commande (compte de test, clé d'API n8n,
  import, identifiant OpenAI pointé sur la passerelle Deadweight, activation). Identifiants de test dans
  `.env.n8n-test`, jamais commité.
- `envoyer_demandes.py` : envoie les demandes au chat, une par une.

## Lancer (trois terminaux)

    # A — Deadweight (repo DeadWeight)
    GATEWAY_DB=out/wf5.db make dev

    # C — n8n local vierge
    N8N_USER_FOLDER=~/n8n-deadweight npx -y n8n@latest start

    # B — ce dossier, avec votre clé chargée dans OPENAI_API_KEY
    python3 preparer_n8n.py
    python3 envoyer_demandes.py --de 1 --a 1     # test de fumée
    python3 envoyer_demandes.py --de 1 --a 15    # session 1
    python3 envoyer_demandes.py --de 16 --a 30   # session 2, au moins 2 h plus tard

## Résultats

À compléter : version de n8n, appels capturés, coût réel, ce que dit le rapport Deadweight.
