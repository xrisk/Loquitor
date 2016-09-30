import csv
import html
from io import StringIO

from pws import Bing

def on_search(event, room, client):
    search = Bing.search(html.unescape(event.query))
    messages = []

    format = "> {result[link_text]}, ({result[link]})\n\n{result[link_info]}"

    for result in search['results']:
        messages.append(format.format(result=result))

    event.respond("\n\n\n".join(messages), False)

commands = {'search': on_search}
help = {'search': 'Search for item on the web (using Bing)'}
