import uvicorn
from bank_account_service.api import app


def start() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    start()
