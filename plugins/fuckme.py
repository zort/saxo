import saxo

@saxo.event("PRIVMSG")
def fuckme(irc):
    if "fuck me" in irc.text.lower():
        irc.say("http://i.imgur.com/EgXFnFf.jpg")
