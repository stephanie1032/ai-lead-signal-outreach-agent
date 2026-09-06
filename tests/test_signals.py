from src.models import Lead
from src.signals import evaluate_lead


def test_high_priority_lead_has_explainable_signals():
    lead = Lead("Acme", "Maya", "maya@example.com", "manufacturing", 25, 10, 20, 6, "Manual spreadsheet process")
    result = evaluate_lead(lead)
    assert result.score == 100
    assert result.priority == "high"
    assert "manual_process" in result.signals
    assert "recent_funding" in result.signals


def test_low_priority_lead():
    lead = Lead("Small Co", "Alex", "alex@example.com", "design", 2, 0, 1, 36, "")
    result = evaluate_lead(lead)
    assert result.score == 0
    assert result.priority == "low"

