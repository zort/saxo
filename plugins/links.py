# http://inamidst.com/saxo/
# Created by Sean B. Palmer

import html.entities
import re
# import time
# import string

import saxo

regex_link = re.compile(r"http[s]?://[^<> \"\x01]+")
regex_nobort = re.compile(r"\bnobort\b")
regex_title = re.compile(r"(?ims)<title[^>]*>(.*?)</title>")
# regex_script = re.compile(r"(?ims)<script(.*?)</script>")
regex_tag = re.compile(r"<[^>]+>")
regex_entity = re.compile(r"&([^;\s]+);")
regex_youtube_link = re.compile(r"^https?://((www\.)?youtube\.com|youtu\.be)/\S+$")
regex_youtube_time_link = re.compile(r"[#&?]t=[0-9sm]+$")
# regex_punc = re.compile(r"(\s|'s|[/·:])+")
stopwords = frozenset(str.split("i a about an are as at be by com for from how in is it of on or that the this to was what when where who will with the"))

@saxo.event("PRIVMSG")
def link(irc):
    nobort = regex_nobort.search(irc.text)
        
    for url in regex_link.findall(irc.text):
        irc.client("link", irc.sender, url)

        if not nobort:
            # Blurt out the title, but only if it's not obvious from the URL
            t = title(url)
            if t:
                # words = [word.lower() for word in re.split(regex_punc, t)]
                # words = [word.replace("'s","").replace("-","").replace(" ","") for word in words]
                # words = [word for word in words if word not in stopwords]
                words = set(re.split("\W+", t)).difference(stopwords)
                if not all(word.lower() in url.lower() for word in words):
                    print(str([word for word in words if word.lower() not in url.lower()]))
                    irc.say(t)

        if regex_youtube_link.match(url) and not regex_youtube_time_link.search(url):
            url = url.replace("youtube.com", "fixyt.com")
            url = url.replace("youtu.be/", "fixyt.com/watch?v=")
            url = url.replace("https://", "http://")
            irc.say("fixyt link: " + url)
        








blacklist = (
    "wikipedia.org",
    "terraria.gamepedia.com",
    "prntscr.com",
    "slexy.org"
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
    # if not url:
    #     url = saxo.env("url")
    # if not url:
    #     return None
    # if " " in url:
    #     return None
    if url.endswith(".jpg") or url.endswith(".png"):
        return None

    # if not url.startswith("http"):
    #     url = "http://" + url

    if "#" in url:
        url = url.split("#", 1)[0]

    for blacklisted in blacklist:
        if blacklisted in url:
            return None

    page = saxo.request(url, limit=262144, follow=True)
    if "html" not in page:
        return None
    # text = regex_script.sub("", page["html"])
    text = page["html"]
    search = regex_title.search(text)
    if search:
        title = search.group(1)
        title = regex_tag.sub("", title)
        title = decode_entities(title)
        title = title.replace("\r", "")
        title = title.replace("\n", "")

        # title = title.replace('"', "'")
        return title.strip()
    return None
