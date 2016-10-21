from collections import defaultdict
import html
import os.path
import random
import sys
from warnings import warn


class main:
    PATH = os.path.join(os.path.dirname(__file__), 'SUBSTITUTIONS.txt')
    VALUES = 0
    ALIAS = 1
    def __init__(self, room=None, bot=None, client=None, path=PATH):
        self.bot = bot
        self.subs = defaultdict(list)
        self.aliases = defaultdict(list)
        if path is not None:
            try:
                self.add(path)
            except IOError:
                warn("Could not open substitutions file.")
                try:
                    with open(path, 'w'):
                        warn("New file successfully created.")
                except IOError:
                    warn("Could not create substitutions file.")

        room.connect("message-posted", self.on_message_posted)


    def add(self, path):
        key = None
        alias = None
        current = self.VALUES
        with open(path) as infile:
            for line in infile:
                line = line.strip()
                if not line:
                    continue
                if line.lower().startswith("##define"):
                    new_key = line.partition(' ')[-1]
                    if new_key.strip():
                        key = new_key
                        alias = key
                        current = self.VALUES
                    else:
                        warn("Invalid key name: {}".format(new_key))
                elif line.lower().startswith("##alias"):
                    _, _, new_alias = line.partition(' ')
                    if new_alias.strip():
                        alias = new_alias
                    else:
                        alias = key
                    current = self.ALIAS
                elif current is self.VALUES:
                    self.subs[key].append(line)
                elif current is self.ALIAS:
                    self.aliases[line].append(alias)


    def get_keys(self, key):
        if key in self.subs:
            yield key
        if key in self.aliases:
            for key in self.aliases[key]:
                yield from self.get_keys(key)

    def get_random(self, key):
        choices = []
        for key in self.get_keys(key):
            choices += self.subs[key]

        return random.choice(choices)

    def on_message_posted(self, event, room, client):
        bot = sys.modules[self.bot.__module__]
        message = bot.remove_ctrl_chars(html.unescape(event.content))

        first_word = message.partition(' ')[0]
        used = set()
        for key in (message, first_word, message.lower(), first_word.lower()):
            if key in used:
                continue
            try:
                room.send_message(self.get_random(key))
                break
            except IndexError:
                used.add(key)
