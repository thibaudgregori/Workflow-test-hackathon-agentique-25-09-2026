# Workflow test — hackathon agentique 25-09-2026

Workflows réels servant de terrain de test.

| Dossier | Source | Snapshot |
| --- | --- | --- |
| `workflow 1 - Miguel short` | [migueltorrezd/shorts-factory](https://github.com/migueltorrezd/shorts-factory) (privé) | commit `34edd0a`, 26/09/2026 |
| `workflow 2 - Recap Gmail` | écrit pour Deadweight | agent de récap Gmail des dernières 24 h, lecture seule |
| `workflow 3 - OpenAI story flow` | exemple officiel [openai-agents-python](https://github.com/openai/openai-agents-python/blob/main/examples/agent_patterns/deterministic.py) (MIT) | 3 agents à la suite : plan, vérification, histoire |
| `workflow 4 - Tri tickets support` | écrit pour Deadweight | un appel `gpt-4o-mini` par ticket de support, 4 catégories |
| `workflow 5 - n8n 4553 guerrilla marketing` | workflow n8n officiel [4553](https://n8n.io/workflows/4553) | 18 agents `gpt-4.1-mini` qui s'enchaînent toujours dans le même ordre |
| `workflow 6 - n8n 2405 assistant vocal` | workflow n8n officiel [2405](https://n8n.io/workflows/2405), adapté OpenAI + Gradium | assistant vocal avec mémoire : Whisper → gpt-4o-mini → Gradium |
| `workflow 7 - n8n 12382 traduction audio` | workflow n8n officiel [12382](https://n8n.io/workflows/12382), adapté OpenAI + Gradium | texte français → 4 langues (gpt-4o), voix Gradium, relecture gpt-4o par langue |

Les dossiers copiés d'un autre repo le sont sans leur historique git.
Aucun secret n'y est stocké : voir `workflow 1 - Miguel short/docs/SECRETS.md` pour les variables attendues.
