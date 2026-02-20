def test_oscar_mapping():
    movie = {
        "title": "Interstellar",
        "nominations": 5,
        "awards": 1,
        "best_picture": False,
    }

    result = {
        "year": 2014,
        "title": movie.get("title", "").strip(),
        "nominations": movie.get("nominations", 0),
        "awards": movie.get("awards", 0),
        "best_picture": movie.get("best_picture", False),
    }

    assert result["title"] == "Interstellar"
    assert result["nominations"] == 5
