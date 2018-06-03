import time
from hatio import ThreePixels, Button

if __name__ == "__main__":

    pixels = ThreePixels()
    button = Button()

    while True:

        try:
            if button.state:
                print "button off"
            else:
                print "button on"
            print "wakeup"
            pixels.wakeup()
            time.sleep(3)
            print "think"
            pixels.think()
            time.sleep(3)
            print "speak"
            pixels.speak()
            time.sleep(3)
            print "off"
            pixels.off()
            time.sleep(3)
        except KeyboardInterrupt:
            break

    pixels.off()
    time.sleep(1)
