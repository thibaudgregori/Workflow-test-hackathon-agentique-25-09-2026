# Workflow 3 — OpenAI story flow

L'exemple officiel **`deterministic.py`** du SDK Agents d'OpenAI
([openai/openai-agents-python](https://github.com/openai/openai-agents-python/blob/main/examples/agent_patterns/deterministic.py),
commit `588826c`, licence MIT : `LICENSE-openai-agents`).

Trois agents à la suite, toujours dans le même ordre :

1. `story_outline_agent` écrit un plan d'histoire à partir de la demande ;
2. `outline_checker_agent` juge le plan : `{good_quality, is_scifi}` ;
3. si le plan est bon **et** de science-fiction, `story_agent` écrit l'histoire.
   Sinon, le flux s'arrête.

Le code des agents est celui d'OpenAI. Les changements sont marqués `DEADWEIGHT`
dans `story_flow.py` : appels via la passerelle en `chat/completions`, pas de
traces envoyées à OpenAI, modèle par variable (`gpt-4o-mini` par défaut), demande
en argument, `return` au lieu de `exit(0)`.

## Lancer

    python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
    export OPENAI_API_KEY=...                        # jamais dans le code
    export OPENAI_BASE_URL=http://127.0.0.1:8080/v1  # la passerelle Deadweight
    .venv/bin/python story_flow.py "A sci-fi story about a library on the Moon"
    .venv/bin/python run_many.py                     # les 15 demandes de prompts.txt

`run_many.py` enchaîne les 15 demandes de `prompts.txt` (9 de science-fiction, 6
d'autres genres) : environ 38 appels, 0,01 $ avec `gpt-4o-mini`.

Résultats du test Deadweight : `docs/retours-tests-workflows.md` dans le repo DeadWeight.
