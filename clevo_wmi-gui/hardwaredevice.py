from kivy.properties import BooleanProperty

import clevoio


class Clevo_HW():
    BRIGHTNESSFILE = "/sys/devices/platform/clevo_wmi/kbled/brightness"

    def updatetoinitialHWvalues(self):
        for a in self.areas:
            rgb = clevoio.readfile(a.hwdev)
            #print(a.getName() + ": " + rgb)
            G = True if rgb[1] == "1" else False
            R = True if rgb[2] == "1" else False
            B = True if rgb[3] == "1" else False
            a.getColor().setRGB(R, G, B)
            #print(a.getName() + ": " + str(a.getColor()))

        # TODO: NumericProperty.
        # "Slider.value have an invalid format (got kivy.properties.NumericProperty object".
        # What's the problem with that?
        self.brightness = int(clevoio.readfile(self.BRIGHTNESSFILE))
        print([str(a) for a in self.areas])

    def getBrightness(self):
        return self.brightness

    def getcolor(self, areastring):
        for a in self.getAreas():
            if a.getName() == areastring:
                return a.getColor()

    def setcolor(self, R, G, B, areastring):
        for a in self.areas:
            if a.getName() == areastring:
                a.setColor(RGBColor(R, G, B))
                a.triggerHWUpdate()

    def setbrightness(self, brightnessval):
        clevoio.writefile(self.BRIGHTNESSFILE, str(brightnessval))

    def getAreas(self):
        return self.areas

    def updateAllHW(self):
        for a in self.getAreas():
            a.triggerHWUpdate()

    def getAreaNames(self):
        return [area.getName() for area in self.getAreas()]

    def getArea(self, area):
        for a in self.getAreas():
            if a.getName() == area:
                return a

class RGBColor():
    def __init__(self, R, G, B):
        self.c = { "R": BooleanProperty(R),
                    "G": BooleanProperty(G),
                    "B": BooleanProperty(B)
        }

    def __str__(self):
        return "(R: " + str(self.c["R"]) + ", G: " + str(self.c["G"]) + ", B: " + str(self.c["B"]) + ")"

    def setcomponent(self, component, val):
        print("set component", component, "to", val)
        self.c[component] = val # TODO: booleanproperty
        print(self.c["R"], self.c["G"], self.c["B"])

    def getcomponent(self, component):
        return self.c[component]

    def getRGB(self):
        return self.c["R"], self.c["G"], self.c["B"]

    def setRGB(self, R, G, B):
        self.c["R"] = R
        self.c["G"] = G
        self.c["B"] = B

class area():
    def __init__(self, name, hwdev, color, order):
        self.name = name
        self.hwdev = hwdev
        self.color = color
        self.order = order

    def __str__(self):
        return "Name: " + self.getName() + "; Color: " + str(self.getColor())

    def RGBtoMask(self, R, G, B):
        mask = ["", "", ""]
        mask[self.order.index("R")] = ("1" if R else "0")
        mask[self.order.index("G")] = ("1" if G else "0")
        mask[self.order.index("B")] = ("1" if B else "0")
        return "".join(mask)

    def getName(self):
        return self.name

    def getHWDev(self,name):
        return self.name

    # def setColor(self, color):
    #     self.color.setRGB(color.R, color.G, color.B)

    def getColor(self):
        return self.color

    def triggerHWUpdate(self):
        mask = self.RGBtoMask(self.getColor().getcomponent("R"), self.getColor().getcomponent("G"), self.getColor().getcomponent("B"))
        print(mask)
        clevoio.writefile(self.hwdev, mask)

class P1X0EM_HW(Clevo_HW):
    def __init__(self):
        ORDER = ["G", "R", "B"] # a bit redundant
        self.left = area("left", "/sys/devices/platform/clevo_wmi/kbled/left", RGBColor(0,0,0), ORDER)
        self.middle = area("middle", "/sys/devices/platform/clevo_wmi/kbled/middle", RGBColor(0,0,0), ORDER)
        self.right = area("right", "/sys/devices/platform/clevo_wmi/kbled/right", RGBColor(0,0,0), ORDER)

        self.areas = [self.left, self.middle, self.right]
        self.updatetoinitialHWvalues()


