import os.path
import re
from threading import Timer

import feedparser

PATH = os.path.join(os.path.expanduser("~"), ".loquitor")

def get_since(url, last_id=None):
    parser = feedparser.parse(url)
    if last_id is None:
        try:
            return [], parser.entries[0].id
        except IndexError:
            return [], None
    else:
        try:
            index = next(index for index,item in enumerate(parser.entries) if item.id == last_id)
            return parser.entries[:index], parser.entries[0].id
        except (StopIteration, IndexError):
            pass
        try:
            last_id = parser.entries[0].id
        except IndexError:
            pass
        return [], last_id

def recursive_timer(room, url, last_id=None):
    entries, new_id = get_since(url, last_id)

    for entry in entries:
        room.send_message("@zondo: {}".format(entry.link))

    if (new_id is not None) and (new_id != last_id):
        with open(os.path.join(PATH, ".nuel_last_id"), "w") as nuel_id:
            nuel_id.write(str(new_id) + "\n")

    timer = Timer(500, recursive_timer, (room, url, new_id))
    timer.daemon = True
    timer.start()

def main(room, bot, client):
    if room.id != 85048:
        return
    url = "https://stackoverflow.com/feeds/user/5768335"
    with open(os.path.join(PATH, ".nuel_last_id")) as nuel_id:
        last_id = nuel_id.read().strip()

    recursive_timer(room, url, last_id)
    
