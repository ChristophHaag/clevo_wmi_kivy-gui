from kivy.app import App
from kivy.properties import NumericProperty
from kivy.uix.floatlayout import FloatLayout

#from hardwaredevice import P1X0EM_HW #TODO: support different hardware stuff
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import hardwaredevice

class MainScreen(FloatLayout):
    brightness = NumericProperty()

    def brightness_change(self, _, val):
        i = str(int(val))
        print("set brightness to " + i)
        self.hw.setbrightness(i)

    def color_change(self, area, colorcomponent, _, val):
        print (area, colorcomponent, _, val)

        c = self.hw.getcolor(area)
        c.setcomponent(colorcomponent, val)
        self.hw.getArea(area).triggerHWUpdate()

    def __init__(self, **kwargs):
        self.hw = hardwaredevice.P1X0EM_HW()
        # first build the color stuff above and only then initialize the gui
        super(MainScreen, self).__init__(**kwargs)

class Clevo_WMI_GUI(App):
    def build(self):
        return MainScreen()

if __name__ == '__main__':
    Clevo_WMI_GUI().run()