from kivy.app import App
from kivy.properties import DictProperty, NumericProperty
from kivy.uix.floatlayout import FloatLayout
import os

def readfile(f):
    with open(f, "rb") as fi:
        return fi.read().decode("UTF-8").strip()


def writefile(f, val):
    print("Writing " + val + " to " + f)

    #TODO
    cmd = "echo " + val +  " > " + f
    print(os.popen(cmd).read())

    #fails silently with "w"
    #fi = os.fdopen(os.open(f, os.O_WRONLY | os.O_APPEND | os.O_EXCL), "w")
    #print(fi.write(val))

    #[Errno 22] Invalid argument
    #with open(f, "w+b", buffering=0) as fi:
    #with open(f, "w") as fi:
    #    try:
    #        #fi.write(bytes(val, "ASCII"))
    #    except Exception as e:
    #        print("Error while writing: ", e)

areas = ["left", "right", "middle"]

BRIGHTNESS = "/sys/devices/platform/clevo_wmi/kbled/brightness"
COLORS = {a: {"file": "/sys/devices/platform/clevo_wmi/kbled/" + a,
              "R": 0, "G": 0, "B": 0} for a in areas}
ORDER = ["G", "R", "B"]

def readcolors():
    for a in COLORS:
        rgb = readfile(COLORS[a]["file"])
        print(a + ": " + rgb)
        COLORS[a]["G"] = True if rgb[1] == "1" else False
        COLORS[a]["R"] = True if rgb[2] == "1" else False
        COLORS[a]["B"] = True if rgb[3] == "1" else False

intmap = {True: 1, False: 0}


class MainScreen(FloatLayout):
    currentcolors = DictProperty() #TODO how to use nested dict properties? AliasProperty doesn't have documentation nor examples???
    brightness = NumericProperty()


    def refreshcurrentcolors(self):
        readcolors()
        for a in areas:
            for i in ORDER:
                self.currentcolors[a + i] = True if COLORS[a][i] else False


    def brightness_change(self, _, val):
        i = str(int(val))
        print("set brightness to " + i)
        writefile(BRIGHTNESS, i)

    #horrible
    def color_change(self, sender, val):
        #print (sender.whoami, val)
        a = sender.whoami["area"]
        c = sender.whoami["color"]
        currentmask = [0,0,0]
        print(self.currentcolors)
        for i in self.currentcolors.keys():
            if str(i).startswith(a):
                idx = ORDER.index(str(i)[-1])
                currentmask[idx] = self.currentcolors.get(i)
                print("idx", idx, currentmask[idx])
        indextochange = ORDER.index(c)
        print("set current " + a + ": " + str(currentmask))
        currentmask[indextochange] = val
        print("to new " + a + ": " + str(currentmask))
        s = "".join([ str(intmap[i]) for i in currentmask])
        writefile(COLORS[a]["file"], s)
        # instead of updating stuff in data structures, just re-read the whole thing
        self.refreshcurrentcolors()

    def __init__(self, **kwargs):
        self.refreshcurrentcolors()
        self.brightness = int(readfile(BRIGHTNESS))
        # first build the color stuff above and only then initialize the gui
        super(MainScreen, self).__init__(**kwargs)

class Clevo_WMI_GUI(App):
    def build(self):
        return MainScreen()


Clevo_WMI_GUI().run()