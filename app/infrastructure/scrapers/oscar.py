import httpx

AJAX_URL = "https://www.scrapethissite.com/pages/ajax-javascript/"


async def scrape_oscar():
    results = []

    async with httpx.AsyncClient(timeout=20) as client:
        # anos disponíveis no site
        for year in range(2010, 2016):
            response = await client.get(
                AJAX_URL,
                params={"ajax": "true", "year": year},
            )

            if response.status_code != 200:
                continue

            data = response.json()

            for movie in data:
                results.append(
                    {
                        "year": year,
                        "title": movie.get("title", "").strip(),
                        "nominations": movie.get("nominations", 0),
                        "awards": movie.get("awards", 0),
                        "best_picture": movie.get("best_picture", False),
                    }
                )

    print(f"Collected {len(results)} oscar films")
    return results
