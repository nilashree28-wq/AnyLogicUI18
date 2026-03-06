# Ireland–UK Post-Brexit Simulation Chatbot

Implements the chatbot from [CHATBOT_TRAINING_AND_LLM_DESIGN.md](../CHATBOT_TRAINING_AND_LLM_DESIGN.md): structured context (no fine-tuning), Ireland–UK scope only, answers from completed runs data.

## Setup

1. **Python 3.9+**

2. **Install dependencies** (from project root or from `chatbot/`):
   ```bash
   pip install -r chatbot/requirements.txt
   ```

3. **Data files** in project root:
   - `Post-Brexit Sector Based Model - Completed runs.xlsx` (sheet "Completed runs")
   - `parameter_names_from_completed_runs_updated.csv`

4. **Optional – OpenAI** (for real LLM answers):
   - Create `.env` in project root with `OPENAI_API_KEY=sk-...`
   - Or export: `export OPENAI_API_KEY=sk-...`
   - Without it, the chatbot runs in mock mode (no API calls).

## Run

From **project root**:

```bash
python -m chatbot.chat
```

Example questions:
- *What input parameters do I need for Ireland to UK direct route?*
- *Which parameters control Irish port checks for exports to GB?*
- *What are typical value ranges for trade volumes between Ireland and GB?*

## Layout

- `config.py` – Paths, Excel schema (input cols 0–158, output 159–332), LLM settings
- `data_loader.py` – Load Excel + parameter CSV; filter to Ireland–UK parameters; build context text
- `context_builder.py` – System prompt and user prompt (context + question)
- `llm_client.py` – Call OpenAI (or mock if no API key)
- `chat.py` – CLI loop: load context once, then answer each question

## LLM

- Default model: `gpt-4o-mini` (override with `OPENAI_CHATBOT_MODEL`).
- Prompt: system = “answer only from context”; user = Ireland–UK parameter list + value ranges + user question.
