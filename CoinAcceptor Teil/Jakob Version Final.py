import time
from machine import Pin

geld_einwurf = Pin(16, Pin.IN, Pin.PULL_DOWN)
print("Drücken Sie den Knopf um mit dem Einwurf des Geldes zu beginnen.")
impulse = 0

while True:
    geld_impuls = geld_einwurf.value()  #überprüfung den buttonzustands

        
    if geld_impuls == 1:
        time.sleep(1)
        print("Warte auf Münzeingabe...")
        startzeit = time.ticks_ms()
        endzeit = 0

        
        while startzeit != 5000:
            geld_impuls = geld_einwurf.value()
            if geld_impuls == 1:    
                impulse = impulse + 1
                time.sleep(0.6)
            endzeit = time.ticks_ms()
            startzeit = endzeit - startzeit
        
        if impulse == 0:
            print("Die Zeit ist abgelaufen! Keine Eingabe erkannt!")
        elif impulse == 1:
            print("Sie haben 50 Cent eingeworfen!", "(",impulse, "Impuls(e))")
            impulse = 0
        elif impulse == 2:
            print("Sie haben 1 Euro eingeworfen!", "(",impulse, "Impuls(e))")
            impulse = 0
        elif impulse == 3:
            print("Sie haben 2 Euro eingeworfen!", "(",impulse, "Impuls(e))")
            impulse = 0
        else:
            print("Münze unzulässig! Impulse der Münze sind nicht bekannt!", "(",impulse, "Impuls(e))")
            impulse = 0