import asyncio
import httpx


async def fetch_with_retry(client, url, retries=3, delay=1):
    for attempt in range(retries):
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response

        except (httpx.RequestError, httpx.HTTPStatusError):
            if attempt == retries - 1:
                raise

            await asyncio.sleep(delay * (attempt + 1))
