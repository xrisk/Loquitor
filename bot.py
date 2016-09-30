#!/usr/bin/env python

from code import interact
from getpass import getpass
import html
from random import choice
import shlex
import sys

import chatexchange

import skeleton

class Bot:
    UNKNOWN_MESSAGES = (
        "I don't now what that means.", "Sorry, I don't understand.",
        "Huh?", "What does that mean?", "That isn't in my dictionary.",
        "I don't get what you're trying to say.",
    )
    TEST_MESSAGES = (
        "This is just a test.", "I'm working.", "Hey.",
        "Test yourself, and see how you like it.", "Don't bother me.",
    )
    NUEL_TESTS = (
        "https://chat.stackoverflow.com/transcript/85048?m=33126572#33126572",
        "https://chat.stackoverflow.com/transcript/85048?m=33101025#33101025",
        "https://chat.stackoverflow.com/transcript/85048?m=32915719#32915719",
        "https://chat.stackoverflow.com/transcript/85048?m=32807076#32807076",
        "https://chat.stackoverflow.com/transcript/85048?m=32774161#32774161",
        "https://chat.stackoverflow.com/transcript/85048?m=33149227#33149227",
        "https://chat.stackoverflow.com/transcript/85048?m=32926859#32926859",
        "https://chat.stackoverflow.com/transcript/85048?m=33083381#33083381",
        "https://chat.stackoverflow.com/transcript/85048?m=33083372#33083372",
        "https://chat.stackoverflow.com/transcript/85048?m=33083371#33083371",
        "https://chat.stackoverflow.com/transcript/85048?m=33083332#33083332",
        "https://chat.stackoverflow.com/transcript/85048?m=33079296#33079296",
        "https://chat.stackoverflow.com/transcript/85048?m=33068126#33068126",
        "https://chat.stackoverflow.com/transcript/85048?m=32828808#32828808",
        "https://chat.stackoverflow.com/transcript/85048?m=32774149#32774149",
    )
    def __init__(self, room, client):
        if not client.logged_in:
            raise ValueError("Client must be logged in.")

        self.room = room
        self.client = client

        self.commands = {}

        self.register("test", self.test_command)
        self.room.connect('message-posted', self.on_message)

    def test_command(self, event, room, client):
        if event.data['user_id'] == 5768335:
            message = choice(self.NUEL_TESTS)
        else:
            message = choice(self.TEST_MESSAGES)
        room.send_message(":{} {}".format(event.data['message_id'], message))

    def register(self, command, function):
        signal_name = 'Command_{}'.format(command)
        event_cls = type(signal_name, (Command,), {})
        skeleton.Events.register(signal_name, event_cls)
        self.commands[command] = event_cls
        self.room.connect(signal_name, function)

    def on_message(self, event, room, client):
        message = html.unescape(event.content)
        if message.startswith(">>"):
            message = message[2:]
            command, *args = shlex.split(message)
            event.data['command'] = command
            event.data['args'] = args

            if command in self.commands:
                event.data['event_type'] = 'Command_{}'.format(command)
                new_event = self.commands[command](event.data, client)
                room.emit(new_event, client)

            else:
                message = choice(self.UNKNOWN_MESSAGES)
                m_id = event.data['message_id']
                room.send_message(":{} {}".format(m_id, message))

        

class EventMeta(type, chatexchange.events.Event):
    def __new__(self, class_name, bases, attrs):
        attrs['type_id'] = class_name
        if '__init__' not in attrs:
            attrs['__init__'] = self._default_init

        event_vars = dict(vars(chatexchange.events.Event))
        del event_vars['__init__']
        attrs.update(event_vars)

        return type.__new__(self, class_name, bases, attrs)

    def _default_init(self, data, client):
        chatexchange.events.Event.__init__(self, data, client)
        for key, value in data.items():
            setattr(self, key, value)

class Command(metaclass=EventMeta):
    pass

skeleton.Events.register('command', Command)


def main(room, username, password, host='stackoverflow.com'):
    client = chatexchange.Client(host, username, password)
    room = skeleton.Room(room, client)
    bot = Bot(room, client)

    interact(banner="Welcome to Loquitor!", local=locals())


if __name__ == '__main__':
    username = input("E-mail: ")
    password = getpass("Password: ")
    room = input("What room would you like to join? ")
    while True:
        try:
            room = int(room)
            break
        except ValueError:
            room = input("Please type an integer: ")

    print("Loading...", end='\r')
    main(1, username, password)
