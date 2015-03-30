# http://inamidst.com/saxo/
# Created by Sean B. Palmer

import saxo

import re
import urllib.parse
from lxml import etree

regex_link = re.compile(r"http[s]?://[^<> \"\x01]+")
stopwords = frozenset(str.split("i a about an are as at be by com for from how in is it of on or that the this to was what when where who will with the"))

@saxo.event("PRIVMSG")
def link(irc):
    nobort = "nobort" in irc.text
        
    for url in regex_link.findall(irc.text):
        irc.client("link", irc.sender, url)

        if nobort:
            continue
        
        text = maybe_request(url)
        if text is None:
            continue
        
        blurbs = [title(text), excerpt(text)]
        
        print("  ☒☒☒  ".join(map(str, blurbs))) # for the log
        
        def interesting(blurb):
            if blurb is None:
                return False
            words = set(re.split("\W+", blurb.lower())).difference(stopwords)
            merl = urllib.parse.unquote(url).lower()
            return not all(word in merl for word in words)

        result = "  ☒☒☒  ".join(filter(interesting, blurbs))
        if result != "":
            irc.say(result)

blacklist = (
    "wikipedia.org",
    "terraria.gamepedia.com",
    "prntscr.com",
    "slexy.org"
)

def maybe_request(url):
    # FixYT fills its page via Javascript, but we can get everything from the
    # corresponding Youtube page
    url = url.replace("http://fixyt.com", "http://youtube.com")
    
    if url.endswith(".jpg") or url.endswith(".png") or url.endswith(".gif"):
        return None

    if "#" in url:
        url = url.split("#", 1)[0]

    for blacklisted in blacklist:
        if blacklisted in url:
            return None

    page = saxo.request(url, limit=262144, follow=True)
    if "html" not in page:
        return None
    else:
        return page["html"]

def try_xpaths(text, queries):
    root = etree.HTML(text)
    for query in queries:
        result = root.xpath(query)
        if result:
            return result[0].strip()

def title(text):
    return try_xpaths(text, ['/html/head/title//text()'])

def excerpt(text):
    return try_xpaths(text,
                      # Copied from https://github.com/nocive/html-page-excerpt/blob/master/lib/HTMLPageExcerpt.php#L485-537
                      ['/html/head/meta[@property="og:description"]/@content',
                       '/html/head/meta[@name="description"]/@content',
                       '//article/section//text()',
                       '//p//text()']):
