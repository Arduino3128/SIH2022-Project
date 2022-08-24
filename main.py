import sys, time, config
from tkinter.tix import Tree
from threading import Thread
from rich import print as pprint

import Overwatcher
from Sensors import Sensor
from Density import density
from Refractometer import ImageProcessing, Laser
from Navigation import GPS, Compass


config.configure()  # Enable and start interface modules in Kernel.

Overwatcher.start()
gps = GPS()
gpsstat = gps.start("/dev/serial0", 9600)
laser = Laser()
print(density())

if gpsstat != "OK":
    pprint(f"[red bold][MAIN THREAD] {gpsstat}[/red bold]")
    sys.exit()

while gps.quality() == 0:
    pprint("[yellow][MAIN THREAD] Waiting for a GPS fix[/yellow]")
    time.sleep(1)

if gps.quality() > 0:
    pprint("[green][MAIN THREAD] GPS Fixed![/green]")
    if gps.quality() == 1:
        pprint("[blue]3D GPS Fix[/blue]")
    else:
        pprint("[blue]Differential GPS Fix[/blue]")
    print(gps.coords()["lat"])
    print(gps.coords()["long"])
gps.stop()
# print(Sensor.Temperature())
Overwatcher.stop()
