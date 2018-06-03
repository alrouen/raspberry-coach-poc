import time
import signal
from voice_engine.source import Source
from voice_engine.kws import KWS
from voice_engine.ns import NS
from avs.alexa import Alexa


src = Source(rate=16000)
ns = NS(rate=16000, channels=1)
kws = KWS(model='/home/pi/coach/alexa.pmdl')
alexa = Alexa()

src.link(ns)
ns.link(kws)
kws.link(alexa)

def on_detected(keyword):
    print('detected {}'.format(keyword))
    print('Alexa is listening!')
    alexa.listen()

kws.set_callback(on_detected)

is_quit = []
def signal_handler(signal, frame):
    print('Quit')
    is_quit.append(True)

signal.signal(signal.SIGINT, signal_handler)

src.recursive_start()
while not is_quit:
    time.sleep(1)
src.recursive_stop()
