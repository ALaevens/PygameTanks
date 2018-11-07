import math

class Vec(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.angle = self.getAngle()

    def getMagnitude(self):
        magnitude = math.sqrt(self.x**2 + self.y**2)
        return magnitude

    def getAngle(self):
        side = 0
        angle = 0
        if self.x >= 0:
            side = 0
        else:
            side = 1
        if self.x == 0:
            if self.y > 0:
                angle = 90
            elif self.y < 0:
                angle = 270
            else:
                angle = 0
        else:
            angle = 180*side + math.degrees(math.atan(self.y/self.x))
        return angle

    def globalRotate(self,angle):
        mag = self.getMagnitude()
        self.angle = angle%360
        if self.angle == 90 or self.angle == 270:
            self.x = 0.0
        else:
            self.x = mag * math.cos(math.radians(angle))
        if self.angle == 0 or self.angle == 180:
            self.y = 0.0
        else:
            self.y = mag*math.sin(math.radians(angle))

    def localRotate(self,angle):
        self.globalRotate(self.angle + angle)

    def magnitude(self,mag):
        self.x = mag*math.cos(math.radians(self.angle))
        self.y = mag*math.sin(math.radians(self.angle))

