# This program will overlook all the components of the system.
from time import sleep
from rich import print as pprint
from threading import Thread

import GPS, Navigation, Density, PressureTransducer

run = False
pprint(
    "[green bold][OVERWATCHER] Overwatcher started![/green bold]\n[green]Monitoring System Health...\nWaiting for other modules to start...[/green]"
)


def PressureVerify():
    pass


def GPSQuality(refreshRate):
    sleep(2)
    while run:
        if GPS.ThreadPool == []:
            pprint("[red bold][OVERWATCHER] (GPS) No Thread Running[/red bold]")
        if GPS.gps_quality == 0:
            pprint("[yellow bold][OVERWATCHER] (GPS) Invalid GPS Fix[yellow bold]")
        sleep(refreshRate)


def RefractometerQuality():
    pass


def start():
    global run
    run = True
    GPSOThread = Thread(target=GPSQuality, args=(5,))
    GPSOThread.start()


def stop():
    global run
    run = False
