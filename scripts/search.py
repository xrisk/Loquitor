import csv
import html
from io import StringIO
import re

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

WIKI_DEFINE = 'en.wiktionary.org'
WIKI_ENCYCL = 'en.wikipedia.org'
def wiki_find(event, room, client, site=WIKI_ENCYCL):
    url = "https://{}/w/index.php?search={}".format(site, quote_plus(event.query))
    r = requests.get(url)
    if r.url.startswith("https://{}/wiki".format(site)):
        event.respond(r.url)
        return

    page = BeautifulSoup(r.text)

    did_you_mean = page.find('div', {'class': 'searchdidyoumean'})
    if did_you_mean:
        link = did_you_mean.find('a')['href']
        link_regex = '&search=(?P<word>.*?)&'
        word = re.search(link_regex, link).group('word')
        event.query = word
        wiki_find(event, room, client, site)
        return

    first_result = page.find("div", {'class': 'mw-search-result-heading'})
    if first_result:
        link = first_result.find('a')
        event.respond('https://{}{}'.format(site, link['href']))
        return

    event.respond("Sorry, I don't know that word.")

commands = {'search': on_search, 'wiki': wiki_find,
            'define': lambda e,r,c: wiki_find(e,r,c,WIKI_DEFINE)}
help = {
    'search': 'Search for item on the web (using Bing)',
    'wiki': 'Search for item on Wikipedia',
    'define': 'Search for meaning of word (on Wiktionary)',
}
