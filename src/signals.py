from .models import Lead, Opportunity


def evaluate_lead(lead: Lead) -> Opportunity:
    score = 0
    signals = []

    if lead.manual_hours_per_week >= 15:
        score += 35
        signals.append("manual_process")
    elif lead.manual_hours_per_week >= 5:
        score += 20
        signals.append("moderate_manual_work")

    if lead.employee_growth_pct >= 20 or lead.open_roles >= 8:
        score += 25
        signals.append("hiring_growth")
    elif lead.employee_growth_pct >= 10 or lead.open_roles >= 3:
        score += 15
        signals.append("moderate_growth")

    if 0 <= lead.funding_months_ago <= 12:
        score += 25
        signals.append("recent_funding")

    notes = lead.notes.lower()
    if any(word in notes for word in ("spreadsheet", "copy-paste", "manual", "repetitive")):
        score += 15
        signals.append("stated_automation_pain")

    score = min(score, 100)
    priority = "high" if score >= 70 else "medium" if score >= 45 else "low"
    return Opportunity(lead=lead, score=score, priority=priority, signals=signals)

