#
# Süßgkeiten Automat von Jakob F. Jonas O. und Karim A.
# Wir haben uns dazu entschieden die Variablen und Backend benannten Funktionen aus Simplizität auf Englisch zu benennen!

#
# JJK Electronics©
#

# Zum starten: Einfach 3 zeichige Item Nummer eingeben.
# 4 Zeichen: Abbruch
# '#': Abbruch
# '*': Bestätigen

# Es gibt einige geheime Codes die man eingeben kann, die auch in der configuration.json geändert werden können


from time import sleep_ms
from machine import I2C, Pin
from machine_i2c_lcd import I2cLcd
from DIYables_Pico_Keypad import Keypad
from schrittmotorlib import schrittmotor

import debug
import utime
import random
import json

debug.println("Imports loaded", "INIT")

# Hardware Setup

led_g = Pin(17, Pin.OUT)
led_r = Pin(18, Pin.OUT)

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=100000)

lcd = I2cLcd(i2c, 0x27, 2, 16)

NUM_ROWS = 4
NUM_COLS = 3

ROW_PINS = [2, 3, 4, 5]
COLUMN_PINS = [6, 7, 8]

KEYMAP = ['1', '2', '3',
          '4', '5', '6',
          '7', '8', '9',
          '*', '0', '#']

keypad = Keypad(KEYMAP, ROW_PINS, COLUMN_PINS, NUM_ROWS, NUM_COLS)
keypad.set_debounce_time(400)

motor_001 = schrittmotor(9,10,11,12)
motor_002 = schrittmotor(13,14,15,16)

debug.println("Hardware setup finished", "INIT")

# Produkt Variablen

product_id = None
product_name = None
product_price = None
product_motor = None
product_slot = None

debug.println("Start variables setup finished", "INIT")

# Software Setup

with open('configuration.json') as configuration:
    config = json.load(configuration)
    configuration.close()
    print(config)

# Automat Variablen

condition = 2 # condition = Zustand
user_input = None
error_code = None
key = None

debug.println("Setup automat variables", "INIT")

def main_menu():
  led_g.off()
  led_r.off()
  lcd.clear()
  lcd.move_to(2,0)
  lcd.putstr("Willkommen!")
  lcd.move_to(0,1)
  lcd.putstr("Bitte w\xE1hlen...")        
  debug.println("Main menu loaded")

def restart():
    global condition
    condition = 0
    debug.println("Restart","SYSTEM")

def get_uptime_seconds():
    uptime_ms = utime.ticks_ms() / 1000
    return round(uptime_ms, 2)

debug.println("System variables and definitions setup finished", "INIT")

# Automat Logik 

while True:
    key = keypad.get_key()

    if (condition == 0):
        
        # Boot Logik / Startup
        led_r.toggle()
        lcd.move_to(0,1)
        lcd.putstr("Starting...")
        debug.println("System starting...", "BOOT")
        utime.sleep(random.randint(2,6))
        led_r.toggle()
        led_g.toggle()
        
        lcd.clear()
        lcd.putstr("JJK Electronics")
        lcd.move_to(0,1)
        lcd.putstr("Booting...")
        debug.println("System booting...", "BOOT")
        utime.sleep(random.randint(2,6))
        led_r.toggle()
        
        lcd.clear()
        lcd.putstr("JJK Electronics")
        lcd.move_to(0,1)
        lcd.putstr("Finished!")
        debug.println(f"System start finished after {get_uptime_seconds()}s", "BOOT")
        utime.sleep(2)
        led_r.toggle()
        led_g.toggle()
        
        main_menu()

        # Zustand
        condition = 2

        debug.println(f"Condition changed to {condition}", "DEBUG")
        
    elif (condition == 1):
        
        # Error Zustand
        led_r.on()
        
        error_code = 404
        lcd.clear()
        lcd.putstr("Error Code: " + str(error_code))
        debug.println(f"The system encountered an error: {str(error_code)}", "ERROR")
        
        utime.sleep(2)
        main_menu()
        
        led_r.off()
        condition = 2

        debug.println(f"Condition changed to {condition}", "DEBUG")
        
    elif (condition == 2):
        
        # Automat wartet auf ersten Key

        if key in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
          
            lcd.clear()

            user_input = key
            lcd.move_to(0,0)
            lcd.putstr("AUSWAHL:")
            lcd.move_to(13,0)
            lcd.putstr(user_input)
            lcd.move_to(0,1)
            lcd.putstr("BETRIEBSBEREIT")

            debug.println(f"User input: {str(key)}", "INFO")

            condition = 3
            debug.println(f"Condition changed to {condition}", "DEBUG")

        elif (key == '*'):

            lcd.clear()
            lcd.putstr("DEBUG PASSWORD:")

            condition = 20
            debug.println("Debug enter_password_screen loaded", "INFO")
            debug.println(f"Condition changed to {condition}", "DEBUG")

    elif (condition == 3):

        # Automat wartet auf zweiten Key
        
        if key in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):

          user_input += key
          lcd.move_to(0,0)
          lcd.putstr("AUSWAHL:")
          lcd.move_to(13,0)
          lcd.putstr(user_input)
          lcd.move_to(0,1)
          lcd.putstr("BETRIEBSBEREIT")

          debug.println(f"User input: {str(key)}", "INFO")
          condition = 4
          debug.println(f"Condition changed to {condition}", "DEBUG")
        
        if (key == '#'):

          # Abbruch

          user_input = None
          lcd.clear()
          led_r.on()
          lcd.putstr("ABBRUCHTASTE GEDRÜCKT...")
          utime.sleep(1)
          lcd.clear()        

          debug.println("#: User canceled")
          main_menu()
          condition = 2
          debug.println(f"Condition changed to {condition}", "DEBUG")
    
    elif (condition == 4):

        # Automat wartet auf dritten Key

        if key in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):

          user_input += key
          lcd.move_to(0,0)
          lcd.putstr("AUSWAHL:")
          lcd.move_to(13,0)
          lcd.putstr(user_input)
          lcd.move_to(0,1)
          lcd.putstr("BETRIEBSBEREIT")

          debug.println(f"User input: {str(key)}", "INFO")
          debug.println(f"Full user input: {user_input}", "INFO")
          condition = 5
          debug.println(f"Condition changed to {condition}", "DEBUG")

        if (key == '#'):

          # Abbruch

          user_input = None
          lcd.clear()
          lcd.putstr("ABBRUCHTASTE GEDRÜCKT...")
          led_r.on()
          utime.sleep(1)
          lcd.clear()        

          debug.println("#: User canceled")
          main_menu()
          condition = 2
          debug.println(f"Condition changed to {condition}", "DEBUG")
      
    elif (condition == 5):

        # Nach Eingabe der 3 Keys

        if (key == '*'):

          # Bestätigung

          lcd.clear()
          product_id = user_input
          user_input = None

          debug.println(f"*: User confirmed input: {product_id}", "INFO")
          condition = 6
          debug.println(f"Condition changed to {condition}", "DEBUG")
        
        if (key == '#'):

          # Abbruch

          user_input = None
          lcd.clear()
          lcd.putstr("ABBRUCHTASTE GEDRÜCKT...")
          led_r.on()
          utime.sleep(1)
          lcd.clear()        

          debug.println("#: User canceled")
          main_menu()
          condition = 2
          debug.println(f"Condition changed to {condition}", "DEBUG")
        
        if key in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):

          # Abbruch

          user_input = None
          lcd.clear()
          lcd.putstr("EINGABE ZU LANG\nABBRUCH...")
          led_r.on()
          utime.sleep(1)
          lcd.clear()

          debug.println("To many characters", "ERROR")
          main_menu()
          condition = 2
          debug.println(f"Condition changed to {condition}", "DEBUG")
    
    elif (condition == 6):

          # Produkt Suche

        for product in config['products']:
            if product['item_id'] == product_id:
                product_price = product['price']
                product_name = product['name']
                product_motor = product['motor_id']
                print(product_name)
                break
            
        if product_price and product_name:
            
            # Prüfen ob Produkt noch in Stock
            
            lcd.clear()
            led_g.on()
            lcd.putstr(str(product_id) + ":")
            lcd.move_to(6,0)
            lcd.putstr("EUR")
            lcd.move_to(12,0)
            lcd.putstr(str(product_price))
            lcd.move_to(0,1)
            lcd.putstr(product_name)
            
            debug.println("Product found", "INFO")
            condition = 7
        else:

            lcd.clear()
            led_r.on()
            lcd.putstr(f"KEIN PRODUKT MIT ID '{product_id}' GEFUNDEN...")
            utime.sleep(1)
            main_menu()
            debug.println("Product not found", "ERROR")
            condition = 2
    elif (condition == 7):
        
        # Geld eingabe
        condition = 10

    elif (condition == 10):

        # Produkt Ausgabe
        lcd.clear()
        lcd.putstr("Bestellung wird ausgegeben...")
        utime.sleep(0.5)
        led_g.on()
        led_r.on()
        if (product_motor == "motor_001"):
            motor_001.eine_umdrehung()
        elif (product_motor == "motor_002"):
            motor_002.eine_umdrehung()
        
        led_r.off()
        led_g.off()
        condition = 2
        main_menu()


    elif (condition == 20):

        # Debug Password enter
        print()


