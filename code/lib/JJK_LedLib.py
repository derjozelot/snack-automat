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
    
    def strip_red(self, brightness=1):
        red = round(255 * brightness)
        if (red > 255):
            print("Error changing LED colour: Brightness cant be over 1")
            return
        for i in range(self.num_leds):
            self.np[i] = (red, 0, 0)
        self.np.write()

    def strip_green(self, brightness=1):
        green = round(255 * brightness)
        if (green > 255):
            print("Error changing LED colour: Brightness cant be over 1")
            return
        for i in range(self.num_leds):
            self.np[i] = (0, green, 0)
        self.np.write()
        
    def strip_blue(self, brightness=1):
        blue = round(255 * brightness)
        if (blue > 255):
            print("Error changing LED colour: Brightness cant be over 1")
            return
        for i in range(self.num_leds):
            self.np[i] = (0, 0, blue)
        self.np.write()

    def strip_white(self, brightness=1):
        white = round(255 * brightness)
        if (white > 255):
            print("Error changing LED colour: Brightness cant be over 1")
            return
        for i in range(self.num_leds):
            self.np[i] = (white, white, white)
        self.np.write()
    
    def strip_yellow(self, brightness=1):
        yellow = round(255 * brightness)
        if (yellow > 255):
            print("Error changing LED colour: Brightness cant be over 1")
            return
        for i in range(self.num_leds):
            self.np[i] = (yellow, yellow, 0)
        self.np.write()

    def off(self):
        for i in range(self.num_leds):
            self.np[i] = (0, 0, 0)
        self.np.write()
    
    def strip_colour(self, r, g, b):
        for i in range(self.num_leds):
            self.np[i] = (r, g, b)
        self.np.write()
        
    def led_colour(self, led, r, g, b):
        self.np[led] = (r, g, b)
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

    
    def leds_colour(self, led_1, led_2, r, g, b, brightness):
        red = round(r * brightness)
        green = round(g * brightness)
        blue = round(b * brightness)
        
        if (brightness > 1):
            print("Error changing LED colour: Brightness cant be over 1")
            return
        for i in range(led_1 - 1, led_2):
            self.np[i] = (red, green, blue)
        self.np.write()
        

