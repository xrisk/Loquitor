from random import choice
from re import findall
from string import punctuation

from urllib.request import urlopen
from bs4 import BeautifulSoup

GREETINGS = (
    "Hey, {}. How are you?", "Hello, {}.", "Heyo there, {}!", "{}: Hello.",
    "Howdy, {}.",
)

INVALID_USER = [char for char in punctuation if char not in "'-"]

def on_say(event, room, client, bot):
    query = event.query


def greet(room, user_name):
    user_name = "".join([char for char in user_name if char not in INVALID_USER])
    additional = "I am a bot. For a list of my commands, type `>>help`."
    greeting = " ".join([choice(GREETINGS), additional])
    room.send_message(greeting.format("@" + user_name))


def on_greet(event, room, client, bot):
    for user_name in event.args:
        if user_name == 'me':
            user_name = event.user_name
        else:
            user_name = user_name.strip(",")
        greet(room, user_name)

commands = {"greet": on_greet}
help = {
    'greet': "Given a space-separated list of usernames, greet those users."
}
