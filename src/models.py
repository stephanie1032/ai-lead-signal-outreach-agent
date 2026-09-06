from dataclasses import dataclass, field


@dataclass(frozen=True)
class Lead:
    company: str
    contact_name: str
    contact_email: str
    industry: str
    employee_growth_pct: float
    open_roles: int
    manual_hours_per_week: float
    funding_months_ago: int
    notes: str = ""

    @property
    def unique_key(self) -> str:
        return f"{self.company.strip().lower()}::{self.contact_email.strip().lower()}"


@dataclass
class Opportunity:
    lead: Lead
    score: int
    priority: str
    signals: list[str] = field(default_factory=list)
    draft: str = ""

