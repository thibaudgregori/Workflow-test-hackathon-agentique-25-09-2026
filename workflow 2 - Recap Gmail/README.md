# Workflow 2 — Récap Gmail des dernières 24 h

Un agent lit les mails reçus depuis 24 h et rédige un récap : ce qui est à traiter
en priorité, ce qui mérite d'être lu, et le reste.

1. **Lecture** des mails en IMAP, **en lecture seule** : rien n'est marqué comme lu,
   rien n'est modifié ni supprimé.
2. **Tri** : un appel de modèle par mail, parmi `urgent`, `a_traiter`, `info`,
   `newsletter`, `spam`.
3. **Récap** : un agent reçoit la liste, ouvre avec l'outil `read_email` les mails
   qui en valent la peine, puis écrit le récap (affiché et enregistré dans `out/`).

Pour Deadweight, c'est un terrain de test réel : le tri répète la même tâche avec
cinq réponses possibles (la règle « une IA qui répond toujours la même chose » doit
le voir), l'agent de récap fait un vrai travail (il ne doit pas être signalé).

## Installation (5 minutes)

**1. Mot de passe d'application Gmail** — pas ton vrai mot de passe :

- la validation en deux étapes doit être active sur le compte Google ;
- ouvre https://myaccount.google.com/apppasswords, crée un mot de passe nommé
  « recap », copie les 16 caractères affichés.

IMAP est activé par défaut sur Gmail. Sinon : Gmail → Paramètres → Transfert et
POP/IMAP → Activer IMAP.

**2. Secrets** — dans ce dossier :

    cp .env.example .env.local

puis ouvre `.env.local` et remplis `GMAIL_ADDRESS`, `GMAIL_APP_PASSWORD` et
`OPENAI_API_KEY`. Ce fichier n'est jamais commité (`.gitignore` à la racine).

**3. Dépendance** :

    python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

## Lancer

Par défaut, les appels passent par la passerelle Deadweight : lance-la d'abord
(`make dev` dans le repo DeadWeight, écoute sur `http://127.0.0.1:8080`).

    .venv/bin/python recap.py --demo   # 12 mails d'exemple, sans toucher à Gmail
    .venv/bin/python recap.py          # ta vraie boîte

Pour appeler OpenAI en direct, sans passerelle : `OPENAI_BASE_URL=https://api.openai.com/v1`
dans `.env.local`.

Coût indicatif avec `gpt-4o-mini` : moins d'un centime pour 50 mails.

## Ce qu'il faut savoir

- **Le contenu des mails part chez OpenAI** (expéditeur, objet, texte), et, si la
  passerelle tourne, il est aussi enregistré localement dans sa base SQLite. Ne pas
  lancer sur une boîte dont le contenu ne doit pas sortir.
- **Un mail peut essayer de donner des ordres à l'IA** (« ignore tes consignes… »).
  Les consignes disent de traiter les mails comme des données, et l'agent n'a qu'un
  outil en lecture : au pire, un récap trompeur, jamais une action. Le jeu de démo
  contient un tel mail (n° 10) pour le vérifier.
- Au plus 100 mails, 4 000 caractères par mail, 15 étapes d'agent.
- Les récaps (`out/`) contiennent le contenu des mails : ils ne sont pas commités.
