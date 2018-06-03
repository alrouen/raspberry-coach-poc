import time
import signal
from voice_engine.source import Source
from voice_engine.kws import KWS
from voice_engine.ns import NS
from avs.alexa import Alexa
from hatio import ThreePixels, Button

is_quit = []


class StateMachine:
    def __init__(self, wake_word_model):

        self.__src = Source(rate=16000)
        self.__ns = NS(rate=16000, channels=1)
        self.__kws = KWS(model=wake_word_model)
        self.__alexa = Alexa()

        self.__src.link(self.__ns)
        self.__ns.link(self.__kws)
        self.__kws.link(self.__alexa)

        self.__pixels = ThreePixels()
        self.__button = Button()

        self.__alexa.state_listener.on_listening = self.on_listening
        self.__alexa.state_listener.on_thinking = self.on_thinking
        self.__alexa.state_listener.on_speaking = self.on_speaking
        self.__alexa.state_listener.on_finished = self.on_finished

    def on_listening(self):
        self.__pixels.wakeup()

    def on_thinking(self):
        self.__pixels.think()

    def on_speaking(self):
        self.__pixels.speak()

    def on_finished(self):
        self.__pixels.off()

    def __on_detected(self, keyword):
        print('detected {}'.format(keyword))
        print('Alexa is listening!')
        self.__alexa.listen()

    def __pushed_button(self, channel):
        print('button pushed')
        print('Alexa is listening!')
        self.__alexa.listen()

    def start(self):
        print('starting voice engine')
        self.__kws.set_callback(self.__on_detected)
        Button.set_callback_on_rising(self.__pushed_button)
        self.__src.recursive_start()

    def stop(self):
        print('stopping voice engine')
        self.__src.recursive_stop()
        Button.clean_up()
        self.__pixels.off()


def signal_handler(signal, frame):
    print('Quit')
    is_quit.append(True)


if __name__ == "__main__":

    signal.signal(signal.SIGINT, signal_handler)

    stateMachine = StateMachine(wake_word_model='/home/pi/coach/alexa.pmdl')

    stateMachine.start()

    while not is_quit:
        time.sleep(1)

    stateMachine.stop()
    time.sleep(1)
