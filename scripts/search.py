import csv
import html
from io import StringIO

from bs4 import BeautifulSoup
import requests
from pws import Bing
from urllib.parse import quote_plus

def on_search(event, room, client):
    search = Bing.search(event.query)
    messages = []

    format = "> {result[link_text]}, ({result[link]})\n\n{result[link_info]}"

    for result in search['results']:
        messages.append(format.format(result=result))

    event.respond("\n\n\n".join(messages), False)

def on_wiki(event, room, client):
    url = "https://en.wikipedia.org/w/index.php?search={}".format(quote_plus(event.query))
    r = requests.get(url)
    if r.url.startswith("https://en.wikipedia.org/wiki"):
        event.respond(r.url)
    else:
        page = BeautifulSoup(r.text)
        first_result = page.find("div", {'class': 'mw-search-result-heading'})
        link = first_result.find('a')
        event.respond('https://en.wikipedia.org{}'.format(link['href']))

commands = {'search': on_search, 'wiki': on_wiki}
help = {
    'search': 'Search for item on the web (using Bing)',
    'wiki': 'Search for item on Wikipedia',
}
