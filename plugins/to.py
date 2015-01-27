# http://inamidst.com/saxo/
# Created by Sean B. Palmer

import os.path
import saxo
import time
import random

@saxo.setup
def setup(irc):
    path = os.path.join(irc.base, "database.sqlite3")
    with saxo.database(path) as db:
        if "saxo_to" not in db:
            db["saxo_to"].create(
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
        query = "SELECT * FROM saxo_to WHERE recipient = ? COLLATE NOCASE"
        for row in db.query(query, irc.nick.strip("_-`")):
            print(row)
            sender = row[0]
            recipient = row[1]
            unixtime = row[2]
            message = row[4]
            sender = sender.replace("Phoenix", random.choice(["Ponik", "Ponix"]))
            irc.say("%s: <%s> %s [%s]" % (irc.nick, sender, message, time.ctime(unixtime)))
            del db["saxo_to"][row]

@saxo.event("JOIN")
def deliverJOIN(irc):
    deliver(irc)
