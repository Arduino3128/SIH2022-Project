import RPi.GPIO as GPIO
from HX711 import *
import sys, os

dout = 5
sck = 6

try:
    hx = SimpleHX711(dout, sck, 1, 0)
except GpioException:
    print("Failed to connect to HX711 chip", file=sys.stderr)
    sys.exit(os.EX_UNAVAILABLE)
except TimeoutException:
    print("Failed to connect to HX711 chip", file=sys.stderr)
    sys.exit(os.EX_UNAVAILABLE)

samples = 15

while True:
    Values = hx.read(Options(samples))
    print(f"Values: {Values}")
