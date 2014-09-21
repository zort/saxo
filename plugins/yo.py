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
            recipient = row[1]
            sender = row[0]
            message = row[4]
            quote = choice(['The old man down the road says, "%s"',
                            'A little bird said, "%s", and flew away.',
                            "There's a rumour going around that %s",
                            'There was a message in a bottle: "%s"',
                            'The tea leaves spell out: "%s"',
                            'I once heard this: "%s"',
                            'Yo, by the way, %s',
                            'At night, they howl and they cackle, and their words are: "%s"'])
            irc.say(quote % message)
            del db["saxo_yo"][row]

@saxo.event("JOIN")
def deliverJOIN(irc):
    deliver(irc)
