from bs4 import BeautifulSoup
from app.infrastructure.scrapers.hockey import safe_int, safe_float, get_text


def test_safe_int_valid():
    assert safe_int("10") == 10


def test_safe_int_invalid():
    assert safe_int("") == 0


def test_safe_float_valid():
    assert safe_float("0.55") == 0.55


def test_safe_float_invalid():
    assert safe_float("") == 0.0


def test_get_text_missing_element():
    html = "<tr></tr>"
    soup = BeautifulSoup(html, "html.parser")
    row = soup.select_one("tr")

    assert get_text(row, ".name") == ""
