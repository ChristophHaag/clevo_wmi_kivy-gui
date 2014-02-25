from kivy.app import App
from kivy.properties import DictProperty
from kivy.uix.floatlayout import FloatLayout


def readfile(f):
    with open(f, "rb") as fi:
        return fi.read().decode("UTF-8").strip()


areas = ["left", "right", "middle"]

BRIGHTNESS = "/sys/devices/platform/clevo_wmi/kbled/brightness"
COLORS = {a: {"file": "/sys/devices/platform/clevo_wmi/kbled/" + a,
              "R": 0, "G": 0, "B": 0} for a in areas}
ORDER = ["G", "R", "B"]

brightness = readfile(BRIGHTNESS)
colors = dict()
for a in COLORS:
    rgb = readfile(COLORS[a]["file"])
    print(a + ": " + rgb)
    COLORS[a]["G"] = True if rgb[1] == "1" else False
    COLORS[a]["R"] = True if rgb[2] == "1" else False
    COLORS[a]["B"] = True if rgb[3] == "1" else False

class MainScreen(FloatLayout):
    currentcolors = DictProperty() #TODO how to use nested dict properties? AliasProperty doesn't have documentation nor examples???

    def on_currentcolors(self):
        print ("mee")

    def __init__(self, **kwargs):
        for a in areas:
            for i in ORDER:
                self.currentcolors[a + i] = True if COLORS[a][i] else False

        # first build the color stuff above and only then initialize the gui
        super(MainScreen, self).__init__(**kwargs)

class Clevo_WMI_GUI(App):
    def build(self):
        return MainScreen()


Clevo_WMI_GUI().run()