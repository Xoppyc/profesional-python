from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ClientCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=120)
    email: str = Field(..., min_length=5, max_length=120)


class ClientResponse(ClientCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class AccountCreate(BaseModel):
    account_number: str = Field(..., min_length=4, max_length=32)
    client_id: int
    initial_balance: float = Field(0.0, ge=0.0)


class AccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    account_number: str
    client_id: int
    balance: float


class AmountRequest(BaseModel):
    amount: float = Field(..., gt=0.0)


class TransferRequest(BaseModel):
    source_account_id: int
    target_account_id: int
    amount: float = Field(..., gt=0.0)


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    account_id: int
    operation: str
    amount: float
    created_at: datetime
