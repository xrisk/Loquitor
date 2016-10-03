from collections import defaultdict
from threading import Thread

import chatexchange6 as chatexchange
from chatexchange6 import events

class Events:
    events = {
        'invitation': events.Invitation.type_id,
        'message_deleted': events.MessageDeleted.type_id,
        'message_edited': events.MessageEdited.type_id,
        'message_moved_out': events.MessageMovedOut.type_id,
        'message_posted': events.MessagePosted.type_id,
        'message_reply': events.MessageReply.type_id,
        'message_starred': events.MessageStarred.type_id,
        'message_moved_in': events.MessagedMovedIn.type_id,
        'user_mentioned': events.UserMentioned.type_id,
        'message_flagged': events.MessageFlagged.type_id,
        'moderator_flag': events.ModeratorFlag.type_id,
        'room_name_changed': events.RoomNameChanged.type_id,
        'time_break': events.TimeBreak.type_id,
        'user_entered': events.UserEntered.type_id,
        'user_left': events.UserLeft.type_id,
        'user_merged': events.UserMerged.type_id,
        'user_notification': events.UserNotification.type_id,
        'user_settings_changed': events.UserSettingsChanged.type_id,
        'user_suspended': events.UserSuspended.type_id,
    }

    rooms = []

    @classmethod
    def register(cls, signal_name, event_cls):
        cls.events[signal_name.replace("-", "_")] = event_cls.type_id
        chatexchange.events.register_type(event_cls)
        for room in cls.rooms:
            room._events[event_cls.type_id] = defaultdict(dict)

    def __init__(self):
        raise Exception("Cannot instantiate class")


class Room(chatexchange.rooms.Room):
    def __init__(self, room_id, client):
        chatexchange.rooms.Room.__init__(self, room_id, client)
        Events.rooms.append(self)

        self._connection_id = 0
        self._ids = {}
        self._events = {}
        for type_id in Events.events.values():
            self._events[type_id] = defaultdict(dict)

        self.room_id = room_id
        self.join()
        self.watch_polling(lambda e,c: Thread(target=self.emit, args=(e,c)).start(), 1)


    def emit(self, event, client):
        events = self._events[event.type_id]
        for priority in sorted(events, reverse=True):
            for callback in events[priority].values():
                if callback(event, self, client):
                    return


    def connect(self, event, callback, priority=0):
        id = self._connection_id
        event = event.replace('-', '_')
        try:
            event_type = Events.events[event]
        except KeyError:
            raise ValueError("Unknown event: {!r}".format(event))

        self._events[Events.events[event]][priority][id] = callback
        self._ids[id] = (event, priority)
        self._connection_id += 1
        return id

    def disconnect(self, id):
        event, priority = self._ids.pop(id)
        self._events[Events.events[event]][priority].pop(id)



def quit(*a):
    for room in Events.rooms:
        room.leave()
