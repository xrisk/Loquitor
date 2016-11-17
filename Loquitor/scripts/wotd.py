from datetime import datetime
import pickle
import os.path
from urllib.request import urlopen

from bs4 import BeautifulSoup
import feedparser


class WOTD:
    FILE = os.path.join(os.path.expanduser("~"), ".loquitor", '.wotd')
    def __init__(self):
        self.wotd = None
        self.definitions = []

    def get_wotd_from_file(self):
        try:
            with open(self.FILE, 'rb') as f:
                self.wotd = pickle.load(f)
                self.definitions = pickle.load(f)
        except (IOError, pickle.PickleError, EOFError):
            pass

    def set_wotd_to_file(self):
        # Any errors are passed to the calling function
        with open(self.FILE, 'wb') as f:
            pickle.dump(self.wotd, f)
            pickle.dump(self.definitions, f)

    def __iter__(self):
        today = datetime.utcnow().date()
        if self.wotd is None or self.wotd[-1] != today:
            self.get_wotd_from_file()
        if self.wotd is None or self.wotd[-1] != today:
            generator = self.get()
            info = next(generator)
            self.wotd = info + (today,)
            yield info
            self.definitions[:] = []
            for definition in generator:
                self.definitions.append(definition)
                yield definition
            self.set_wotd_to_file()
        else:
            yield self.wotd[:-1]
            yield from self.definitions

    def on_wotd(self, event, room, client, bot):
        event.message.reply(self.format(), False)

    def get(self):
        feed = feedparser.parse("https://en.wiktionary.org/w/api.php?action=featuredfeed&feed=wotd")
        soup = BeautifulSoup(feed.entries[-1]['summary'])

        span = soup.find('span', {'id': 'WOTD-rss-title'})
        word = span.text
        speech_part = soup.find('i').text
        link = 'https://en.wiktionary.org' + span.parent['href']
        pointer = soup.find('img', alt='PointingHand.svg')
        if pointer is None:
            fun_fact = None
        else:
            fun_fact_tag = pointer.findNext()
            fun_fact = fun_fact_tag.text
            fun_fact_tag.clear()

        yield word, speech_part, link, fun_fact

        definitions = soup.find("ol")
        yield from (definition.text for definition in definitions.find_all("li"))

    def format(self):
        wotd_generator = iter(self)
        word, speech_part, link, fun_fact = next(wotd_generator)
        lines = ["The word of the day is: {} ({}): {}".format(word, speech_part, link)]
        for index, definition in enumerate(wotd_generator, 1):
            lines.append("{}. {}".format(index, definition.replace("\n", "\n\n")))

        if fun_fact:
            lines.append("--> " + fun_fact)

        return "\n\n".join(lines)


wotd = WOTD()

commands = {
    'wotd': wotd.on_wotd,
}

help = {
    'wotd': 'Give the word of the day from Wiktionary',
}
