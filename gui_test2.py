from guizero import App, Text, Drawing, Picture
import time
import datetime
import threading
import RPi.GPIO as GPIO


# DATE
class DateThread(threading.Thread):
    def __init__(self, delay=10):
        threading.Thread.__init__(self)
        self.delay = delay

    def run(self):
        try:
            while True:
                refreshDate()
                time.sleep(self.delay)
        finally:
            print("")


def refreshDate():
    i = datetime.datetime.now()
    i = "%s-%s-%s   %s:%s" % (
        '{:02d}'.format(i.day), '{:02d}'.format(i.month), '{:04d}'.format(i.year), '{:02d}'.format(i.hour),
        '{:02d}'.format(i.minute))  # ,'{:02d}'.format(i.second))
    d.line(380, 25, 800, 25, color="black", width=60)
    d.text(380, 25, i, color="white", size=20)


# RPM
'''class RpmThread(threading.Thread):
    def __init__(self, rpm, timeout=4):
        threading.Thread.__init__(self)
        self.rpm = rpm
        self.state = rpm.count
        self.timeout = timeout

    def run(self):
        while (True):
            if 0 < self.rpm.count - self.state < 10:
                refreshRpm(0, 8)
            else:
                self.state = self.rpm.count
                self.rpm.start = None
            time.sleep(self.timeout)'''


# RPM
class Rpm():
    def __init__(self):
        self.start = time.time()
        self.last = -1
        self.count = 0
        d.text(470, 140, str(0) + " Rpm", color="white", size=20)
        refreshRpm(-1, 8)

    def elapsedTime(self):
        if time.time() - self.start <= 2:
            self.count += 1
        else:
            if self.count <= 2:
                refreshRpm(-1, self.last)
                self.last = -1
            else:
                rounds = int(60 * self.count / (time.time() - self.start))
                # print(str(time.time() - self.start))
                refreshRpm(rounds, self.last)
                self.last = int(rounds / 555)
            # print(rounds)
            self.start = time.time()
            self.count = 0


def rpmCallback(channel):
    if GPIO.input(channel):
        rpm.elapsedTime()


def refreshRpm(n_rpm, last):
    if n_rpm == -1:
        updateRpmBars(n_rpm, last)
        n_rpm = 0
    else:
        updateRpmBars(int(n_rpm / 555), last)
    d.line(470, 140, 800, 140, color="black", width=65)
    d.text(470, 140, str(n_rpm) + " Rpm", color="white", size=20)


def updateRpmBars(actual, last):
    if actual - last > 0:
        for i in range(last, actual + 1):
            colorBar(i)
    elif actual - last < 0:
        for i in range(last, actual, -1):
            clearBar(i)


def colorBar(level):
    if level == 0:
        d.rectangle(550, 400, 600, 380, color="Green", outline=True, outline_color="Green")
    elif level == 1:
        d.rectangle(540, 375, 600, 355, color="Green", outline=True, outline_color="Green")
    elif level == 2:
        d.rectangle(530, 350, 600, 330, color="Lawn Green", outline=True, outline_color="Lawn Green")
    elif level == 3:
        d.rectangle(520, 325, 600, 305, color="Yellow", outline=True, outline_color="Yellow")
    elif level == 4:
        d.rectangle(510, 300, 600, 280, color="Yellow", outline=True, outline_color="Yellow")
    elif level == 5:
        d.rectangle(500, 275, 600, 255, color="Orange", outline=True, outline_color="Orange")
    elif level == 6:
        d.rectangle(490, 250, 600, 230, color="Orange Red", outline=True, outline_color="Orange Red")
    elif level == 7:
        d.rectangle(480, 225, 600, 205, color="Red", outline=True, outline_color="Red")
    elif level == 8:
        d.rectangle(470, 200, 600, 180, color="Firebrick", outline=True, outline_color="Firebrick")


def clearBar(level):
    if level == 0:
        d.rectangle(550, 400, 600, 380, outline=True, outline_color="Green")
    elif level == 1:
        d.rectangle(540, 375, 600, 355, outline=True, outline_color="Green")
    elif level == 2:
        d.rectangle(530, 350, 600, 330, outline=True, outline_color="Lawn Green")
    elif level == 3:
        d.rectangle(520, 325, 600, 305, outline=True, outline_color="Yellow")
    elif level == 4:
        d.rectangle(510, 300, 600, 280, outline=True, outline_color="Yellow")
    elif level == 5:
        d.rectangle(500, 275, 600, 255, outline=True, outline_color="Orange")
    elif level == 6:
        d.rectangle(490, 250, 600, 230, outline=True, outline_color="Orange Red")
    elif level == 7:
        d.rectangle(480, 225, 600, 205, outline=True, outline_color="Red")
    elif level == 8:
        d.rectangle(470, 200, 600, 180, outline=True, outline_color="Firebrick")


# APP
def getApp(path):
    app = App(title="Tachimetro Digitale", bg="Black")
    app.full_screen = "true"

    d = Drawing(app, width=800, height=480)

    # d.image(5, 5, image=path + "fsp.png")
    # d.image(95, 5, image=path + "ansp.png")
    # d.image(185, 5, image=path + "absp.png")
    # d.image(275, 5, image=path + "frsp.png")
    # d.image(5, 105, image=path + "benac.png")

    d.line(0, 100, 800, 100, color="White", width=2)

    # KM
    km = open(path + "Km.txt", "r")
    tot = km.read()
    d.text(420, 65, tot, color="white", size=20)
    d.text(550, 65, "Km", color="white", size=20)

    # 0 KM/H
    d.text(20, 150, "0", color="white", size=200)
    d.text(350, 380, "Km/h", color="white", size=20)

    # 0 RPM
    # d.text(470, 140, str(0) + " Rpm", color="white", size=20)

    # EMPTY RPM
    # d.rectangle(550, 400, 600, 380, outline=True, outline_color="Green")
    # d.rectangle(540, 375, 600, 355, outline=True, outline_color="Green")
    # d.rectangle(530, 350, 600, 330, outline=True, outline_color="Lawn Green")
    # d.rectangle(520, 325, 600, 305, outline=True, outline_color="Yellow")
    # d.rectangle(510, 300, 600, 280, outline=True, outline_color="Yellow")
    # d.rectangle(500, 275, 600, 255, outline=True, outline_color="Orange")
    # d.rectangle(490, 250, 600, 230, outline=True, outline_color="Orange Red")
    # d.rectangle(480, 225, 600, 205, outline=True, outline_color="Red")
    # d.rectangle(470, 200, 600, 180, outline=True, outline_color="Firebrick")

    # EMPTY FUEL LEVEL
    d.rectangle(250, 105, 270, 185, outline=True, outline_color="Green")
    d.rectangle(230, 105, 250, 185, outline=True, outline_color="Green")
    d.rectangle(210, 105, 230, 185, outline=True, outline_color="Lawn Green")
    d.rectangle(190, 105, 210, 185, outline=True, outline_color="Yellow")
    d.rectangle(170, 105, 190, 185, outline=True, outline_color="Yellow")
    d.rectangle(150, 105, 170, 185, outline=True, outline_color="Orange")
    d.rectangle(130, 105, 150, 185, outline=True, outline_color="Orange Red")
    d.rectangle(110, 105, 130, 185, outline=True, outline_color="Red")
    d.rectangle(90, 105, 110, 185, outline=True, outline_color="Firebrick")

    return (app, d)


# LOW BEAN
'''def lbCallback(channel):
    if GPIO.input(channel):
        lbOn()
    else:
        lbOff()


def lbOn():
    d.image(5, 5, image=path + "fac.png")


def lbOff():
    d.image(5, 5, image=path + "fsp.png")'''


# INDICATORS
class Indicator():
    def __init__(self, channel, x, y, onIMG, offIMG, blink=False):
        self.channel = channel
        self.x = x
        self.y = y
        self.onIMG = onIMG
        self.offIMG = offIMG
        self.blink = blink
        d.image(self.x, self.y, image=path + self.offIMG)
        GPIO.setup(self.channel, GPIO.IN, GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.channel, GPIO.RISING, callback=self.callback)

    def callback(self, channel):
        if GPIO.input(channel):
            self.on(channel)
        else:
            self.off()

    def on(self, channel):
        if self.blink:
            while GPIO.input(channel):
                d.image(self.x, self.y, image=path + self.onIMG)
                time.sleep(1)
                d.image(self.x, self.y, image=path + self.offIMG)
                time.sleep(1)
        else:
            d.image(self.x, self.y, image=path + self.onIMG)

    def off(self):
        d.image(self.x, self.y, image=path + self.offIMG)


# SIMULATE OUTPUT
class OutputThread(threading.Thread):
    def __init__(self, pin):
        threading.Thread.__init__(self)
        self.pin = pin

    def run(self):
        while True:
            GPIO.output(self.pin, 1)
            time.sleep(0.008)
            GPIO.output(self.pin, 0)
            time.sleep(0.012)


class SimulateThread(threading.Thread):
    def __init__(self, values, delay):
        threading.Thread.__init__(self)
        self.values = values
        self.delay = delay
        self.last = 0

    def run(self):
        for v in self.values:
            time.sleep(self.delay)
            refreshRpm(v, int(self.last / 555))
            self.last = v


class SimulateInputThread(threading.Thread):
    def __init__(self, indicator, wait, time):
        threading.Thread.__init__(self)
        self.wait = wait
        self.time = time
        self.indicator = indicator
        self.last = 0

    def run(self):
        time.sleep(self.wait)
        self.indicator.on(channel=None)
        time.sleep(self.time)
        self.indicator.off()


if __name__ == "__main__":
    # SET PATH
    path = "C:\\Users\\betta\\PycharmProjects\\raspBerry\\Desktop\\"  # "/home/pi/Desktop/"

    # GET DISPLAY
    (app, d) = getApp(path)

    # SET BCM MODE
    GPIO.setmode(GPIO.BCM)

    # START DATE
    date = DateThread()
    date.start()

    # START FARI (head lights)
    hlChannel = 0
    hlX = 5
    hlY = 5
    hlOnIMG = "fac.png"
    hlOffIMG = "fsp.png"

    headLights = Indicator(hlChannel, hlX, hlY, hlOnIMG, hlOffIMG)

    # sHL = SimulateInputThread(headLights,2,5)
    # sHL.start()

    # GPIO.setup(hlChannel, GPIO.IN, GPIO.PUD_DOWN)
    # GPIO.add_event_detect(hlChannel, GPIO.RISING, callback=headLights.callback)

    # START ANABBAGLIANTI (low bean)
    lbChannel = 23
    lbX = 95
    lbY = 5
    lbOnIMG = "anac.png"
    lbOffIMG = "ansp.png"

    lowBean = Indicator(lbChannel, lbX, lbY, lbOnIMG, lbOffIMG)

    # sLB = SimulateInputThread(lowBean,8,5)
    # sLB.start()

    # GPIO.setup(lbChannel, GPIO.IN, GPIO.PUD_DOWN)
    # GPIO.add_event_detect(lbChannel, GPIO.RISING, callback=lowBean.callback)

    # START ABBAGLIANTI (high bean)
    hbChannel = 0
    hbX = 185
    hbY = 5
    hbOnIMG = "abac.png"
    hbOffIMG = "absp.png"

    highBean = Indicator(hbChannel, hbX, hbY, hbOnIMG, hbOffIMG)

    # sHB = SimulateInputThread(highBean,14,5)
    # sHB.start()

    # GPIO.setup(hbChannel, GPIO.IN, GPIO.PUD_DOWN)
    # GPIO.add_event_detect(hbChannel, GPIO.RISING, callback=highBean.callback)

    # START FRECCE (turn signal)
    tsChannel = 0
    tsX = 275
    tsY = 5
    tsOnIMG = "frac.png"
    tsOffIMG = "frsp.png"

    turnSignal = Indicator(tsChannel, tsX, tsY, tsOnIMG, tsOffIMG, blink=True)

    # GPIO.setup(tsChannel, GPIO.IN, GPIO.PUD_DOWN)
    # GPIO.add_event_detect(tsChannel, GPIO.RISING, callback=turnSignal.callback)  # se non funziona, chiamare la callback da funz esterna a classe

    # START BENZINA (fuel)
    fChannel = 0
    fX = 5
    fY = 105
    fOnIMG = "benac.png"
    fOffIMG = "bensp.png"

    fuel = Indicator(fChannel, fX, fY, fOnIMG, fOffIMG)

    # sF = SimulateInputThread(fuel,20,5)
    # sF.start()

    # GPIO.setup(fChannel, GPIO.IN, GPIO.PUD_DOWN)
    # GPIO.add_event_detect(fChannel, GPIO.RISING, callback=fuel.callback)

    # START RPM
    rpmChannel = 22

    # time.sleep(1)
    # rpmThread = RpmThread(rpm)
    # rpmThread.start()

    rpm = Rpm()

    # GPIO.setup(rpmChannel, GPIO.IN, GPIO.PUD_DOWN)
    # GPIO.add_event_detect(rpmChannel, GPIO.RISING, callback=rpmCallback)

    # SIMULATE OUTPUT

    # out_pin = 27
    # GPIO.setup(out_pin, GPIO.OUT)
    # ot = OutputThread(out_pin)
    # ot.start()

    # SIMULATE BARS
    values = [1500, 3000, 5000, 4500, 1700, 0, -1]
    st = SimulateThread(values, delay=3)
    st.start()

    app.display()

    GPIO.cleanup()
