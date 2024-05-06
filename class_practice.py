class AudioVisual:
    def __init__(self, power, volumn):
        self.power = power
        self.volumn = volumn
    def switch(self, on_off):
        self.power = on_off
    def set_volumn(self, vol):
        self.volumn = vol

class Audio(AudioVisual):
    def __init__(self, power, volumn):
        super().__init__(power, volumn)
    def tune(self):
        str = "La La La..." if self.power else "turn it on"
        print(str)

class TV(AudioVisual):
    def __init__(self, power, volumn, size):
        super().__init__(power, volumn)
        self.size = size
    def watch(self):
        str = "have fun!" if self.power else "switch on"
        print(str)
    
obj1 = TV(False, 12, 40)
obj1.switch(True)
obj1.watch()

obj2 = Audio(True, 12)
obj2.set_volumn(6)
obj2.tune()
