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
from JJK_StepperLib import StepperMotor
from JJK_LedLib import LedStrip

import debug
import utime
import random
import json

debug.save_log()

debug.println("Imports loaded", "INIT")

OS_Version = "1.4"

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

motor_001 = StepperMotor(9,10,11,12)
motor_002 = StepperMotor(13,14,15,16)

led_front = LedStrip(19, 17)
led_001 = LedStrip(20, 20)
led_002 = LedStrip(21, 20)

debug.println("Hardware setup finished", "INIT")

# Produkt Variablen

product_id = None
product_name = None
product_price = None
product_motor = None
product_stock = None

debug.println("Start variables setup finished", "INIT")

# Software Setup

with open('assets/configuration.json') as configuration:
    config = json.load(configuration)
    configuration.close()
    print(config)

with open('assets/stock.json') as stock_data:
    stock = json.load(stock_data)
    stock_data.close()
    print(stock_data)

with open('assets/lang.json', encoding='utf-8') as lang_data:
    lang = json.load(lang_data)
    lang_data.close()
    print(lang_data)

# Automat Variablen

condition = config['settings']['standard_condition'] # condition = Zustand
user_input = None
error_code = None
key = None

pay_start_time = None
pay_max_time = None
current_pay_time = None

debug.println("Setup automat variables", "INIT")

def main_menu():
    led_front.strip_white(stock['led_brightness']['led_front'])
    led_001.strip_white(stock['led_brightness']['led_001'])
    led_002.strip_white(stock['led_brightness']['led_002'])
    led_g.off()
    led_r.off()
    lcd.clear()
    lcd.move_to(2,0)
    lcd.putstr(lang['welcome'])
    lcd.move_to(0,1)
    lcd.putstr(lang['please_choose'])        
    debug.println("Main menu loaded")

def led_strips_off():
    led_front.off()
    led_001.off()
    led_002.off()

def restart():
    global condition
    
    led_strips_off()
    condition = 0
    debug.println("Restart","SYSTEM")

def get_uptime_seconds():
    uptime_ms = utime.ticks_ms() / 1000
    return round(uptime_ms, 2)

def decrease_stock(item_id):
    for product in stock["stock"]:
        if product["item_id"] == item_id:
            if product["stock"] > 0:
                product["stock"] -= 1

                with open("assets/stock.json", "w") as file:
                    json.dump(stock, file)

                return True
            else:
                return False
            
    return False


def increase_stock(item_id):
    for product in stock["stock"]:
        if product["item_id"] == item_id:
            if product["stock"] >= 0:
                product["stock"] += 1

                with open("assets/stock.json", "w") as file:
                    json.dump(stock, file)

                return True
            else:
                return False
            
    return False

def decrease_brightness(led_id):
    if led_id == "led_front":
        if stock['led_brightness']['led_front'] > 0:
            stock['led_brightness']['led_front'] = round(stock['led_brightness']['led_front'] - 0.1, 1)
        
        with open("assets/stock.json", "w") as file:
            json.dump(stock, file)

        return True
    elif led_id == "led_001":
        if stock['led_brightness']['led_001'] > 0:
            stock['led_brightness']['led_001'] = round(stock['led_brightness']['led_002'] - 0.1, 1)
        
        with open("assets/stock.json", "w") as file:
            json.dump(stock, file)

        return True
    elif led_id == "led_002":
        if stock['led_brightness']['led_002'] > 0:
            stock['led_brightness']['led_002'] = round(stock['led_brightness']['led_002'] - 0.1, 1)
        
        with open("assets/stock.json", "w") as file:
            json.dump(stock, file)

        return True

    return False

def increase_brightness(led_id):
    if led_id == "led_front":
        if stock['led_brightness']['led_front'] >= 0:
            stock['led_brightness']['led_front'] = round(stock['led_brightness']['led_front'] + 0.1, 1)
        
        with open("assets/stock.json", "w") as file:
            json.dump(stock, file)

        return True
    elif led_id == "led_001":
        if stock['led_brightness']['led_001'] >= 0:
            stock['led_brightness']['led_001'] = round(stock['led_brightness']['led_001'] + 0.1, 1)
        
        with open("assets/stock.json", "w") as file:
            json.dump(stock, file)

        return True
    elif led_id == "led_002":
        if stock['led_brightness']['led_002'] >= 0:
            stock['led_brightness']['led_002'] = round(stock['led_brightness']['led_002'] + 0.1, 1)
        
        with open("assets/stock.json", "w") as file:
            json.dump(stock, file)

        return True

    return False

def start_led_animation():
    led_001.led_colour(1, 255, 255, 255, stock['led_brightness']['led_001'])
    led_002.led_colour(1, 255, 255, 255, stock['led_brightness']['led_002'])
    utime.sleep(0.1)
    led_001.led_colour(2, 255, 255, 255, stock['led_brightness']['led_001'])
    led_002.led_colour(2, 255, 255, 255, stock['led_brightness']['led_002'])
    utime.sleep(0.1)
    led_001.led_colour(3, 255, 255, 255, stock['led_brightness']['led_001'])
    led_002.led_colour(3, 255, 255, 255, stock['led_brightness']['led_002'])
    utime.sleep(0.1)
    led_001.led_colour(4, 255, 255, 255, stock['led_brightness']['led_001'])
    led_002.led_colour(4, 255, 255, 255, stock['led_brightness']['led_002'])
    utime.sleep(0.1)
    led_001.led_colour(5, 255, 255, 255, stock['led_brightness']['led_001'])
    led_002.led_colour(5, 255, 255, 255, stock['led_brightness']['led_002'])
    utime.sleep(0.1)
    led_001.led_colour(6, 255, 255, 255, stock['led_brightness']['led_001'])
    led_002.led_colour(6, 255, 255, 255, stock['led_brightness']['led_002'])
    utime.sleep(0.1)
    led_001.led_colour(7, 255, 255, 255, stock['led_brightness']['led_001'])
    led_002.led_colour(7, 255, 255, 255, stock['led_brightness']['led_002'])
    utime.sleep(0.1)
    led_001.led_colour(8, 255, 255, 255, stock['led_brightness']['led_001'])
    led_002.led_colour(8, 255, 255, 255, stock['led_brightness']['led_002'])
    utime.sleep(0.1)
    led_001.led_colour(9, 255, 255, 255, stock['led_brightness']['led_001'])
    led_002.led_colour(9, 255, 255, 255, stock['led_brightness']['led_002'])
    utime.sleep(0.1)
    led_001.led_colour(10, 255, 255, 255, stock['led_brightness']['led_001'])
    led_002.led_colour(10, 255, 255, 255, stock['led_brightness']['led_002'])
    utime.sleep(0.1)
    led_001.led_colour(11, 255, 255, 255, stock['led_brightness']['led_001'])
    led_002.led_colour(11, 255, 255, 255, stock['led_brightness']['led_002'])
    utime.sleep(0.1)
    led_001.led_colour(12, 255, 255, 255, stock['led_brightness']['led_001'])
    led_002.led_colour(12, 255, 255, 255, stock['led_brightness']['led_002'])
    utime.sleep(0.1)
    led_001.led_colour(13, 255, 255, 255, stock['led_brightness']['led_001'])
    led_002.led_colour(13, 255, 255, 255, stock['led_brightness']['led_002'])
    utime.sleep(0.1)
    led_001.led_colour(14, 255, 255, 255, stock['led_brightness']['led_001'])
    led_002.led_colour(14, 255, 255, 255, stock['led_brightness']['led_002'])
    utime.sleep(0.05)

    led_front.led_colour(1, 255, 255, 255, stock['led_brightness']['led_front'])
    led_front.led_colour(17, 255, 255, 255, stock['led_brightness']['led_front'])
    utime.sleep(0.05)
    led_front.led_colour(2, 255, 255, 255, stock['led_brightness']['led_front'])
    led_front.led_colour(16, 255, 255, 255, stock['led_brightness']['led_front'])
    utime.sleep(0.05)
    led_front.led_colour(3, 255, 255, 255, stock['led_brightness']['led_front'])
    led_front.led_colour(15, 255, 255, 255, stock['led_brightness']['led_front'])
    utime.sleep(0.05)
    led_front.led_colour(4, 255, 255, 255, stock['led_brightness']['led_front'])
    led_front.led_colour(14, 255, 255, 255, stock['led_brightness']['led_front'])
    utime.sleep(0.05)
    led_front.led_colour(5, 255, 255, 255, stock['led_brightness']['led_front'])
    led_front.led_colour(13, 255, 255, 255, stock['led_brightness']['led_front'])
    utime.sleep(0.05)
    led_front.led_colour(6, 255, 255, 255, stock['led_brightness']['led_front'])
    led_front.led_colour(12, 255, 255, 255, stock['led_brightness']['led_front'])
    utime.sleep(0.05)
    led_front.led_colour(7, 255, 255, 255, stock['led_brightness']['led_front'])
    led_front.led_colour(11, 255, 255, 255, stock['led_brightness']['led_front'])
    utime.sleep(0.05)
    led_front.led_colour(7, 255, 255, 255, stock['led_brightness']['led_front'])
    led_front.led_colour(11, 255, 255, 255, stock['led_brightness']['led_front'])
    utime.sleep(0.05)
    led_front.led_colour(8, 255, 255, 255, stock['led_brightness']['led_front'])
    led_front.led_colour(10, 255, 255, 255, stock['led_brightness']['led_front'])
    utime.sleep(0.05)
    led_front.led_colour(9, 255, 255, 255, stock['led_brightness']['led_front'])
    utime.sleep(0.05)
    


led_strips_off()
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
        lcd.putstr(lang['company_name'])
        lcd.move_to(0,1)
        lcd.putstr("Booting...")
        debug.println("System booting...", "BOOT")
        utime.sleep(random.randint(2,6))
        led_r.toggle()
        
        lcd.clear()
        lcd.putstr(lang['company_name'])
        lcd.move_to(0,1)
        lcd.putstr("Finished!")
        debug.println(f"System start finished after {get_uptime_seconds()}s", "BOOT")
        utime.sleep(2)
        led_r.toggle()
        led_g.toggle()
        

        # Zustand
        condition = 1

        debug.println(f"Condition changed to {condition}", "DEBUG")
    
    elif (condition == 1):
    
        start_led_animation()
        condition = 2
        debug.println(f"Condition changed to {condition}", "DEBUG")
        main_menu()
        
    elif (condition == 2):
        
        # Automat wartet auf ersten Key

        if key in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
          
            lcd.clear()
            led_front.strip_colour(255, 180, 5, stock['led_brightness']['led_front'])

            user_input = key
            lcd.move_to(0,0)
            lcd.putstr(lang['selection'])
            lcd.move_to(13,0)
            lcd.putstr(user_input)
            lcd.move_to(0,1)
            lcd.putstr(lang['ready'])

            debug.println(f"User input: {str(key)}", "INFO")

            condition = 3
            debug.println(f"Condition changed to {condition}", "DEBUG")

        elif (key == '*'):

            lcd.clear()
            lcd.putstr("DEBUG PASSWORD:")

            led_front.strip_gradient((250, 35, 27),(250, 127, 27))
            led_001.strip_gradient((250, 35, 27),(250, 127, 27))
            led_002.strip_gradient((250, 35, 27),(250, 127, 27))
            condition = 20
            debug.println("Debug enter_password_screen loaded", "INFO")
            debug.println(f"Condition changed to {condition}", "DEBUG")

    elif (condition == 3):

        # Automat wartet auf zweiten Key
        
        if key in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):

          user_input += key
          lcd.move_to(0,0)
          lcd.putstr(lang['selection'])
          lcd.move_to(13,0)
          lcd.putstr(user_input)
          lcd.move_to(0,1)
          lcd.putstr(lang['ready'])

          debug.println(f"User input: {str(key)}", "INFO")
          condition = 4
          debug.println(f"Condition changed to {condition}", "DEBUG")
        
        if (key == '#'):

          # Abbruch

          user_input = None
          lcd.clear()
          led_r.on()
          led_front.strip_red(stock['led_brightness']['led_front'])
          lcd.putstr(lang['cancel_pressed'])
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
          lcd.putstr(lang['selection'])
          lcd.move_to(13,0)
          lcd.putstr(user_input)
          lcd.move_to(0,1)
          lcd.putstr(lang['ready'])

          debug.println(f"User input: {str(key)}", "INFO")
          debug.println(f"Full user input: {user_input}", "INFO")
          condition = 5
          debug.println(f"Condition changed to {condition}", "DEBUG")

        if (key == '#'):

          # Abbruch

          user_input = None
          lcd.clear()
          led_front.strip_red(stock['led_brightness']['led_front'])
          lcd.putstr(lang['cancel_pressed'])
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
          led_front.strip_red(stock['led_brightness']['led_front'])
          lcd.putstr(lang['cancel_pressed'])
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
          led_front.strip_red(stock['led_brightness']['led_front'])
          lcd.putstr(lang['input_too_long'])
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
                break
            
        for product in stock['stock']:
            if product['item_id'] == product_id:
                product_stock = product['stock']
                break

            
        if (product_price is not None and product_name is not None and product_motor is not None):
            
            debug.println(f"Product with ID '{product_id}' found. Name: '{product_name}', Price: '{product_price}', Motor: '{product_motor}'", "INFO")
           
            if (product_stock > 0):
                # Prüfen ob Produkt noch in Stock
            
                debug.println(f"Product in stock: {product_stock}", "INFO")
                led_front.strip_white(stock['led_brightness']['led_front'])
                lcd.clear()
                led_g.on()
                lcd.putstr(str(product_id) + ":")
                lcd.move_to(6,0)
                lcd.putstr(lang['current'])
                lcd.move_to(12,0)
                lcd.putstr(str(product_price))
                lcd.move_to(0,1)
                lcd.putstr(product_name)

                if (product_motor == "motor_001"):
                    led_001.strip_green(stock['led_brightness']['led_001'])
                    led_002.strip_white(stock['led_brightness']['led_002'] * 0.5)
                elif (product_motor == "motor_002"):
                    led_002.strip_green(stock['led_brightness']['led_002'])
                    led_001.strip_white(stock['led_brightness']['led_001'] * 0.5)
            
                pay_multiplier = config['settings']['max_time_at_pay']
                pay_start_time = utime.ticks_ms()
                pay_max_time = pay_start_time + pay_multiplier
                
                condition = 7
                debug.println(f"Condition changed to {condition}", "DEBUG")
            else:
                lcd.clear()
                led_r.on()
                led_front.strip_white(stock['led_brightness']['led_front'])
                lcd.putstr(lang['product_not_in_stock'])
                debug.println(f"Product not in stock", "ERROR")

                if (product_motor == "motor_001"):
                    led_001.strip_red(stock['led_brightness']['led_001'])
                    led_002.strip_white(stock['led_brightness']['led_002'] * 0.5)
                elif (product_motor == "motor_002"):
                    led_002.strip_red(stock['led_brightness']['led_front'])
                    led_001.strip_white(stock['led_brightness']['led_front'] * 0.5)

                utime.sleep(2)
            
                condition = 2
                debug.println(f"Condition changed to {condition}", "DEBUG")
                main_menu()
        else:
            
            lcd.clear()
            led_front.strip_red(stock['led_brightness']['led_front'])
            led_r.on()
            lcd.putstr(f"ID {product_id}")
            lcd.move_to(0,1)
            lcd.putstr(lang['product_not_exist'])

            utime.sleep(2)
            debug.println(f"Product with ID '{product_id}' not found", "ERROR")
            
            condition = 2
            debug.println(f"Condition changed to {condition}", "DEBUG")
            main_menu()
            
    elif (condition == 7):
        
        current_pay_time = utime.ticks_ms()
        
        # Geld eingabe
        led_front.strip_white(stock['led_brightness']['led_front'])
        debug.println(f"Waiting for pay...", "INFO")
        
        if (key == "*"):

            pay_start_time = None
            pay_max_time = None
            current_pay_time = None
            
            lcd.clear()
            led_g.on()
            lcd.putstr(str(product_id) + ":")
            lcd.move_to(6,0)
            lcd.putstr(lang['current'])
            lcd.move_to(12,0)
            lcd.putstr(str(product_price))
            lcd.move_to(0,1)
            lcd.putstr(lang['product_payed'])
            
            utime.sleep(2)
            
            debug.println(f"Product with ID '{product_id}' was bought...", "INFO")
            condition = 10
            debug.println(f"Condition changed to {condition}", "DEBUG")
        
        if (current_pay_time == pay_max_time):
            
            lcd.clear()
            lcd.putstr(lang['waited_too_long'])
            if (product_motor == "motor_001"):
                led_001.strip_red(stock['led_brightness']['led_001'])
                led_002.strip_white(stock['led_brightness']['led_002'] * 0.5)
            elif (product_motor == "motor_002"):
                led_002.strip_red(stock['led_brightness']['led_002'])
                led_001.strip_white(stock['led_brightness']['led_f001'] * 0.5)
            
            utime.sleep(2)            
            
            condition = 2
            main_menu()
        
    elif (condition == 10):

        # Produkt Ausgabe
        lcd.clear()
        lcd.putstr(lang['product_issuing'])
        debug.println(f"Product is being issued", "INFO")
        utime.sleep(0.5)
        led_g.on()
        led_r.on()
        
        if (product_motor == "motor_001"):
            led_001.strip_colour(255, 180, 5, stock['led_brightness']['led_001'])
            motor_001.one_rotate()
        elif (product_motor == "motor_002"):
            led_002.strip_colour(255, 180, 5, stock['led_brightness']['led_002'])
            motor_002.one_rotate()
        else:
            debug.println(f"Error with {product_motor}", "ERROR")
            lcd.clear()
            lcd.putstr("Machine run into error with motor")
            utime.sleep(2)
            lcd.clear()
            lcd.putstr("Machine will restart...")
            utime.sleep(2)
            restart()

        debug.println(f"Product successfully issued", "INFO")
        debug.println(f"New stock: '{product_stock - 1}'", "INFO")
        
        decrease_stock(product_id)
        
        led_r.off()
        led_g.off()
        
        condition = 2
        main_menu()

    elif (condition == 20):
        
        # Debug PW Enter
        
        if (key == '#'):
            lcd.clear()
            lcd.putstr(lang['cancel_pressed'])
            led_front.strip_red(stock['led_brightness']['led_front'])
            led_r.on()
            
            utime.sleep(2)
            
            condition = 2
            main_menu()
        
        elif key in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            
            user_input = key
            lcd.move_to(0,1)
            lcd.putstr(user_input)
            condition = 21
            
    elif (condition == 21):
        
        if (key == '#'):
            lcd.clear()
            led_front.strip_red(stock['led_brightness']['led_front'])
            lcd.putstr(lang['cancel_pressed'])
            led_r.on()
            utime.sleep(2)
            
            condition = 2
            main_menu()
        
        elif key in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            
            lcd.clear()
            lcd.putstr("DEBUG PASSWORD:")
            
            user_input += key
            lcd.move_to(0,1)
            lcd.putstr(user_input)
            condition = 22

    elif (condition == 22):
        
        if (key == '#'):
            lcd.clear()
            led_front.strip_red(stock['led_brightness']['led_front'])
            lcd.putstr(lang['cancel_pressed'])
            led_r.on()
            
            utime.sleep(2)
            
            condition = 2
            main_menu()
        
        elif key in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            
            user_input += key
            lcd.move_to(0,1)
            lcd.putstr(user_input)
            condition = 23
            
    elif (condition == 23):
        
        if (key == '#'):
            lcd.clear()
            led_front.strip_red(stock['led_brightness']['led_front'])
            lcd.putstr(lang['cancel_pressed'])
            led_r.on()
            utime.sleep(2)
            
            condition = 2
            main_menu()
        
        elif key in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            
            lcd.clear()
            lcd.putstr("DEBUG PASSWORD:")
            
            user_input += key
            lcd.move_to(0,1)
            lcd.putstr(user_input)
            condition = 24
    
    elif (condition == 24):
        
        if (key == '#'):
            lcd.clear()
            led_front.strip_red(stock['led_brightness']['led_front'])
            lcd.putstr(lang['cancel_pressed'])
            led_r.on()
            utime.sleep(2)
            
            condition = 2
            main_menu()
        
        elif key in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            
            lcd.clear()
            lcd.putstr("DEBUG PASSWORD:")
            
            user_input += key
            lcd.move_to(0,1)
            lcd.putstr(user_input)
            condition = 26
    
    elif (condition == 26):
        
        if (key == '#'):
            led_front.strip_white(stock['led_brightness']['led_front'])
            lcd.clear()
            lcd.putstr(lang['cancel_pressed'])
            led_r.on()
            utime.sleep(2)
            
            condition = 2
            main_menu()
        
        elif key in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            
            lcd.clear()
            led_front.strip_red(stock['led_brightness']['led_front'])
            lcd.putstr(lang['input_too_long'])
            led_r.on()
            utime.sleep(2)
            
            condition = 2
            main_menu()
        
        elif (key == '*'):
            
            debug_code = config["codes"]["debug_mode"]
            
            if (user_input == debug_code): # Debug Mode entered
                led_front.strip_gradient((2, 138, 191),(2, 204, 123))
                lcd.clear()
                lcd.putstr("[Debug-Mode]")
                lcd.move_to(0,1)
                lcd.putstr("Stock Settings")
                lcd.move_to(15,1)
                lcd.putstr("<")
                condition = 30
            
            else:
                lcd.clear()
                lcd.putstr(lang['password_incorrect'])
                utime.sleep(2)
                condition = 2
                main_menu()
    
    elif (condition == 30): # Start Zustand des Debugs
        if (key == "#"): # Zurück ins Main Menu
            lcd.clear()
            led_front.strip_red(stock['led_brightness']['led_front'])
            lcd.putstr(lang['cancel_pressed'])
            led_r.on()
            utime.sleep(2)
            
            condition = 2
            main_menu()
        
        elif (key == "8"): # Eins weiter runter im Main menu
                lcd.clear()
                lcd.putstr("Stock Settings")
                lcd.move_to(0,1)
                lcd.putstr("LED Settings")
                lcd.move_to(15,1)
                lcd.putstr("<")
                condition = 32
        
        elif (key == "*"): # Enter Stock Settings
                for product in stock['stock']:
                    if product['item_id'] == "001":
                        product_stock = product['stock']
                        break
                lcd.clear()
                lcd.putstr("[Stock Settings]")
                lcd.move_to(0,1)
                lcd.putstr(f"Slot_001   {product_stock}")
                lcd.move_to(15,1)
                lcd.putstr("<")
                condition = 31
    
    elif (condition == 31): # Stock Settings
        if (key == "#"): # Zurück ins Debug Menu
            lcd.clear()
            lcd.putstr("[Debug-Mode]")
            lcd.move_to(0,1)
            lcd.putstr("Stock Settings")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 30
        
        elif (key == "8"): # Stock weiter runter
            
            for product in stock['stock']:
                if product['item_id'] == "001":
                    product_stock = product['stock']
                    break
                
            for product in stock['stock']:
                if product['item_id'] == "002":
                    product_stock2 = product['stock']
                    break
            
            lcd.clear()
            lcd.putstr(f"Slot_001   {product_stock}")
            lcd.move_to(0,1)
            lcd.putstr(f"Slot_002   {product_stock2}")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 33
        
        elif (key == "*"):
                lcd.clear()
                lcd.putstr("[Stock Settings]")
                lcd.move_to(0,1)
                lcd.putstr(f"Slot_001   {product_stock}")
                lcd.move_to(14,1)
                lcd.putstr("<")
                condition = 48         
    
    elif (condition == 33): # Stock Settings unten
        if (key == "#"): # Zurück ins Debug Menu
            lcd.clear()
            lcd.putstr("[Debug-Mode]")
            lcd.move_to(0,1)
            lcd.putstr("Stock Settings")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 30
        
        elif (key == "2"): # Stock weiter hoch
            for product in stock['stock']:
                if product['item_id'] == "001":
                    product_stock = product['stock']
                    break
            lcd.clear()
            lcd.putstr("[Stock Settings]")
            lcd.move_to(0,1)
            lcd.putstr(f"Slot_001   {product_stock}")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 31
        
        elif (key == "*"):
            for product in stock['stock']:
                if product['item_id'] == "001":
                    product_stock = product['stock']
                    break
            for product in stock['stock']:
                if product['item_id'] == "002":
                    product_stock2 = product['stock']
                    break
                lcd.clear()
                lcd.putstr(f"Slot_001   {product_stock}")
                lcd.move_to(0,1)
                lcd.putstr(f"Slot_002   {product_stock2}")
                lcd.move_to(14,1)
                lcd.putstr("<")
                condition = 49           
            
    
    elif (condition == 32): # LED Settings unten
        if (key == "#"):
            lcd.clear()
            led_front.strip_red(0.5)
            lcd.putstr(lang['cancel_pressed'])
            led_r.on()
            utime.sleep(2)
            
            condition = 2
            main_menu()
        
        elif (key == "*"): # In LED Settings rein
            lcd.clear()
            lcd.putstr("[LED Settings]")
            lcd.move_to(0,1)
            lcd.putstr(f"Led_Front {stock['led_brightness']['led_front']}")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 43
            

        elif (key == "2"): # Zurück an Anfang des Debug Modes
            lcd.clear()
            lcd.putstr("[Debug-Mode]")
            lcd.move_to(0,1)
            lcd.putstr("Stock Settings")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 30
        
        elif (key == "8"): # Weiter runter
            lcd.clear()
            lcd.putstr("LED Settings")
            lcd.move_to(0,1)
            lcd.putstr("Rotate Motor")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 34

    elif (condition == 34): # Weiter runter
        if (key == "#"):
            lcd.clear()
            led_front.strip_red(0.5)
            lcd.putstr(lang['cancel_pressed'])
            led_r.on()
            utime.sleep(2)
            
            condition = 2
            main_menu()
        
        elif (key == "*"):
            lcd.clear()
            lcd.putstr("[Rotate Motor]")
            lcd.move_to(0,1)
            lcd.putstr("Motor_001")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 46

        elif (key == "2"):
            lcd.clear()
            lcd.putstr("Stock Settings")
            lcd.move_to(0,1)
            lcd.putstr("LED Settings")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 32

        elif (key == "8"):
            lcd.clear()
            lcd.putstr("Rotate Motor")
            lcd.move_to(0,1)
            lcd.putstr("Generel")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 36
    
    elif (condition == 36):
        if (key == "#"):
            lcd.clear()
            led_front.strip_red(0.5)
            lcd.putstr(lang['cancel_pressed'])
            led_r.on()
            utime.sleep(2)
            
            condition = 2
            main_menu()

        elif (key == "2"):
            lcd.clear()
            lcd.putstr("LED Settings")
            lcd.move_to(0,1)
            lcd.putstr("Motor Settings")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 32
        
        elif (key == "*"):
            lcd.clear()
            lcd.putstr("[Generel]")
            lcd.move_to(0,1)
            lcd.putstr(f"OS Version {OS_Version}")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 40
    
    elif (condition == 40):
        if (key == "#"):
            lcd.clear()
            lcd.putstr("[Debug-Mode]")
            lcd.move_to(0,1)
            lcd.putstr("Stock Settings")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 30
            
        elif (key == "8"):
            lcd.clear()
            lcd.putstr(f"OS Version {OS_Version}")
            lcd.move_to(0,1)
            lcd.putstr("Restart")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 42
    
    elif (condition == 42):
        if (key == "#"):
            lcd.clear()
            lcd.putstr("[Debug-Mode]")
            lcd.move_to(0,1)
            lcd.putstr("Stock Settings")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 30
        
        elif (key == "2"):
            lcd.clear()
            lcd.putstr("[Generel]")
            lcd.move_to(0,1)
            lcd.putstr(f"OS Version {OS_Version}")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 40
            
            
        if (key == "*"):
            restart()
    
    elif (condition == 43): # LED Settings innerhalb
        if (key == "#"): # Zurück ins Debug Menu
            lcd.clear()
            lcd.putstr("[Debug-Mode]")
            lcd.move_to(0,1)
            lcd.putstr("Stock Settings")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 30
            
        elif (key == "8"):
            lcd.clear()
            lcd.putstr(f"Led_Front {stock['led_brightness']['led_front']}")
            lcd.move_to(0,1)
            lcd.putstr(f"Led_001   {stock['led_brightness']['led_001']}")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 44
        
        elif (key == "*"):
            lcd.clear()
            lcd.putstr("[LED Settings]")
            lcd.move_to(0,1)
            lcd.putstr(f"Led_Front {stock['led_brightness']['led_front']}")
            lcd.move_to(14,1)
            lcd.putstr("<")
            condition = 50       
            
    elif (condition == 44): # LED Settings 2
        if (key == "#"): # Zurück ins Debug Menu
            lcd.clear()
            lcd.putstr("[Debug-Mode]")
            lcd.move_to(0,1)
            lcd.putstr("Stock Settings")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 30
        
        elif (key == "2"):
            lcd.clear()
            lcd.putstr("[LED Settings]")
            lcd.move_to(0,1)
            lcd.putstr(f"Led_Front {stock['led_brightness']['led_front']}")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 43
        
        elif (key == "8"):
            lcd.clear()
            lcd.putstr(f"Led_001   {stock['led_brightness']['led_001']}")
            lcd.move_to(0,1)
            lcd.putstr(f"Led_002   {stock['led_brightness']['led_002']}")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 45

        elif (key == "*"):
            lcd.clear()
            lcd.putstr(f"Led_Front {stock['led_brightness']['led_front']}")
            lcd.move_to(0,1)
            lcd.putstr(f"Led_001   {stock['led_brightness']['led_001']}")
            lcd.move_to(14,1)
            lcd.putstr("<")
            condition = 51
    
    elif (condition == 45): # LED Settings 3
        if (key == "#"): # Zurück ins Debug Menu
            lcd.clear()
            lcd.putstr("[Debug-Mode]")
            lcd.move_to(0,1)
            lcd.putstr("Stock Settings")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 30
        
        elif (key == "2"):
            lcd.clear()
            lcd.putstr(f"Led_Front {stock['led_brightness']['led_front']}")
            lcd.move_to(0,1)
            lcd.putstr(f"Led_001   {stock['led_brightness']['led_001']}")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 44

        elif (key == "*"):
            lcd.clear()
            lcd.putstr(f"Led_001   {stock['led_brightness']['led_001']}")
            lcd.move_to(0,1)
            lcd.putstr(f"Led_002   {stock['led_brightness']['led_002']}")
            lcd.move_to(14,1)
            lcd.putstr("<")
            condition = 52
        
    elif (condition == 46):
        if (key == "#"): # Zurück ins Debug Menu
            lcd.clear()
            lcd.putstr("[Debug-Mode]")
            lcd.move_to(0,1)
            lcd.putstr("Stock Settings")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 30         
        
        elif (key == "8"):
            lcd.clear()
            lcd.putstr("Motor_001")
            lcd.move_to(0,1)
            lcd.putstr("Motor_002")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 47
        
        elif (key == "*"):
            led_001.strip_green(0.5)
            led_002.strip_white(0.25)
            motor_001.one_rotate()
            led_001.strip_white(0.5)
            led_002.strip_white(0.5)
    
    elif (condition == 47): # Motor 002
        if (key == "#"): # Zurück ins Debug Menu
            lcd.clear()
            lcd.putstr("[Debug-Mode]")
            lcd.move_to(0,1)
            lcd.putstr("Stock Settings")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 30
        
        elif (key == "2"): # Motor 001
            lcd.clear()
            lcd.putstr("[Rotate Motor]")
            lcd.move_to(0,1)
            lcd.putstr("Motor_001")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 46
            
        elif (key == "*"):
            led_002.strip_green(0.5)
            led_001.strip_white(0.25)
            motor_002.one_rotate()
            led_002.strip_white(0.5)
            led_001.strip_white(0.5)
    
    elif (condition == 48):
        if (key == "#"):
            for product in stock['stock']:
                if product['item_id'] == "001":
                    product_stock = product['stock']
                    break

            lcd.clear()
            lcd.putstr("[Stock Settings]")
            lcd.move_to(0,1)
            lcd.putstr(f"Slot_001   {product_stock}")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 31
        
        elif (key == "*"):
            for product in stock['stock']:
                if product['item_id'] == "001":
                    product_stock = product['stock']
                    break
                

            lcd.clear()
            lcd.putstr("[Stock Settings]")
            lcd.move_to(0,1)
            lcd.putstr(f"Slot_001   {product_stock}")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 31
        
        elif (key == "2"):
            for product in stock['stock']:
                if product['item_id'] == "001":
                    product_stock = product['stock']
                    break
                

            
            increase_stock("001")
            lcd.clear()
            lcd.putstr("[Stock Settings]")
            lcd.move_to(0,1)
            lcd.putstr(f"Slot_001   {product_stock + 1}")
            lcd.move_to(14,1)
            lcd.putstr("<")
        
        elif (key == "8"):
            for product in stock['stock']:
                if product['item_id'] == "001":
                    product_stock = product['stock']
                    break
                

            decrease_stock("001")
            lcd.clear()
            lcd.putstr("[Stock Settings]")
            lcd.move_to(0,1)
            lcd.putstr(f"Slot_001   {product_stock - 1}")
            lcd.move_to(14,1)
            lcd.putstr("<")
            
    elif (condition == 49):
        if (key == "#"):
            for product in stock['stock']:
                if product['item_id'] == "001":
                    product_stock = product['stock']
                    break
                
            for product in stock['stock']:
                if product['item_id'] == "002":
                    product_stock2 = product['stock']
                    break

            lcd.clear()
            lcd.putstr(f"Slot_001   {product_stock}")
            lcd.move_to(0,1)
            lcd.putstr(f"Slot_002   {product_stock2}")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 33
        
        elif (key == "*"):
            for product in stock['stock']:
                if product['item_id'] == "001":
                    product_stock = product['stock']
                    break
                
            for product in stock['stock']:
                if product['item_id'] == "002":
                    product_stock2 = product['stock']
                    break
                

            lcd.clear()
            lcd.putstr(f"Slot_001   {product_stock}")
            lcd.move_to(0,1)
            lcd.putstr(f"Slot_002   {product_stock2}")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 33
        
        elif (key == "2"):
            for product in stock['stock']:
                if product['item_id'] == "001":
                    product_stock = product['stock']
                    break
                
            for product in stock['stock']:
                if product['item_id'] == "002":
                    product_stock2 = product['stock']
                    break
                

            
            increase_stock("002")
            lcd.clear()
            lcd.putstr(f"Slot_001   {product_stock}")
            lcd.move_to(0,1)
            lcd.putstr(f"Slot_002   {product_stock2 + 1}")
            lcd.move_to(14,1)
            lcd.putstr("<")
        
        elif (key == "8"):
            for product in stock['stock']:
                if product['item_id'] == "001":
                    product_stock = product['stock']
                    break
                
            for product in stock['stock']:
                if product['item_id'] == "002":
                    product_stock2 = product['stock']
                    break
                

            decrease_stock("002")
            lcd.clear()
            lcd.putstr(f"Slot_001   {product_stock}")
            lcd.move_to(0,1)
            lcd.putstr(f"Slot_002   {product_stock2 - 1}")
            lcd.move_to(14,1)
            lcd.putstr("<") 
            
    elif (condition == 50):
        if (key == "#"):

            lcd.clear()
            lcd.putstr("[LED Settings]")
            lcd.move_to(0,1)
            lcd.putstr(f"Led_Front {stock['led_brightness']['led_front']}")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 43
        
        elif (key == "*"):
            lcd.clear()
            lcd.putstr("[LED Settings]")
            lcd.move_to(0,1)
            lcd.putstr(f"Led_Front {stock['led_brightness']['led_front']}")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 43
        
        elif (key == "2"):
            
            increase_brightness("led_front")
            lcd.clear()
            lcd.putstr("[LED Settings]")
            lcd.move_to(0,1)
            lcd.putstr(f"Led_Front {stock['led_brightness']['led_front']}")
            lcd.move_to(14,1)
            lcd.putstr("<")
        
        elif (key == "8"):

            decrease_brightness("led_front")
            lcd.clear()
            lcd.putstr("[LED Settings]")
            lcd.move_to(0,1)
            lcd.putstr(f"Led_Front {stock['led_brightness']['led_front']}")
            lcd.move_to(14,1)
            lcd.putstr("<")

    elif (condition == 51):
        if (key == "#"):

            lcd.clear()
            lcd.putstr(f"Led_Front {stock['led_brightness']['led_front']}")
            lcd.move_to(0,1)
            lcd.putstr(f"Led_001   {stock['led_brightness']['led_001']}")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 44
        
        elif (key == "*"):
            lcd.clear()
            lcd.putstr(f"Led_Front {stock['led_brightness']['led_front']}")
            lcd.move_to(0,1)
            lcd.putstr(f"Led_001   {stock['led_brightness']['led_001']}")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 44
        
        elif (key == "2"):
            
            increase_brightness("led_001")
            lcd.clear()
            lcd.putstr(f"Led_Front {stock['led_brightness']['led_front']}")
            lcd.move_to(0,1)
            lcd.putstr(f"Led_001   {stock['led_brightness']['led_001']}")
            lcd.move_to(14,1)
            lcd.putstr("<")
        
        elif (key == "8"):

            decrease_brightness("led_001")
            lcd.clear()
            lcd.putstr(f"Led_Front {stock['led_brightness']['led_front']}")
            lcd.move_to(0,1)
            lcd.putstr(f"Led_001   {stock['led_brightness']['led_001']}")
            lcd.move_to(14,1)
            lcd.putstr("<")

    elif (condition == 52):
        if (key == "#"):

            lcd.clear()
            lcd.putstr(f"Led_001   {stock['led_brightness']['led_001']}")
            lcd.move_to(0,1)
            lcd.putstr(f"Led_002   {stock['led_brightness']['led_002']}")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 45
        
        elif (key == "*"):
            lcd.clear()
            lcd.putstr(f"Led_001   {stock['led_brightness']['led_001']}")
            lcd.move_to(0,1)
            lcd.putstr(f"Led_002   {stock['led_brightness']['led_002']}")
            lcd.move_to(15,1)
            lcd.putstr("<")
            condition = 45
        
        elif (key == "2"):
            
            increase_brightness("led_002")
            lcd.clear()
            lcd.putstr(f"Led_001   {stock['led_brightness']['led_001']}")
            lcd.move_to(0,1)
            lcd.putstr(f"Led_002   {stock['led_brightness']['led_002']}")
            lcd.move_to(14,1)
            lcd.putstr("<")
        
        elif (key == "8"):

            decrease_brightness("led_002")
            lcd.clear()
            lcd.putstr(f"Led_001   {stock['led_brightness']['led_001']}")
            lcd.move_to(0,1)
            lcd.putstr(f"Led_002   {stock['led_brightness']['led_002']}")
            lcd.move_to(14,1)
            lcd.putstr("<")