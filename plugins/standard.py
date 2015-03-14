# http://inamidst.com/saxo/
# Created by Sean B. Palmer

import saxo
import re
from threading import Timer
import random

@saxo.event("PRIVMSG")
def exclamation(irc):
    if re.search(r"^%s\W*$" % irc.config["nick"], irc.text):
        irc.say(irc.text.replace(irc.config['nick'], irc.nick))

@saxo.event("PRIVMSG")
def wololo(irc):
    if re.search(r"\b(18(?![!])|29(?![?]))\b", irc.text):
        Timer(random.uniform(1.0,1.5), irc.say, ["30!"]).start()

    if re.search(r"\bking me\b", irc.text, re.IGNORECASE):
        irc.say("17")

    if re.search(r"\bfuck me\b", irc.text, re.IGNORECASE):
        irc.say("http://i.imgur.com/EgXFnFf.jpg")

    if re.search(r"enjoy.*reading", irc.text, re.IGNORECASE):
        irc.say("http://i.imgur.com/QmReEX3.jpg")

    if re.search(r"\bweak as piss\b", irc.text, re.IGNORECASE):
        msg = random.choice(
            ["Who the hell %s?" % x for x in ["put you up to that",
                                              "told you to do this",
                                              "told you to do that",
                                              "gave you that idea"]]
            +
            ["Z" + "O" * x + "U" * (x-3) + "L" * (x-6) for x in [random.randint(8,12)]]
            )
        if irc.text.isupper():
            msg = msg.upper()
        Timer(random.uniform(1.0,1.5), irc.say, [msg]).start()
