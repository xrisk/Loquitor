import csv
import html
from io import StringIO

from pws import Bing
import wikipedia

def on_search(event, room, client):
    search = Bing.search(event.query)
    messages = []

    format = "> {result[link_text]}, ({result[link]})\n\n{result[link_info]}"

    for result in search['results']:
        messages.append(format.format(result=result))

    event.respond("\n\n\n".join(messages), False)

def on_wiki(event, room, client):
    result = wikipedia.page(event.query)
    event.respond(result.url)

commands = {'search': on_search, 'wiki': on_wiki}
help = {
    'search': 'Search for item on the web (using Bing)',
    'wiki': 'Search for item on Wikipedia',
}
