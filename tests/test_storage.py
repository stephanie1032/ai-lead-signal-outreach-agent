from src.storage import AuditStore


def test_store_prevents_duplicate_keys(tmp_path):
    store = AuditStore(str(tmp_path / "audit.db"))
    assert not store.exists("acme::maya@example.com")
    store.record("acme::maya@example.com", "Acme", "maya@example.com", 80, "approved", "Hello")
    assert store.exists("acme::maya@example.com")

