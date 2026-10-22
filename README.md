# Bank Account Service — Lab 10 (Variant 4)

Production-ready Bank Account REST API and Double-Entry Transfer System, packaged as `bank-account-service`.

## Features
- **Client & Account Management**: Register clients, create savings/checking accounts with initial balances.
- **Deposit & Withdrawal**: Validated financial operations strictly enforcing non-negative balances.
- **Atomic Transfers**: Double-entry bookkeeping transfers between accounts with automatic rollback upon failure.
- **Transaction Ledger**: Complete audit logging of all deposits, withdrawals, and transfers.
- **Docker & CI/CD**: Multi-stage lightweight containerization and automated GitHub Actions verification.

## Local Installation & Run
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn bank_account_service.api:app --reload
```

Interactive API documentation available at `http://127.0.0.1:8000/docs`.

## Docker Run
```bash
docker build -t bank-account-service:latest .
docker run -p 8000:8000 bank-account-service:latest
```

## API Specification
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Healthcheck endpoint |
| `POST` | `/clients` | Create new client |
| `POST` | `/accounts` | Create account for client |
| `GET` | `/accounts/{id}` | Retrieve account details |
| `GET` | `/accounts/{id}/transactions` | Account transaction history |
| `POST` | `/accounts/{id}/deposit` | Deposit funds |
| `POST` | `/accounts/{id}/withdraw` | Withdraw funds |
| `POST` | `/transfers` | Transfer funds atomically between accounts |
