import time
from machine import Pin

coin_acceptor = Pin(0, Pin.IN, Pin.PULL_DOWN)

ENTPRELLZEIT_MS = 200

ZEITFENSTER_MS = 2000

pulses = 0
last_pulse_time = 0
start_time = 0

while True:
    impulse = coin_acceptor.value()
    now = time.ticks_ms()

    if pulses == 0 and impulse == 1:
        start_time = now
        last_pulse_time = now
        pulses += 1
        print("Impulse erkannt...")

    elif pulses > 0 and impulse == 1:
        if time.ticks_diff(now, last_pulse_time) > ENTPRELLZEIT_MS:
            pulses += 1
            last_pulse_time = now

    if pulses > 0 and time.ticks_diff(now, start_time) >= ZEITFENSTER_MS:

        if pulses == 1:
            betrag = 0.05
        elif pulses == 2:
            betrag = 0.10
        elif pulses == 3:
            betrag = 0.20
        elif pulses == 4:
            betrag = 0.50
        elif pulses == 5:
            betrag = 1.00
        elif pulses == 6:
            betrag = 2.00
        else:
            betrag = 0.00

        print("Impulsanzahl:", pulses)
        print("Erkannter Betrag: {:.2f} €".format(betrag))

        pulses = 0
        start_time = 0
        last_pulse_time = 0

    time.sleep_ms(10) 
