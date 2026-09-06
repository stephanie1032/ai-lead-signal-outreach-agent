import csv

from .models import Lead


REQUIRED_FIELDS = {
    "company", "contact_name", "contact_email", "industry",
    "employee_growth_pct", "open_roles", "manual_hours_per_week",
    "funding_months_ago",
}


def load_leads(path: str) -> list[Lead]:
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED_FIELDS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

        leads = []
        for row_number, row in enumerate(reader, start=2):
            try:
                email = row["contact_email"].strip()
                if "@" not in email:
                    raise ValueError("invalid email")
                leads.append(Lead(
                    company=row["company"].strip(),
                    contact_name=row["contact_name"].strip(),
                    contact_email=email,
                    industry=row["industry"].strip(),
                    employee_growth_pct=float(row["employee_growth_pct"]),
                    open_roles=int(row["open_roles"]),
                    manual_hours_per_week=float(row["manual_hours_per_week"]),
                    funding_months_ago=int(row["funding_months_ago"]),
                    notes=row.get("notes", "").strip(),
                ))
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Invalid lead on CSV row {row_number}: {exc}") from exc
    return leads

