import click
import textwrap
import requests
import wikipediaapi
from bs4 import BeautifulSoup

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help', 'help'])

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
headers = {
    'User-Agent': user_agent}


def get_weather(city_name: str) -> tuple:
    city = city_name.replace(" ", "+")
    request_string1 = f"https://www.google.com/search?q=weather+{city}&oq=weather+{city}"
    request_string2 = "&aqs=chrome.0.69i59j0i512l9.4791j1j7&sourceid=chrome&ie=UTF-8'"
    res = requests.get(request_string1 + request_string2, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    location = soup.select('#wob_loc')[0].getText().strip()
    time = soup.select('#wob_dts')[0].getText().strip()
    info = soup.select('#wob_dc')[0].getText().strip()
    weather = soup.select('#wob_tm')[0].getText().strip()
    celsius = round((int(weather) - 32) * 5 / 9, 1)
    return location, time, info, weather + "°F" + ", " + str(celsius) + "°C"


def get_wiki_article(city_name: str, ignore_article: bool = False) -> str:

    if ignore_article:
        return ""
    else:
        wiki_wiki = wikipediaapi.Wikipedia('en')
        page = wiki_wiki.page(city_name)
        return page.summary


def text_representation(weather: tuple, article: str, ignore_article: bool = False):
    print()
    print("*" * 100)
    print()
    for i, j in zip(("Location:", "Local time:", "Info:", "Temperature:"), weather):
        print(i, j)

    print()
    print("*" * 100)
    if ignore_article:
        print()
    else:
        print()
        print(f"Wikipedia article {weather[0]}:")
        print()
        wrapped_article = textwrap.wrap(article, width=70)
        for i in wrapped_article:
            print(i)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("city_name", type=str)
@click.option('--n', type=bool, default=False)
def main(city_name, n):
    """
    to run cli: python weather_cli {city name}
    if city name consists of several words like New York, type them with underscore:
    New_York_City
    --n 0 will return only weather without a wiki article, by default returns weather and an article
    """
    city = city_name.split("_")
    city = " ".join(c for c in city)
    if n:
        text_representation(get_weather(city), get_wiki_article("New York", True), True)
    else:
        text_representation(get_weather(city), get_wiki_article(city))


if __name__ == '__main__':
    main()
