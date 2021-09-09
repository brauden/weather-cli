from weather_cli import get_weather, get_wiki_article


city = "Almaty"


def test_get_weather():
    testing_result = get_weather(city)
    assert type(testing_result) == tuple, f"Wrong type. Expected tuple, got {type(testing_result)}"
    assert len(testing_result) == 4, f"Wrong length. Expected 4, got {len(testing_result)}"
    assert all(x is not None for x in testing_result), f"Got none"


def test_get_wiki_article():
    assert type(get_wiki_article(city)) == str
    assert len(get_wiki_article(city)) > 0
    assert get_wiki_article(city, True) == ""
