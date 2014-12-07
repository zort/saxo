import saxo
import json
import threading

stream_on = None

@saxo.setup
def start_check_stream(irc):
    threading.Timer(60, check_stream, [irc]).start()
    
def check_stream(irc):
    global stream_on
    
    threading.Timer(60, check_stream, [irc]).start()
    
    page = saxo.request('https://api.twitch.tv/kraken/streams/lf2stream')['text']
    stream_on_now = page and json.loads(page)['stream']

    if stream_on_now and not stream_on:
        irc.send("PRIVMSG", "#lfe", "GREEN LAMP YO http://www.twitch.tv/lf2stream/")
    elif stream_on and not stream_on_now:
        irc.send("PRIVMSG", "#lfe", "lf2 stream ova")
    
    stream_on = stream_on_now
