# http://inamidst.com/saxo/
# Created by Sean B. Palmer

import saxo
import re
from threading import Timer
import random

@saxo.event("PRIVMSG")
def exclamation(irc):
    if (irc.text.startswith(irc.config["nick"]) and
        re.match("(\\W*)$", irc.text[len(irc.config["nick"]):])):
        irc.say(irc.text.replace(irc.config['nick'], irc.nick))

@saxo.event("PRIVMSG")
def wololo(irc):
    if re.search("\\b(18(?![!])|29(?![?]))\\b", irc.text):
        Timer(random.uniform(1.0,1.5), irc.say, ["30!"]).start()

@saxo.event("PRIVMSG")
def kingme(irc):
    if re.search("\\bking me\\b", irc.text, re.IGNORECASE):
        irc.say("17")

@saxo.event("PRIVMSG")
def fuckme(irc):
    if re.search("\\bfuck me\\b", irc.text, re.IGNORECASE):
        irc.say("http://i.imgur.com/EgXFnFf.jpg")

@saxo.event("PRIVMSG")
def weakasposs(irc):
    if re.search("\\weak as piss\\b", irc.text, re.IGNORECASE):
        msg = random.choice(
            ["Who the hell %s?" % x for x in ["put you up to that", "told you to do this", "told you to do that", "gave you that idea"]]
            +
            ["Z" + "O" * x + "U" * (x-3) + "L" * (x-6) for x in [random.randint(8,12)]]
            )
        if irc.text.isupper():
            msg = msg.upper()
        Timer(random.uniform(1.0,1.5), irc.say, [msg]).start()
