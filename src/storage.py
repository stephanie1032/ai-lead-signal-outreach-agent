import sqlite3
from datetime import datetime, timezone


class AuditStore:
    def __init__(self, path: str):
        self.connection = sqlite3.connect(path)
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS outreach_audit (
                lead_key TEXT PRIMARY KEY,
                company TEXT NOT NULL,
                email TEXT NOT NULL,
                score INTEGER NOT NULL,
                status TEXT NOT NULL,
                draft TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        self.connection.commit()

    def exists(self, lead_key: str) -> bool:
        row = self.connection.execute(
            "SELECT 1 FROM outreach_audit WHERE lead_key = ?", (lead_key,)
        ).fetchone()
        return row is not None

    def record(self, lead_key: str, company: str, email: str, score: int, status: str, draft: str):
        self.connection.execute(
            "INSERT INTO outreach_audit VALUES (?, ?, ?, ?, ?, ?, ?)",
            (lead_key, company, email, score, status, draft, datetime.now(timezone.utc).isoformat()),
        )
        self.connection.commit()

