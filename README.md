# Workflow test — hackathon agentique 25-09-2026

Workflows réels servant de terrain de test.

| Dossier | Source | Snapshot |
| --- | --- | --- |
| `workflow 1 - Miguel short` | [migueltorrezd/shorts-factory](https://github.com/migueltorrezd/shorts-factory) (privé) | commit `34edd0a`, 26/09/2026 |
| `workflow 2 - Recap Gmail` | écrit pour Deadweight | agent de récap Gmail des dernières 24 h, lecture seule |
| `workflow 3 - OpenAI story flow` | exemple officiel [openai-agents-python](https://github.com/openai/openai-agents-python/blob/main/examples/agent_patterns/deterministic.py) (MIT) | 3 agents à la suite : plan, vérification, histoire |
| `workflow 4 - Tri tickets support` | écrit pour Deadweight | un appel `gpt-4o-mini` par ticket de support, 4 catégories |

Les dossiers copiés d'un autre repo le sont sans leur historique git.
Aucun secret n'y est stocké : voir `workflow 1 - Miguel short/docs/SECRETS.md` pour les variables attendues.
