from datetime import datetime
from urllib.request import urlopen

from bs4 import BeautifulSoup
import feedparser


class WOTD:
    def __init__(self):
        self.wotd = None
        self.definitions = []

    def __iter__(self):
        utcnow = datetime.utcnow().date()
        if self.wotd is None or self.wotd[-1] != utcnow:
            generator = self.get()
            word, link = next(generator)
            self.wotd = (word, link, utcnow)
            yield word, link
            self.definitions[:] = []
            for definition in generator:
                self.definitions.append(definition)
                yield definition
        else:
            yield self.wotd[:2]
            yield from self.definitions

    def on_wotd(self, event, room, client, bot):
        event.message.reply(self.format())

    def get(self):
        feed = feedparser.parse("https://en.wiktionary.org/w/api.php?action=featuredfeed&feed=wotd")
        soup = BeautifulSoup(feed.entries[-1]['summary'])

        span = soup.find('span', {'id': 'WOTD-rss-title'})
        word = span.text
        link = 'https://en.wiktionary.org' + span.parent['href']

        yield word, link

        definitions = soup.find("ol")
        yield from (definition.text for definition in definitions.find_all("li"))

    def format(self):
        wotd_generator = iter(self)
        word, link = next(wotd_generator)
        lines = ["The word of the day is: {} ({})".format(word, link)]
        for index, definition in enumerate(wotd_generator, 1):
            lines.append("{}. {}".format(index, definition.replace("\n", "\n\n")))

        return "\n\n".join(lines)


wotd = WOTD()

commands = {
    'wotd': wotd.on_wotd,
}

help = {
    'wotd': 'Give the word of the day from Wiktionary',
}
