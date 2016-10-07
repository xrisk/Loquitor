from getpass import getpass
import locale
from re import match

from BingTranslator import Translator


class UnknownTokenError(Exception):
    pass

class UnknownLanguageError(Exception):
    def __init__(self, language):
        Exception.__init__(self, language)
        self.language = language

class main:
    def __init__(self, room, bot, client):
        print("If you would like to have the translate command, please give your Bing translation credentials.  If you aren't willing, just hit Enter to skip this feature.")
        client_id = input("Client ID: ")
        if not client_id:
            return
        secret = getpass("Secret: ")
        if not secret:
            return

        self.translator = Translator(client_id, secret)
        bot.register("translate", self.on_translate, help="Translate word/phrase using Bing's translation API.  By default, the source language is guessed, and the target language is English, but you can specify with the `from` and `to` keywords (at the end of the command.)  Multi-word texts should be in quotation marks.")

    def get_from_to(self, words):
        try:
            token, lang = words[-2:]
            if (len(token.split()) > 1) or (len(lang.split()) > 1):
                raise UnknownTokenError
            if token in ("from", "to"):
                lang = self.normalize(lang)
                if not lang:
                    raise UnknownLanguageError(lang)
                return words[:-2], (token, lang)
            else:
                raise UnknownTokenError
        except ValueError as e:
            pass
        return words, None

    def respond_from_to(self, event, words):
        reply = event.message.reply
        try:
            words, result = self.get_from_to(words)
            return words, result
        except UnknownTokenError:
            reply("Only `from` and `to` are allowed keywords.")
        except UnknownLanguageError as e:
            reply("Sorry, I don't understand {!r} is.".format(e.language))
        raise ValueError


    def on_translate(self, event, room, client, bot):
        words = event.args
        keys = {'from': 'from_lang', 'to': 'to_lang'}
        dic = {keys['to']: 'en'}
        try:
            words, result = self.respond_from_to(event, words)
        except ValueError:
            return
        if result:
            key, value = result
            dic[keys[key]] = value
            try:
                words, result = self.respond_from_to(event, words)
            except ValueError:
                return
            if result:
                key2, value2 = result
                if key2 == key:
                    message = "Text can be translated {} only one language"
                    event.message.reply(message.format(key))
                    return
                dic[keys[key2]] = value2

        if len(words) > 1:
            event.message.reply("The text to be translated should be surrounded with quotation marks.")
            return

        event.message.reply(self.translator.translate("".join(words), **dic))

    def normalize(self, lang):
        # Normalized good locale codes will strip the spaces, but bad ones
        # remain as is.
        normalized = locale.normalize(lang)
        if normalized == lang and locale.normalize(lang + ' ') == lang + ' ':
            lang = lang.strip()
            raise ValueError("Unknown locale code: {}".format(lang), lang)
        return normalized[:2]
        
