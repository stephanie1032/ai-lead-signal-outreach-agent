from src.generator import template_draft
from src.models import Lead, Opportunity


def test_template_uses_contact_and_company():
    lead = Lead("Acme", "Maya", "maya@example.com", "manufacturing", 20, 5, 10, 5)
    draft = template_draft(Opportunity(lead, 70, "high", ["hiring_growth"]))
    assert "Maya" in draft
    assert "Acme" in draft

