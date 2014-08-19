# http://inamidst.com/saxo/
# Created by Sean B. Palmer

import os.path
import saxo

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
            irc.say('"%s"' % message)
            del db["saxo_yo"][row]

@saxo.event("JOIN")
def deliverJOIN(irc):
    deliver(irc)
