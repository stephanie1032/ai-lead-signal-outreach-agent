# AI Lead Signal & Outreach Agent

A practical sales-engineering project that turns structured company data into prioritized outreach opportunities. The agent detects business signals, assigns a transparent score, drafts a personalized message, requires human approval, and records every decision so the same lead is not contacted twice.

## Why I built it

Sales teams often spend time reviewing scattered lead information and writing repetitive outreach. This project shows how an AI-assisted workflow can reduce that manual work while keeping a person in control of what gets sent.

## What it does

- Reads lead and company data from CSV
- Detects signals such as hiring growth, manual-work pain, and recent funding
- Scores and prioritizes opportunities using explainable rules
- Creates personalized outreach with either an OpenAI model or an offline template
- Requires explicit human approval before marking a message ready to send
- Prevents duplicate outreach with a local SQLite audit log
- Validates required fields and records skipped, rejected, and approved leads
- Supports `--dry-run` for safe demonstrations

## Architecture

```text
CSV leads -> validation -> signal detection -> lead scoring -> message draft
                                                        -> human approval
                                                        -> SQLite audit log
```

The scoring layer is intentionally deterministic and explainable. Generative AI is used only for drafting, and the workflow falls back to a local template when no API key is available.

## Technology

Python, OpenAI API, REST/JSON concepts, SQLite, CSV, pytest, environment variables, logging, and Git/GitHub.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py --input data/sample_leads.csv --dry-run
```

The demo works without an API key. To use model-generated drafts, add an API key to `.env` and run with `--use-llm`.

```bash
python main.py --input data/sample_leads.csv --use-llm
```

No message is actually emailed by this project. Approval means the draft is recorded as ready for a downstream CRM or email integration.

## Example output

```text
Acme Manufacturing | score=85 | priority=high
Signals: hiring_growth, manual_process, recent_funding
Draft: Hi Maya, I noticed Acme is expanding its operations team...
Status: dry_run
```

## Tests

```bash
pytest -q
```

The tests cover validation, signal detection, scoring, duplicate prevention, and the offline message generator.

## Design decisions

- **Human-in-the-loop:** a user reviews every draft before it is approved.
- **Explainability:** each score includes the signals that contributed to it.
- **Idempotency:** a unique lead key prevents accidental duplicate outreach.
- **Safe configuration:** secrets belong in `.env`, which is excluded from Git.
- **Offline demo:** reviewers can run the project without paid services.

## Possible extensions

- Connect approved drafts to HubSpot or another CRM
- Add an email provider with rate limiting and retry handling
- Replace CSV ingestion with a live enrichment API
- Track replies and use outcomes to recalibrate signal weights
- Add a web dashboard for reviewing and approving drafts

## Author

Stephanie Nworgu  
[GitHub](https://github.com/stephanie1032) | [LinkedIn](https://www.linkedin.com/in/stephanie-nworgu-79a847255)

