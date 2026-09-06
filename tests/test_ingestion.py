import pytest

from src.ingestion import load_leads


def test_sample_data_loads():
    leads = load_leads("data/sample_leads.csv")
    assert len(leads) == 3
    assert leads[0].company == "Acme Manufacturing"


def test_invalid_email_is_rejected(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text("company,contact_name,contact_email,industry,employee_growth_pct,open_roles,manual_hours_per_week,funding_months_ago\nA,B,invalid,C,1,1,1,1\n")
    with pytest.raises(ValueError, match="invalid email"):
        load_leads(str(path))

