# Workflow 7 — Traduction audio multilingue (n8n 12382), OpenAI + Gradium

Modèle n8n [12382](https://n8n.io/workflows/12382) « Translate Chinese text to multilingual audio with GPT-4o
and ElevenLabs », adapté : texte **français** → anglais, allemand, espagnol, portugais, lus par Gradium.

    Webhook {"text": …} → Workflow Configuration → Validate French Text
      → Translation Agent (gpt-4o, 1 appel : les 4 langues d'un coup)
      → Split Translations (1 élément par langue)
      → Gradium (texte → voix, une voix par langue)          × 4
      → Format Audio Response
      → Quality Review Agent (gpt-4o, relecture notée /10)    × 4
      → Check Quality Score : oui → réponse ; non → retour au Translation Agent

Par texte : **5 appels gpt-4o** (1 traduction + 4 relectures) et 4 voix Gradium.

## Changements par rapport au modèle

- chinois → français (validation : texte non vide ; prompts « French ») ; langues cibles = celles de Gradium ;
- ElevenLabs → Gradium (API REST `POST https://api.gradium.ai/api/post/speech/tts`, en-tête `x-api-key`,
  voix Harper / Lorena / Vera / Bianca, réglées dans « Workflow Configuration ») ;
- nœuds OpenAI : **« Use Responses API » désactivé**. En n8n 2.x, le nœud OpenAI Chat Model 1.3 passe par
  défaut par l'API Responses d'OpenAI, que la passerelle Deadweight ne capture pas (problème 11) : sans ce
  réglage, Deadweight ne verrait aucun appel ;
- Gradium : **une voix toutes les 3 s**, connexion fermée après chaque voix, sans nouvel essai. L'offre
  Gradium limite à 2 synthèses simultanées (« Concurrency limit exceeded: 2 active sessions ») et une session
  reste comptée un moment après la réponse. Au premier essai, n8n envoyait les 4 langues en même temps et les
  30 textes ont échoué après avoir payé leur traduction gpt-4o. En passant à une voix à la fois, la 3e restait
  refusée, et le « Retry on fail » de n8n relance tout le nœud, donc repaie les voix déjà faites ;
- webhook en mode « Respond to Webhook node » (le modèle déclarait un nœud de réponse sans l'utiliser).
- `gpt-4o` est **gardé** partout, comme dans le modèle.

## Fichiers

- `workflow-12382-openai-gradium.json` : le workflow, **sans identifiants** ;
- `textes.jsonl` : 30 textes courts d'office de tourisme (Lyon) ;
- `preparer_n8n.py` : installe le workflow dans le n8n local du workflow 5, avec vos clés OpenAI et Gradium
  prises dans le terminal (jamais écrites dans ce dossier) ;
- `envoyer_textes.py` : envoie les textes un par un, réponses dans `out/reponses/`, garde-fou anti-boucle.

## Lancer

    # A — Deadweight :  GATEWAY_DB=out/wf7.db make dev     (repo DeadWeight)
    # C — n8n local du workflow 5 : N8N_USER_FOLDER=~/n8n-deadweight npx -y n8n@latest start
    # B — ce dossier :
    read -s OPENAI_API_KEY && export OPENAI_API_KEY
    read -s GRADIUM_API_KEY && export GRADIUM_API_KEY
    python3 preparer_n8n.py
    python3 envoyer_textes.py --a 1      # test de fumée
    python3 envoyer_textes.py            # les 30 textes

Coût estimé : environ 0,01 $ de gpt-4o par texte (≈ 0,35 $ pour 30), plus 120 synthèses Gradium courtes.

## Défauts du modèle d'origine (à voir si Deadweight les trouve)

- `gpt-4o` pour une traduction courte et pour une note /10 : surdimensionné ;
- une relecture LLM **par langue** (4 appels) au lieu d'une seule pour les 4 ;
- la relecture a lieu **après** la synthèse vocale : une traduction refusée a déjà été payée chez Gradium ;
- boucle « refusé → retraduire » : `maxRetries` n'est jamais utilisé, et l'élément renvoyé n'a plus de
  texte, donc l'exécution plante (« No prompt specified ») : **tout le texte est perdu**, les 5 appels et
  4 voix déjà faits compris ;
- la réponse du webhook ne contient que les notes de relecture : les traductions et l'audio sont perdus
  (visibles seulement dans l'exécution n8n).
- Deadweight ne voit que les appels gpt-4o : Gradium (appel direct) n'est pas dans son rapport.
