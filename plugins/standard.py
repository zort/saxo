# http://inamidst.com/saxo/
# Created by Sean B. Palmer

import saxo
import re

@saxo.event("PRIVMSG")
def exclamation(irc):
    if irc.text == irc.config["nick"]:
        irc.say(irc.nick)
    elif irc.text == irc.config["nick"] + "!":
        irc.say(irc.nick + "!")

# TODO: Move this into prefix.py?
@saxo.event("PRIVMSG")
def prefix(irc):
    if irc.text == irc.config["nick"] + ": prefix?":
        irc.reply('"' + irc.config["prefix"] + '"')

@saxo.event("PRIVMSG")
def wololo(irc):
    if re.match("(18(?!!)|29)\\b", irc.text):
        irc.say("30!")

@saxo.event("PRIVMSG")
def kingme(irc):
    if re.search("\\bking me\\b", irc.text):
        irc.say("17")
