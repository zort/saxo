# http://inamidst.com/saxo/
# Created by Sean B. Palmer

import html.entities
import re
import time
import string

import saxo

regex_link = re.compile(r"http[s]?://[^<> \"\x01]+")
regex_nobort = re.compile(r"\bnobort\b")
regex_title = re.compile(r"(?ims)<title[^>]*>(.*?)</title>")
regex_script = re.compile(r"(?ims)<script(.*?)</script>")
regex_tag = re.compile(r"<[^>]+>")
regex_entity = re.compile(r"&([^;\s]+);")
regex_youtube_link = re.compile(r"^https?://((www\.)?youtube\.com|youtu\.be)/\S+$")
regex_youtube_time_link = re.compile(r"[#&?]t=[0-9sm]+$")
nopunc = str.maketrans("","",string.punctuation.replace(".","")) # usually punctuation gets deleted except when it's a file name (and church+glass)

@saxo.event("PRIVMSG")
def link(irc):
    search = regex_link.search(irc.text)
    if search:
        if irc.sender.startswith("#"):
            irc.client("link", irc.sender, search.group())

    if not regex_nobort.search(irc.text):
        for url in regex_link.findall(irc.text):
            if regex_twitter_link.match(url):
                irc.say(tw(url))
            else:
                # Blurt out the title, but only if it's not in the URL, ignoring
                # punctuation and whitespace
                t = title(url)
                if t:
                    if not all(word.lower().replace("'","") in url.lower()
                               for word in t.split()):
                        irc.say("Title: " + t)

            if regex_youtube_link.match(url) and not regex_youtube_time_link.search(url):
                url = url.replace("youtube.com", "fixyt.com")
                url = url.replace("youtu.be/", "fixyt.com/watch?v=")
                url = url.replace("https://", "http://")
                irc.say("fixyt link: " + url)









def longest(input, sep):
    longest = 0
    result = ""
    for part in input.split(sep):
        part = part.strip()
        if len(part) > longest:
           longest = len(part)
           result = part
    return result

blacklist = (
    "swhack.com",
    "translate.google.com",
    "tumbolia.appspot.com",
    "wikia.com",
    "wikipedia.org"
)

def decode_entities(hypertext):
    def entity(match):
        name = match.group(1).lower()

        if name.startswith("#x"):
            return chr(int(name[2:], 16))
        elif name.startswith("#"):
            return chr(int(name[1:]))
        elif name in html.entities.name2codepoint:
            return chr(html.entities.name2codepoint[name])
        return "[" + name + "]"

    return regex_entity.sub(entity, hypertext)

def title(url):
    if not url:
        url = saxo.env("url")
    if not url:
        return None
    if " " in url:
        return None

    if not url.startswith("http"):
        url = "http://" + url

    if "#" in url:
        url = url.split("#", 1)[0]

    for blacklisted in blacklist:
        if blacklisted in url:
            return None

    if "nytimes.com" in url:
        return url.rsplit(".html", 1)[0].rsplit("/").pop()

    page = saxo.request(url, limit=262144, follow=True)
    if "html" not in page:
        return None
    text = regex_script.sub("", page["html"])
    search = regex_title.search(text)
    if search:
        title = search.group(1)
        title = regex_tag.sub("", title)
        title = decode_entities(title)
        title = title.replace("\r", "")
        title = title.replace("\n", "")

        # title = longest(title, " : ")
        # title = longest(title, " | ")
        # title = longest(title, "| ")
        # title = longest(title, " — ")
        # if "youtube.com" not in url:
        #     title = longest(title, " - ")
        # elif title.endswith(" - YouTube"):
        #     title = title[:-10]
        title = title.replace('"', "'")
        return title.strip()
    return None
