from datetime import datetime
from urllib.request import urlopen

from bs4 import BeautifulSoup
import feedparser


class WOTD:
    def __init__(self):
        self.wotd = None
        self.definitions = []

    def __iter__(self):
        today = datetime.utcnow().date()
        if self.wotd is None or self.wotd[-1] != today:
            generator = self.get()
            info = next(generator)
            self.wotd = info + (today,)
            yield info
            self.definitions[:] = []
            for definition in generator:
                self.definitions.append(definition)
                yield definition
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
        fun_fact_tag = soup.find_all('small')[-1]
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

        lines.append(fun_fact)
        return "\n\n".join(lines)


wotd = WOTD()

commands = {
    'wotd': wotd.on_wotd,
}

help = {
    'wotd': 'Give the word of the day from Wiktionary',
}
