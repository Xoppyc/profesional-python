import asyncio
from typing import Any

import httpx


class AsyncAccountAggregator:
    def __init__(self, base_url: str = "http://testserver", max_concurrency: int = 3) -> None:
        self.base_url = base_url
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def fetch_account_with_retry(
        self, client: httpx.AsyncClient, account_id: int, retries: int = 2
    ) -> dict[str, Any] | None:
        async with self.semaphore:
            for attempt in range(retries + 1):
                try:
                    response = await client.get(
                        f"{self.base_url}/accounts/{account_id}", timeout=5.0
                    )
                    if response.status_code == 200:
                        return response.json()
                except httpx.RequestError:
                    if attempt == retries:
                        return None
                    await asyncio.sleep(0.1 * (attempt + 1))
            return None

    async def fetch_multiple_accounts(
        self, client: httpx.AsyncClient, account_ids: list[int]
    ) -> list[dict[str, Any]]:
        # Run concurrent fetches bounded by Semaphore to avoid socket starvation
        tasks = [self.fetch_account_with_retry(client, acc_id) for acc_id in account_ids]
        results = await asyncio.gather(*tasks)
        return [r for r in results if r is not None]
