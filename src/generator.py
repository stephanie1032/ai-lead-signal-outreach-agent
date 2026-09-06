import json
import os

from .models import Opportunity


def template_draft(opportunity: Opportunity) -> str:
    lead = opportunity.lead
    descriptions = {
        "manual_process": "substantial manual work",
        "moderate_manual_work": "recurring manual work",
        "hiring_growth": "rapid team growth",
        "moderate_growth": "continued team growth",
        "recent_funding": "recent funding",
        "stated_automation_pain": "a repetitive workflow",
    }
    signal_text = " and ".join(descriptions[signal] for signal in opportunity.signals[:2])
    return (
        f"Hi {lead.contact_name}, I noticed {lead.company} is showing signs of {signal_text}. "
        f"Teams in {lead.industry} often lose time to repetitive operational work. "
        "I would be interested in comparing notes on where a focused automation could remove the most friction."
    )


def llm_draft(opportunity: Opportunity) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required when --use-llm is enabled")

    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    payload = {
        "company": opportunity.lead.company,
        "contact_name": opportunity.lead.contact_name,
        "industry": opportunity.lead.industry,
        "signals": opportunity.signals,
        "notes": opportunity.lead.notes,
    }
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        instructions=(
            "Write a concise, professional B2B outreach message under 70 words. "
            "Use only the supplied facts, mention one relevant signal, avoid hype, "
            "and end with a low-pressure question. Return only the message."
        ),
        input=json.dumps(payload),
    )
    return response.output_text.strip()


def generate_draft(opportunity: Opportunity, use_llm: bool = False) -> str:
    return llm_draft(opportunity) if use_llm else template_draft(opportunity)
