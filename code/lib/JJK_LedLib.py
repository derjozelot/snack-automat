#
# Diese Library ist von uns selbst geschrieben worden.
# Sie dient lediglich dazu, dass wir die Led Streifen alle Steuern können mit selbst programmierten Effekten
#

#
# JJK Electronics©
#

from neopixel import NeoPixel
from machine import Pin
import utime

class LedStrip():
    def __init__(self, pin ,num_leds):
        self.num_leds = num_leds
        self.pin = Pin(pin)
        self.np = NeoPixel(self.pin, self.num_leds)
        self._blink_timer = None
    
    def strip_red(self, brightness=1):
        self.strip_colour(255, 0, 0, brightness)

    def strip_green(self, brightness=1):
        self.strip_colour(0, 255, 0, brightness)
        
    def strip_blue(self, brightness=1):
        self.strip_colour(0, 0, 255, brightness)
    
    def strip_yellow(self, brightness=1):
        self.strip_colour(255, 255, 0, brightness)

    def strip_white(self, brightness=1):
        self.strip_colour(255, 255, 255, brightness)
        
    def off(self):
        for i in range(self.num_leds):
            self.np[i] = (0, 0, 0)
        self.np.write()
    
    def strip_colour(self, r, g, b, brightness=1):
        factor_r = round(r * brightness)
        factor_g = round(g * brightness)
        factor_b = round(b * brightness)
        
        if (brightness > 1):
            print("[LedLib] Error: Brightness can't be over 1")
            return
        
        for i in range(self.num_leds):
            self.np[i] = (factor_r, factor_g, factor_b)
        self.np.write()
        
    def led_colour(self, led, r, g, b, brightness=1):
        if (brightness > 1):
            print("[LedLib] Error: Brightness can't be over 1")
            return
        
        factor_r = round(r * brightness)
        factor_g = round(g * brightness)
        factor_b = round(b * brightness)
         
        self.np[led - 1] = (factor_r, factor_g, factor_b)
        self.np.write()

    def strip_gradient(self, color1, color2):
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        
        for i in range(self.num_leds):
            ratio = i / (self.num_leds - 1) if self.num_leds > 1 else 0
            r = round(r1 + (r2 - r1) * ratio)
            g = round(g1 + (g2 - g1) * ratio)
            b = round(b1 + (b2 - b1) * ratio)
            self.np[i] = (r, g, b)
        self.np.write()
    
    def leds_gradient(self, led_1, led_2, color1, color2):
        if led_1 < 1 or led_2 > self.num_leds or led_1 > led_2:
            return

        r1, g1, b1 = color1
        r2, g2, b2 = color2
        led_range = led_2 - led_1 + 1

        start_index = led_1 - 1
        end_index = led_2 - 1

        for i in range(start_index, end_index + 1):
            ratio = (i - start_index) / (led_range - 1) if led_range > 1 else 0

            r = round(r1 + (r2 - r1) * ratio)
            g = round(g1 + (g2 - g1) * ratio)
            b = round(b1 + (b2 - b1) * ratio)

            self.np[i] = (r, g, b)

        self.np.write()