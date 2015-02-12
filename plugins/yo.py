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
                    ,'They go my niggaz all up in da hood sayin\' "%s"'
                    ,'Dem hoes keep tryin to buck my rides, one spittin\' "%s"'
                    ,'It was complete darkness. The little boy heard a whisper coming from the closed wardrobe: "%s%"'
                    ,'"%s" is a lie.'
                    ,'"%s" is the truth.'
                    ,'Only idiots say things like "%s"'
                    ,'I have been told that "%s" is a must.'
                    ,'"%s" and a puppy just died.'
                    ,'Money cannot buy you "%s".'
                    ,irc.nick + ', you are the ugliest person on this planet. But "%s".'
                    ,'Here, "%s". By the way, ' + irc.nick + ' is a terrible name.'
                    ,'I have a message for you written with blood: "%s"'
                    ,irc.nick + ', I will kill you in your sleep, whispering "%s".'
                    ,'Dear ' + irc.nick + ', please stop playing with yourself while moaning "%s".'
                    ,'In this room %s is turning me on, but %%s' % irc.nick
                    ,'Goddamnit %s! Here have your smelly message: %%s' % irc.nick
                    ])
            irc.say(quote % message if type(quote) == type("") else quote(message))
            del db["saxo_yo"][row]

@saxo.event("JOIN")
def deliverJOIN(irc):
    deliver(irc)
