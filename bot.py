#!/usr/bin/env python

from code import interact
import html
import sys

import chatexchange

import skeleton

class EventMeta(type, chatexchange.events.Event):
    def __new__(self, class_name, bases, attrs):
        print(attrs)
        attrs['type_id'] = class_name
        if '__init__' not in attrs:
            attrs['__init__'] = self._default_init
        return type.__new__(self, class_name, bases, attrs)

    def _default_init(self, data, client):
        chatexchange.events.Event.__init__(self, data, client)
        self.update(data)

class Command(metaclass=EventMeta):
    pass

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
