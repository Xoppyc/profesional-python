# Lab 07 — Робота з базами даних у Python (Варіант 4)

Лабораторна робота №7 курсу «Професійний Python».

## Архітектура Persistence Layer
- **ORM**: Використання `SQLAlchemy` (2.0 declarative mapping) для сутностей банківських клієнтів (`ClientModel`), рахунків (`AccountModel`) та транзакцій (`TransactionModel`).
- **СУБД**: SQLite з перевіркою цілісності на рівні бази (`CHECK (balance >= 0.0)`).
- **Паттерн Repository**: Ізоляція операцій збереження в `ClientRepository`, `AccountRepository` та `TransactionRepository`.
- **DB-API (PEP 249)**: Безпечне виконання параметризованих SQL-запитів (`query_account_raw_db_api`) для запобігання SQL Injection.
- **Транзакційність (ACID)**: Атомарне списання/зарахування коштів у функції `transfer_money` з автоматичним `rollback()` у разі недостатності коштів або помилки.
- **Міграції**: Керування схемою бази даних через `Alembic`.

## Запуск тестів
```bash
pytest -v
```
