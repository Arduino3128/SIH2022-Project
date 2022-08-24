from rich import print as pprint
import adafruit_lsm303dlh_mag
import board
from math import degrees, atan2

import GPS as gp

i2c = board.I2C()


class GPS:
    def __init__(self):
        pprint("[green bold][NAVIGATION] GPS Receiver started![/green bold]")
        self.gps = gp.NEO6M()

    def velocity(self):
        return gp.speed_kmph

    def coords(self):
        return {"lat": gp.lat_degmin, "long": gp.long_degmin}

    def quality(self):
        return int(gp.gps_quality)

    def start(self, port, baudrate=9600):
        return self.gps.start(port, baudrate)

    def stop(self):
        self.gps.stop()


class Compass:
    def __init__(self):
        pprint("[green bold][NAVIGATION] Compass module started![/green bold]")
        self.sensor = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)

    def vector_2_degrees(self, x, y):
        angle = degrees(atan2(y, x))
        if angle < 0:
            angle += 360
        return angle

    def get_heading(self):
        magnet_x, magnet_y, _ = self.sensor.magnetic
        return round(self.vector_2_degrees(magnet_x, magnet_y), 3)
