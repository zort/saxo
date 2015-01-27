# http://inamidst.com/saxo/
# Created by Sean B. Palmer

import os.path
import saxo
from random import choice

@saxo.setup
def setup(irc):
    path = os.path.join(irc.base, "database.sqlite3")
    with saxo.database(path) as db:
        if "saxo_yo" not in db:
            db["saxo_yo"].create(
                ("sender", str),
                ("recipient", str),
                ("unixtime", int),
                ("channel", str),
                ("message", str))
        # TODO: Drop messages more than a year old

@saxo.event("PRIVMSG")
def deliver(irc):
    path = os.path.join(irc.base, "database.sqlite3")
    with saxo.database(path) as db:
        query = "SELECT * FROM saxo_yo WHERE recipient = ? COLLATE NOCASE"
        for row in db.query(query, irc.nick.strip("_-`")):
            print(row)
            message = row[4]
            def MC(message):
                splitted = message.split(maxsplit=1)
                if len(splitted) == 1:
                    return 'Yo, I\'m MC {0} and I\'m here to say,'.format(*splitted)
                else:
                    return 'Yo, I\'m MC {0} and I\'m here to say, {1}'.format(*splitted)
            quote = choice([
                    'The old man down the road says, "%s"'
                    ,'A little bird said, "%s", and flew away.'
                    ,"There's a rumour going around that %s"
                    ,'Nobody can deny that %s'
                    ,'There was a message in a bottle: "%s"'
                    ,'The tea leaves spell out: "%s"'
                    ,'I once heard this: "%s"'
                    ,'Yo, by the way, %s'
                    ,'At night, they howl and they cackle, and their words are: "%s"'
                    ,'If you listen carefully to the wind, you can hear "%s"'
                    ,'Heed this, and you shall prosper: "%s"'
                    ,'Some babies\' first words are "%s"'
                    ,MC
                    ,'It\'s forseeable that %s'
                    ,'Ancient scriptures read: "%s"'
                    ,'Your horoscope for today (or since last horoscope): "%s"'
                    ,'The alignment of the stars foretell %s'
                    ,'The townsfolk mutter about %s'
                    ,'The monks in the forest chant "%s"'
                    ,'From the depths of the well echoes a voice murmuring, "%s"'
                    ,'The tarot cards predict %s'
                    ,'The answer to Life, the Universe and Everything is: %s'
                    ,'Once a generation, someone has this brilliant thought: %s'
                    ,'Don\'t do drugs, they ruin you. Also, %s'
                    ,'Protect your environment. Also, %s'
                    ,'Don\'t do drugs, they ruin you. Also, protect your environment. Also, %s'
                    ,'Don\'t forget: "%s"'
                    ,'As William Wallace used to say, "%s"'
                    ,'Even the ancients knew: %s'
                    ,'The bible contains the encoded message: "%s"'
                    ,'If you put a seashell to your ear, you can hear "%s"'
                    ,'Any undergraduate can tell you that %s'
                    ,'The message you have been tasked to deliver is: "%s"'
                    ])
            irc.say(quote % message if type(quote) == type("") else quote(message))
            del db["saxo_yo"][row]

@saxo.event("JOIN")
def deliverJOIN(irc):
    deliver(irc)
