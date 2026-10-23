from __future__ import annotations

import os


def get_payment_mode() -> str:
    return os.getenv("PAYMENT_MODE", "sandbox")
