import saxo
import json
import threading

stream_on = None

@saxo.setup
def check_stream(bla):
    global stream_on
    
    threading.Timer(60, check_stream, [saxo]).start()
    
    page = saxo.request('https://api.twitch.tv/kraken/streams/lf2stream')['text']
    stream_on_now = json.loads(page)['stream']

    if stream_on_now and not stream_on:
        saxo.send("PRIVMSG", "#lfe", "GREEN LAMP YO http://www.twitch.tv/lf2stream/")
    elif stream_on and not stream_on_now:
        saxo.send("PRIVMSG", "#lfe", "lf2 stream ova")
    
    stream_on = stream_on_now
