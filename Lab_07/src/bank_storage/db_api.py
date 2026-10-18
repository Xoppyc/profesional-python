import sqlite3
from typing import Any, Optional


def query_account_raw_db_api(db_path: str, account_number: str) -> Optional[dict[str, Any]]:
    # DB-API parameterized query prevents SQL injection attacks
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        query = "SELECT id, account_number, balance, client_id FROM accounts WHERE account_number = ?"
        cursor.execute(query, (account_number,))
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id": row[0],
            "account_number": row[1],
            "balance": row[2],
            "client_id": row[3],
        }
    finally:
        conn.close()
