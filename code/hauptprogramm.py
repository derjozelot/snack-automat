from schrittmotorlib import schrittmotor
from machine import I2C, Pin
import time



m1 = Pin(28,27,26,22, Pin.OUT)

time.sleep(1)
m1.eine_umdrehung()
time.sleep(1)
m1.eine_umdrehung()
