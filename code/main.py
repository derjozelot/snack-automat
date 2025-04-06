#
# Süßgkeiten Automat von Jakob F. Jonas O. und Karim A.
# Wir haben uns dazu entschieden die Variablen und Backend benannten Funktionen aus Simplizität auf Englisch zu benennen!
#
# JJK Electronics©

# Zum starten: Einfach 3 zeichige Item Nummer eingeben.
# 4 Zeichen: Abbruch
# '#': Abbruch
# '*': Bestätigen

# Es gibt einige geheime Codes die man eingeben kann, die auch in der configuration.json geändert werden können


from time import sleep_ms
from machine import I2C, Pin
from machine_i2c_lcd import I2cLcd
from DIYables_Pico_Keypad import Keypad

import debug
import utime
import random
import json
import jozelot

# Hardware Setup

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

# Produkt Variablen

product_id = None
product_name = None
product_price = None
product_slot = None

debug.println("Setup product variables")

# Software Setup

with open('configuration.json') as configuration:
    config = json.load(configuration)
    configuration.close()
    print(config)

# Automat Variablen

condition = 0 # Startzustand | condition = Zustand
user_input = None
error_code = None

debug.println("Setup automat variables")

def main_menu():
  lcd.clear()
  lcd.move_to(2,0)
  lcd.putstr("Willkommen!")
  lcd.move_to(0,1)
  lcd.putstr("Bitte w\xE1hlen...")        
  debug.println("Main menu")

def restart():
    global condition
    condition = 0
    debug.println("Boot: Restart")

# Automat Logik 
while True:
    key = keypad.get_key()

    if (condition == 0):
        
        # Boot Logik / Startup
        
        lcd.move_to(0,1)
        lcd.putstr("Starting...")
        debug.println("Boot: Starting...")
        utime.sleep(random.randint(2,6))
        
        lcd.clear()
        lcd.putstr("JJK Electronics")
        lcd.move_to(0,1)
        lcd.putstr("Booting...")
        debug.println("Boot: Booting...")
        utime.sleep(random.randint(2,6))
        
        lcd.clear()
        lcd.putstr("JJK Electronics")
        lcd.move_to(0,1)
        lcd.putstr("Finished!")
        debug.println("Boot: Finished!")
        utime.sleep(2)
        
        main_menu()

        # Zustand
        condition = 2
        
    elif (condition == 1):
        
        # Error Zustand
        
        error_code = 404
        lcd.clear()
        lcd.putstr("Error Code: " + str(error_code))
        debug.println("Error: " + str(error_code))
        
        utime.sleep(2)
        main_menu()
        condition = 2
        
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

          debug.println("Condition 3")
          condition = 3
    
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

          debug.println("Condition 4")
          condition = 4
        
        if (key == '#'):

          # Abbruch

          user_input = None
          lcd.clear()
          lcd.putstr("ABBRUCH...")
          utime.sleep(1)
          lcd.clear()        

          debug.println("Pressed: # | Condition 2")
          main_menu()
          condition = 2
    
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

          debug.println("Condition 5")
          condition = 5

        if (key == '#'):

          # Abbruch

          user_input = None
          lcd.clear()
          lcd.putstr("ABBRUCH...")
          utime.sleep(1)
          lcd.clear()        

          debug.println("Pressed: # | Condition 2")
          main_menu()
          condition = 2
      
    elif (condition == 5):

        # Nach Eingabe der 3 Keys

        if (key == '*'):

          # Bestätigung

          lcd.clear()
          product_id = user_input
          user_input = None

          debug.println("Pressed: * | Condition 6")
          condition = 6
        
        if (key == '#'):

          # Abbruch

          user_input = None
          lcd.clear()
          lcd.putstr("ABBRUCH...")
          utime.sleep(1)
          lcd.clear()        

          debug.println("Pressed: # | Condition 2")
          main_menu()
          condition = 2
        
        if key in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):

          # Abbruch

          user_input = None
          lcd.clear()
          lcd.putstr("ABBRUCH...")
          utime.sleep(1)
          lcd.clear()

          debug.println("False user input | Condition 2")
          main_menu()
          condition = 2
    
    elif (condition == 6):

          # Produkt Suche

        for product in config['products']:
            if product['item_id'] == product_id:
                product_price = product['price']
                product_name = product['name']
                print(product_name)
                break
            
        if product_price and product_name:
            
            lcd.clear()
            lcd.putstr(str(product_id) + ":")
            lcd.move_to(6,0)
            lcd.putstr("EUR")
            lcd.move_to(12,0)
            lcd.putstr(str(product_price))
            lcd.move_to(0,1)
            lcd.putstr(product_name)
            
            debug.println("Product found | Condition 7")
            condition = 7
        else:
            
            main_menu()
            debug.println("Product not found | Condition 2")
            condition = 2
    elif (condition == 7):
        
        # Geld eingabe
        print()
