# Workflow 8 — Traduction audio optimisable (d'après n8n 12382), OpenAI + Gradium

Variante du [workflow 7](../workflow%207%20-%20n8n%2012382%20traduction%20audio) : mêmes textes, même traduction,
mêmes voix Gradium. Les deux défauts qui faisaient planter le modèle d'origine sont corrigés, et on y laisse
volontairement deux gaspillages que Deadweight sait repérer et prouver. Le workflow 7 reste la copie fidèle.

    Webhook {"text": …} → Validate French Text → Translation Agent (gpt-4o, les 4 langues d'un coup)
      → Split Translations (1 élément par langue)
      → Choose Voice (gpt-4o : quelle voix pour cette langue ?)        × 4   ← gaspillage 1
      → Attach Voice → Gradium (une voix toutes les 3 s)                × 4
      → Quality Review Agent (gpt-4o : note /10 + oui/non)              × 4   ← gaspillage 2
      → réponse (notes)

Par texte : 9 appels gpt-4o (1 traduction, 4 choix de voix, 4 relectures) et 4 voix Gradium.

## Corrigé par rapport au workflow 7

- le juge recevait « Original French: » **vide** (Split Translations lisait le texte au mauvais endroit) :
  il reçoit maintenant le texte français ;
- plus de boucle « refusé → retraduire » qui plantait à chaque refus : le verdict est rendu tel quel ;
- le juge ne rend plus qu'une note et un oui/non (le commentaire libre n'était lu par personne et faisait
  échouer le format de sortie : 12 textes perdus sur 30 dans le workflow 7).

## Les deux gaspillages laissés exprès

1. **Choose Voice** : gpt-4o reçoit `Language: Spanish` et doit répondre `Vera`. La langue est déjà connue,
   une table suffit. Deadweight : « une IA qui répond toujours la même chose » (4 réponses possibles), règles
   extraites et **prouvées par rejeu** sur l'historique, puis micro-PR (`deadweight/preuves/` +
   `GATEWAY_SHORTCIRCUIT`) : une fois acceptée, la passerelle répond à la place de gpt-4o.
   Vérifié hors ligne sur les vraies traductions du workflow 7 : 100 % d'accord sur 72 appels rejoués.
2. **Quality Review Agent** : gpt-4o pour rendre `{"qualityScore": 9, "passesQuality": true}`, une fois par
   langue. Deadweight : « modèle haut de gamme pour une tâche simple » ; un modèle moins cher se teste au
   banc (`BANC=oui`, appels payants).

## Lancer

    # A — Deadweight :  GATEWAY_DB=out/wf8.db make dev     (repo DeadWeight, à jour de main)
    # C — n8n local du workflow 5 : N8N_USER_FOLDER=~/n8n-deadweight npx -y n8n@latest start
    # B — ce dossier :
    read -s OPENAI_API_KEY && export OPENAI_API_KEY
    read -s GRADIUM_API_KEY && export GRADIUM_API_KEY
    python3 preparer_n8n.py
    python3 envoyer_textes.py --a 1      # test de fumée
    python3 envoyer_textes.py            # les 30 textes (environ 15 min)

    # analyse, puis micro-PR préparée sur ce dépôt
    cd ~/Desktop/DeadWeight-optimiser && GATEWAY_DB=out/wf8.db make optimiser OPTIM_OUT=out/wf8 \
        REPO=~/Desktop/Workflow-test-hackathon-agentique-25-09-2026

Coût estimé : environ 0,35 $ de gpt-4o pour les 30 textes, plus 120 synthèses Gradium courtes.
