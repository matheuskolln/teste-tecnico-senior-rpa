import httpx
from bs4 import BeautifulSoup
from app.infrastructure.scrapers.utils import fetch_with_retry

BASE_URL = "https://www.scrapethissite.com/pages/forms/"


def safe_int(value: str, default=0):
    try:
        return int(value.strip())
    except Exception:
        return default


def safe_float(value: str, default=0.0):
    try:
        return float(value.strip())
    except Exception:
        return default


def get_text(row, selector):
    el = row.select_one(selector)
    return el.text.strip() if el else ""


async def scrape_hockey():
    results = []
    page = 1

    async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=5.0)) as client:
        while True:
            url = f"{BASE_URL}?page_num={page}"
            response = await fetch_with_retry(client, url)

            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, "html.parser")
            rows = soup.select("tr.team")

            if not rows:
                break

            for row in rows:
                results.append(
                    {
                        "team_name": get_text(row, ".name"),
                        "year": safe_int(get_text(row, ".year")),
                        "wins": safe_int(get_text(row, ".wins")),
                        "losses": safe_int(get_text(row, ".losses")),
                        "ot_losses": safe_int(get_text(row, ".ot-losses")),
                        "win_pct": safe_float(get_text(row, ".pct")),
                        "goals_for": safe_int(get_text(row, ".gf")),
                        "goals_against": safe_int(get_text(row, ".ga")),
                        "goal_diff": safe_int(get_text(row, ".diff")),
                    }
                )

            page += 1

    print(f"Collected {len(results)} hockey teams from page {page}")
    return results
