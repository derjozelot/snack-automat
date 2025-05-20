from machine import Pin
import time


class StepperMotor(object):
    def __init__(self,a,b,c,d):
        self.a=Pin(a, Pin.OUT)
        self.b=Pin(b, Pin.OUT)
        self.c=Pin(c, Pin.OUT)
        self.d=Pin(d, Pin.OUT)
              
        self.a.value(False)
        self.b.value(False)
        self.c.value(False)
        self.d.value(False)

    def rotate(self):
        self.a.value(True)
        time.sleep(0.001)
        self.b.value(True)
        time.sleep(0.001)
        self.a.value(False)
        time.sleep(0.001)
        self.c.value(True)
        time.sleep(0.001)
        self.b.value(False)
        time.sleep(0.001)
        self.d.value(True)
        time.sleep(0.001)
        self.c.value(False)
        time.sleep(0.001)
        self.a.value(True)
        time.sleep(0.001)
        self.a.value(False)
        self.d.value(False)
    
    def unrotate(self):
        self.d.value(True)
        time.sleep(0.001)
        self.c.value(True)
        time.sleep(0.001)
        self.d.value(False)
        time.sleep(0.001)
        self.b.value(True)
        time.sleep(0.001)
        self.c.value(False)
        time.sleep(0.001)
        self.a.value(True)
        time.sleep(0.001)
        self.b.value(False)
        time.sleep(0.001)
        self.d.value(True)
        time.sleep(0.001)
        self.d.value(False)
        self.a.value(False)
        
    def one_rotate(self):
        for i in range(512):
            self.rotate()


