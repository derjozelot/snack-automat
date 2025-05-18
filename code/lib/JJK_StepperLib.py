from machine import Pin
import time

class StepperMotor:
    def __init__(self, pin1, pin2, pin3, pin4, step_delay=0.002):
        self.pins = [
            Pin(pin1, Pin.OUT),
            Pin(pin2, Pin.OUT),
            Pin(pin3, Pin.OUT),
            Pin(pin4, Pin.OUT)
        ]
        self.step_delay = step_delay
        self._reset_pins()

        self.step_sequence = [
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 1]
        ]

    def _reset_pins(self):
        for pin in self.pins:
            pin.value(0)

    def step(self, steps, direction=1):
        seq_len = len(self.step_sequence)
        for i in range(steps):
            seq = self.step_sequence[i % seq_len][::direction]
            for pin, val in zip(self.pins, seq):
                pin.value(val)
            time.sleep(self.step_delay)
        self._reset_pins()

    def one_rotation(self, direction=1):
        self.step(512, direction)


