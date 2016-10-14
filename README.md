# Loquitor
A chatbot for Stack Exchange

## Commands

A command is given to the bot by prepending a chat message with `>>`.  Those commands are as follows:

* `define QUERY`: Searches wiktionary.org for the meaning of a word or phrase.
* `greet USER1 [USER2] [USER3] ...`: For each user given, greet that user (no @ is needed when giving the names.)
* `help [CMD]`: Gives help on all commands that implement help (probably everything).  If the name of a command is passed to `help` (without `>>`), it gives help on only that command.
* `pause TIME`: Pause for the specified amount of time.  When the bot is paused, it may respond to messages already posted, but it will not listen for more messages until the time runs out.  Only room owners can run this command.
* `search QUERY`: Gives a list of ten search results from Bing.  Because of the limitations of chat formatting, the results are given like this:

>   \> Speedtest.net - Official Site, (https://speedtest.net)
>
   Test your Internet connection bandwidth to locations around the world with this interactive broadband speed test from Ookla 

* `test`: Responds with a random message taken from a list found [here](https://github.com/ralphembree/Loquitor/blob/master/bot.py#L24).
* `translate`: Translates a word or phrase. If multiple words are given, they should be surrounded with quotation marks.  The source language will be automatically detected, but it can be specified with `from LANG`.  The translated text will be in English unless `to LANG` is specified.
* `whatis`: Tries to find a definition of a word or phrase by searching Google for the phrase with `definition` prepended.  If Google's little custom response is not there, it resorts to the `define` command.
* `wiki`: Searches Wikipedia for a word or phrase.
* `wotd`: Finds the word of the day from Wiktionary.
* `xkcd`: Finds an xkcd comic given an ID or a search term.  Without arguments, gives a random comic.
* `youtube QUERY`: Searches YouTube for a video.  It responds with the first result one-boxed. The `yt` shortcut command can also be used.

## Contributing

Contributions are welcome.  Most of the background code should be done, so probably all that needs to be done is in the [scripts folder](scripts/). A file that is in the scripts folder will automatically be parsed for commands.  If a `main()` function is defined, it will be called when `bot.py` is run.  Otherwise, a `commands` dictionary will be looked for.  The two methods of adding commands are listed below.

### `main()` function

If a command file has a `main()` function, it will be executed, and it will be given these arguments:

    room: The `skeleton.Room` object that represents the room we are in.
    bot: The `bot.Bot` object connected to that room.
    client: The `stackexchange.client.Client` object that represents the account we are using.

The room is an object of type `skeleton.Room`, which is a subclass of `chatexchange.rooms.Room`.  The extra methods provided by `skeleton.Room` are as follows:

* `connect(signal, callback, priority=0)`: Registers a function to be called when a signal is emitted.  The optional priority sets some functions to be called before others (the higher priority is called first).  If a callback returns True, no other callbacks will be called.  The `connect()` method returns an ID that can be used for `disconnect()`.
* `disconnect(callback_id)`: Removes a function from the callback list.  The `callback_id` is the ID returned by `connect()`.
* `emit(event, client)`: Imitates an event.  Given an event and a client, it calls all the callbacks registered for that signal.  This is rarely used except in the background.

This is the only time the `bot` object is passed to a function.  The methods of a `Bot` are as follows:

* `get_help(command, args=())`: Gets help for a command.  If arguments are passed and the command's help is a function, the arguments will be passed to the function.
* `help_command(event, room, client)`: Propably doesn't need to be used.  This is the callback for the `>>help` command.
* `on_message(event, room, client)`: Probably doesn't need to be used.  This is the callback when any message is posted.
* `on_reply(event, room, client)`: Probably doesn't need to be used.  This is the callback when a bot's message is replied to.
* `register(command, function, help=None)`: To register a new command.  The command is passed as a string (without `>>`).  The function is called when that command is executed. (More information [below](#callbacks).)  The optional `help` argument is the string that will be used in the long help or in the help on that particular command.  It is planned to have two help texts
 for these two.  (More on that [below](#todo).)  A function could also be passed for help.  It will be called with whatever arguments are passed to the `help` command`.


### Commands dictionary

The `commands` dictionary is a mapping of commands to functions.  Each function should take three arguments: `room`, `event`, and `client.`  Here is an example:

    from random import choice

    YES_REPLIES = ("Yes.", "Oh, yeah!", "Uh huh.", "Definitely!", "Of course!", "Sure.")
    NO_REPLIES = ("I don't think so.", "No.", "No way!", "Certainly not!", "No, siree.")

    def say_yes_or_no(event, room, client):
        choices = choice([YES_REPLIES, NO_REPLIES])
        event.message.reply(choice(choices))
        
    commands = {
        'yes-or-no': say_yes_or_no, 'yes?': say_yes_or_no, 'no?': say_yes_or_no,
    }

More information about callbacks is given [below](#callbacks).  If a `help` dictionary is given, it can be used for command help:

    help = {
        'yes-or-no': 'Give a random response of yes or no.  yes? and no? are synonymous commands.',
    }

A function could also be used instead of a string.  Commands that do not appear in that `help` dictionary will not appear in the general help, and will reply with `Sorry, I can't help you with that.` if help is asked for that command.  Better help texts are planned [below](#todo).


### Callbacks

A callback is a function that is called when a signal is emitted.  A callback is given three arguments: `event`, `room`, and `client`.  The event is a subclass of `chatexchange.events.Event`. (Command events are subclasses of `bot.Command`).  The `bot.Command` events are just like `chatexchange.events.MessagePosted` events except that they have these three extra attributes (and keys of `event.data`): `command`, `query`, and `args`.  Here is an example:

    >>search Clark Gable "Gone with the Wind"

The event would be of type `Command_search`; `event.command` would be `search`; `event.query` would be `'Clark Gable "Gone with the Wind"'`; and `event.args` would be `['Clark', 'Gable', 'Gone with the Wind']`.  The most commonly-used attribute of an event is `event.message` because it provides `event.message.reply()`.

The `room` is a `skeleton.Room` object, which is a subclass of `chatexchange.rooms.Room`.  More information on that [above](#main-function)

The client is an instance of `chatexchange.client.Client`.


###Todo

#### bot.py

* Separate help texts for main and specific help commands.
* Option to have a different command prompt.
