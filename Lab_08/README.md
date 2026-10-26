# Lab 08 — Мережеве та асинхронне програмування. REST API (Варіант 4)

Лабораторна робота №8 курсу «Професійний Python».

## Архітектура REST API та Асинхронних Сервісів
- **Фреймворк**: `FastAPI` (RESTful routing, status codes, OpenAPI docs).
- **Валідація даних**: `Pydantic` v2 схеми (`ClientCreate`, `AccountCreate`, `AmountPayload`, `TransferPayload`).
- **Ресурси**:
  - `POST /clients` — реєстрація клієнта
  - `POST /accounts` — відкриття рахунку
  - `GET /accounts` — перелік рахунків
  - `GET /accounts/{id}` — перевірка балансу та інформації рахунку
  - `GET /accounts/{id}/transactions` — історія операцій
  - `POST /accounts/{id}/deposit` — внесення коштів
  - `POST /accounts/{id}/withdraw` — зняття коштів (заборона від'ємного залишку)
  - `POST /transfers` — атомарний переказ між рахунками з валідацією достатності коштів
  - `GET /total-funds` — агрегація загальної суми коштів
- **Асинхронний агрегатор**: `AsyncAccountAggregator` на базі `httpx.AsyncClient`, `asyncio.Semaphore` (обмеження одночасних з'єднань), `asyncio.gather` та retry policy з timeout.

## Запуск тестів
```bash
pytest -v
```
