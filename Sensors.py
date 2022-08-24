# import RPi.GPIO as GPIO
import PressureTransducer


class Sensor:
    def __init__(self):
        pass

    def Temperature(self, unit="C"):
        return 20
        with open("/sys/bus/w1/devices/28-01186c811dff/temperature") as temp:
            temp = int(temp.read()) / 1000
        if unit == "F":
            return (temp * 9 / 5) + 32
        return temp

    def Static_Pressure(self):
        return 5000000

    def Dynamic_Pressure(self):
        pass
