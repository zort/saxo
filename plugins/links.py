# http://inamidst.com/saxo/
# Created by Sean B. Palmer

import html.entities
import re
import time
import string

import saxo

regex_link = re.compile(r"http[s]?://[^<> \"\x01]+")
regex_title = re.compile(r"(?ims)<title[^>]*>(.*?)</title>")
regex_script = re.compile(r"(?ims)<script(.*?)</script>")
regex_tag = re.compile(r"<[^>]+>")
regex_entity = re.compile(r"&([^;\s]+);")
regex_youtube_link = re.compile(r"^https?://((www\.)?youtube\.com|youtu\.be)/\S+$")
nopunc = str.maketrans("","",string.punctuation)

@saxo.event("PRIVMSG")
def link(irc):
    search = regex_link.search(irc.text)
    if search:
        if irc.sender.startswith("#"):
            irc.client("link", irc.sender, search.group())

    for url in regex_link.findall(irc.text):
        if regex_twitter_link.match(url):
            irc.say(tw(url))
        else:
            # Blurt out the title, but only if it's not in the URL, ignoring
            # punctuation and whitespace
            t = title(url)
            if t:
                words = t.translate(nopunc).split()
                if not all(word.lower() in url.lower() for word in words):
                    irc.say(t)

        if regex_youtube_link.match(url):
            url = url.replace("youtube.com", "fixyt.com")
            url = url.replace("youtu.be", "fixyt.com")
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
        return
    if " " in url:
        return

    if not url.startswith("http"):
        url = "http://" + url

    if "#" in url:
        url = url.split("#", 1)[0]

    for blacklisted in blacklist:
        if blacklisted in url:
            return

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

        title = longest(title, " : ")
        title = longest(title, " | ")
        title = longest(title, "| ")
        title = longest(title, " — ")
        if "youtube.com" not in url:
            title = longest(title, " - ")
        elif title.endswith(" - YouTube"):
            title = title[:-10]
        title = title.replace('"', "'")
        return title.strip()
    return
























regex_twitter_username = re.compile(r"^[a-zA-Z0-9_]{1,15}$")
regex_twitter_link = re.compile(r"^https?://twitter.com/\S+$")
regex_twitter_p = re.compile(r"(?ims)(<p class=\"js-tweet-text.*?</p>)")
regex_twitter_div = re.compile(r'(?ims)<div class="tweet-text".*?</div></div>')
regex_twitter_tag = re.compile(r"(?ims)<[^>]+>")
regex_twitter_anchor = re.compile(r"(?ims)(<a.*?</a>)")
regex_twitter_exp = re.compile(r"(?ims)data-url=[\"'](.*?)[\"']")
regex_twitter_whiteline = re.compile(r"(?ims)[ \t]+[\r\n]+")
regex_twitter_breaks = re.compile(r"(?ims)[\r\n]+")
regex_twitter_b = re.compile(r"(?ims)<b>(.+?)</b>")
regex_twitter_follow = re.compile(r'action="/([^/]+)/follow"')
regex_twitter_canonical = \
    re.compile(r'rel="canonical" href="https?://twitter.com/([^/\">]+)')
tco = '<span class="tco-ellipsis"><span class="invisible">\xA0</span>…</span>'

class NotFound(Exception):
    ...

def page(url, username=None):
    page = saxo.request(url, follow=True)
    if page["status"] == 404:
        raise NotFound("No such tweet")
    text = page["text"]
    text = text.replace(tco, "")

    username = None
    retweeted = None
    tweet = None

    if not username:
        username = "?"
        for username in regex_twitter_canonical.findall(text):
            username = username
            break
        if username == "?":
            for username in regex_twitter_follow.findall(text):
                username = username
                break

    shims = ['<div class="main-tweet-container">',
             '<div class="content clearfix">']
    for shim in shims:
        if shim in text:
            text = text.split(shim, 1).pop()

    def expand(tweet):
        def replacement(match):
            anchor = match.group(1)
            for link in regex_twitter_exp.findall(anchor):
                return link
            return regex_twitter_tag.sub("", anchor)
        return regex_twitter_anchor.sub(replacement, tweet)

    for paragraph in regex_twitter_p.findall(text):
        preamble = text.split('p class="js-tweet-text', 1)[0][-512:]
        for rt in regex_twitter_b.findall(preamble):
            if rt != username:
                retweeted = rt

        paragraph = expand(paragraph)
        paragraph = regex_twitter_tag.sub("", paragraph)
        paragraph = paragraph.strip()
        paragraph = regex_twitter_whiteline.sub(" ", paragraph)
        tweet = regex_twitter_breaks.sub(" ", paragraph)
        break

    for div in regex_twitter_div.findall(text):
        div = div.split(">", 1).pop()
        div = expand(div)
        div = regex_twitter_tag.sub("", div)
        div = div.strip()
        div = regex_twitter_whiteline.sub(" ", div)
        tweet = regex_twitter_breaks.sub(" ", div)
        break

    if not tweet:
        raise Exception("Couldn't get a tweet from %s" % page["url"])
    return username, retweeted, tweet

def format_tweet(username, retweeted, tweet):
    if retweeted:
        return "%s (@%s, RT @%s)" % (tweet, username, retweeted)
    return "%s (@%s)" % (tweet, username)

def get_tweet_basic(username=None, tweet=None, url=None):
    if username:
        response = saxo.request("http://dpk.io/services/tw/" + username)
        return response["text"]

    elif tweet:
        url = "https://twitter.com/twitter/status/" + tweet
        username, retweeted, tweet = page(url)
        return format_tweet(username, retweeted, tweet)

    elif url:
        username, retweeted, tweet = page(url)
        return format_tweet(username, retweeted, tweet)

    raise ValueError("Needed username, id, or url")

def get_tweet(username=None, tweet=None, url=None):
    try: return get_tweet_basic(username=username, tweet=tweet, url=url)
    except NotFound:
        return "No such tweet"

def tw(arg):
    if not arg:
        arg = saxo.env("url")
        if arg is None:
            return "Show a tweet from a link, username, or tweet id"

    if arg.startswith("@"):
        arg = arg[1:]

    if set(arg) <= set("0123456789"):
        tweet = get_tweet(tweet=arg)
    elif regex_twitter_username.match(arg):
        tweet = get_tweet(username=arg)
    elif regex_twitter_link.match(arg):
        tweet = get_tweet(url=arg)
    else:
        return "Expected a link, a username, or a tweet id"

    return tweet
