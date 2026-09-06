import logging

from .generator import generate_draft
from .ingestion import load_leads
from .signals import evaluate_lead
from .storage import AuditStore


class OutreachPipeline:
    def __init__(self, database_path: str, minimum_score: int = 45, dry_run: bool = False, use_llm: bool = False):
        self.store = AuditStore(database_path)
        self.minimum_score = minimum_score
        self.dry_run = dry_run
        self.use_llm = use_llm

    def run(self, input_path: str):
        for lead in load_leads(input_path):
            if self.store.exists(lead.unique_key):
                logging.info("Skipping duplicate lead: %s", lead.company)
                continue

            opportunity = evaluate_lead(lead)
            if opportunity.score < self.minimum_score:
                logging.info("Skipping low-score lead: %s (%s)", lead.company, opportunity.score)
                continue

            opportunity.draft = generate_draft(opportunity, self.use_llm)
            print(f"\n{lead.company} | score={opportunity.score} | priority={opportunity.priority}")
            print(f"Signals: {', '.join(opportunity.signals)}")
            print(f"Draft: {opportunity.draft}")

            if self.dry_run:
                status = "dry_run"
            else:
                approved = input("Approve this draft? [y/N]: ").strip().lower() == "y"
                status = "approved" if approved else "rejected"

            self.store.record(
                lead.unique_key, lead.company, lead.contact_email,
                opportunity.score, status, opportunity.draft,
            )
            print(f"Status: {status}")

