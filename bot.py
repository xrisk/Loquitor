#!/usr/bin/env python

from code import interact
import html
import sys

import chatexchange

import skeleton

class Command(chatexchange.events.MessageEvent):
    type_id = 'bot.Command'
    def __init__(self, data, client):
        chatexchange.events.MessageEvent.__init__(self, data, client)
        self.__dict__.update(data)

skeleton.Events.register('command', Command)

def run_command(event, room, client):
    if event.content == "test":
        room.send_message(":{} That worked!".format(event.message_id))


def _on_message_posted(event, room, client):
    message = html.unescape(event.content)
    if message.startswith(">>"):
        event.data['content'] = message[2:]
        event.data['event_type'] = Command.type_id
        new_event = Command(event.data, client)
        room.emit(new_event, client)

def main(room, username, password, host='stackoverflow.com'):
    client = chatexchange.Client(host, username, password)

    room = skeleton.Room(room, client)

    room.connect('message-posted', _on_message_posted)
    room.connect('command', run_command)

    interact(banner="Welcome to Loquitor!", local=locals())


if __name__ == '__main__':
    _, username, password = sys.argv
    main(1, username, password)
