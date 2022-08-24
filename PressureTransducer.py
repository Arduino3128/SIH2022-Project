import RPi.GPIO as GPIO
from HX711 import *
import sys, os

dout = 5
sck = 6

try:
    hx = AdvancedHX711(dout, sck, 1, 0, Rate.HZ_10)
except GpioException:
    print("Failed to connect to HX711 chip", file=sys.stderr)
    sys.exit(os.EX_UNAVAILABLE)
except TimeoutException:
    print("Failed to connect to HX711 chip", file=sys.stderr)
    sys.exit(os.EX_UNAVAILABLE)

samples = 15


class Transducer:
    def __init__(self) -> None:
        pass

    def calibrate(self):
        print("Remove the pressure intially")
        self.offset = hx.read(Options(samples))

    def get_value(self):
        while True:
            values = hx.read(Options(samples))
            print(f"Values: {values-self.offset}")
