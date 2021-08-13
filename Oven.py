import math

class Oven:    
    def __init__(self):
        self.temperature = 0
        self.heating = False

    def heatOn(self):
        self.heating = True
        
    def heatOff(self):
        self.heating = False

    def getTemp(self):
        return self.temperature

    def update(self, dt):
        if self.heating:
            self.temperature = self.temperature + ( 10 / max(math.sqrt( max(self.temperature, 0) ), 1) ) * dt
        else:
            if self.temperature > 0:
                self.temperature = self.temperature - ( max(math.sqrt( max(self.temperature, 0) ), 1) / 5 ) * dt
            else:
                self.temperature = 0
    