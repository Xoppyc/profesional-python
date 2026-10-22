FROM python:3.12-slim AS builder

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src/ ./src/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir build && \
    python -m build --wheel

FROM python:3.12-slim AS runner

WORKDIR /app
COPY --from=builder /app/dist/*.whl ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir *.whl

EXPOSE 8000
CMD ["uvicorn", "bank_account_service.api:app", "--host", "0.0.0.0", "--port", "8000"]
