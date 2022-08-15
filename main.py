import sys, time, config
from threading import Thread
from rich import print as pprint

import Overwatcher
from Sensors import Sensor
from Density import density
from Refractometer import ImageProcessing
from Navigation import GPS


# config.configure()  # Enable and start interface modules in Kernel.
image = ImageProcessing()
# image.calibrate()
# print(image.refraction())
gps = GPS()
gpsstat = gps.start("COM3", 9600)

if gpsstat != "OK":
    pprint(f"[red bold][MAIN THREAD] {gpsstat}[/red bold]")
    sys.exit()

GPSOThread = Thread(target=Overwatcher.GPSQuality, args=(5,))
Overwatcher.run = True
GPSOThread.start()

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
Overwatcher.run = False
gps.stop()
print(density())
# print(Sensor.Temperature())
