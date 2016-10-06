from random import choice

from urllib.request import urlopen
from bs4 import BeautifulSoup

GREETINGS = (
    "Hey, {}. How are you?", "Hello, {}.", "Heyo there, {}!", "{}: Hello.",
    "Howdy, {}.",
)

def greet(room, user_name):
    user_name = "".join(user_name.split())
    greeting = choice(GREETINGS)
    room.send_message(greeting.format("@" + user_name))

def user_entered(event, room, client):
    me = client.get_me().id
    user_id = event.data['user_id']
    if user_id == me:
        return
    room_id = room.room_id

    user = urlopen("https://chat.stackoverflow.com/users/{}".format(user_id))
    soup = BeautifulSoup(user.read())
    room_card = soup.find('div', {'class': 'roomcard', 'id': 'room-{}'.format(room_id)})
    if room_card is None:
        return
    messages_tag = room_card.find('div', {'class': 'room-message-count'})
    message_text = messages_tag['title']
    message_count = int(message_text.partition(' ')[0])

    if not message_count:
        greet(room, event.data['user_name'])

def on_greet(event, room, client, bot):
    for user_name in event.args:
        user_name = user_name.strip(",")
        greet(room, user_name)

def main(room, bot, client):
    room.connect("user-entered", user_entered)
    bot.register(
        "greet", on_greet,
        help="Given a space-separated list of usernames, greet those users."
    )
