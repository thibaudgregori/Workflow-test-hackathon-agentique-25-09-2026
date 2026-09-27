# Workflow 6 — Assistant vocal (n8n 2405), OpenAI + Gradium

Modèle n8n [2405](https://n8n.io/workflows/2405) « AI voice chat using webhook, Memory Manager, OpenAI,
Google Gemini & ElevenLabs » (40 000+ vues), adapté à OpenAI + Gradium.

On envoie un message vocal, on reçoit une réponse vocale, avec la mémoire de la conversation :

    Webhook (audio) → OpenAI Whisper (voix → texte) → Get Chat + Aggregate (historique)
      → Basic LLM Chain + gpt-4o-mini (réponse) → Insert Chat (mémoire) → Limit
      → Gradium (texte → voix, voix « Apolline ») → réponse audio

**Deux changements seulement** par rapport au modèle : Google Gemini → OpenAI `gpt-4o-mini` ;
ElevenLabs → Gradium (API REST `POST https://api.gradium.ai/api/post/speech/tts`, en-tête `x-api-key`).

## Fichiers

- `workflow-2405-openai-gradium.json` : le workflow, **sans identifiants** ;
- `questions/` : 10 questions vocales en français (`say` du Mac), une conversation qui fait appel à la mémoire ;
- `preparer_n8n.py` : installe le workflow dans le n8n local du workflow 5, avec vos clés OpenAI et Gradium
  prises dans le terminal (jamais écrites dans ce dossier) ;
- `envoyer_questions.py` : envoie les questions dans l'ordre, enregistre les réponses vocales dans `out/reponses/`.

## Lancer

    # A — Deadweight :  GATEWAY_DB=out/wf6.db make dev     (repo DeadWeight)
    # C — n8n local du workflow 5 : N8N_USER_FOLDER=~/n8n-deadweight npx -y n8n@latest start
    # B — ce dossier :
    read -s OPENAI_API_KEY && export OPENAI_API_KEY
    read -s GRADIUM_API_KEY && export GRADIUM_API_KEY
    python3 preparer_n8n.py
    python3 envoyer_questions.py --a 1      # test de fumée, puis : afplay out/reponses/r01.wav
    python3 envoyer_questions.py            # les 10 questions

## À savoir

- Deadweight ne voit que les appels au **modèle de langage** (`gpt-4o-mini`). La transcription (Whisper,
  relayée sans capture) et la voix (Gradium, en direct) ne sont pas dans son rapport.
- Défaut du modèle d'origine : la mémoire utilise une **clé de session fixe** (`test-0dacb3b5…`) :
  tous les utilisateurs partagent la même conversation.
