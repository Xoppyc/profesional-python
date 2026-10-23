from __future__ import annotations

from stream_processor.models import AccountRecord, BankAccountRecord
from stream_processor.pipeline import build_pipeline

__version__ = "0.3.0"
__all__ = ["AccountRecord", "BankAccountRecord", "build_pipeline"]
