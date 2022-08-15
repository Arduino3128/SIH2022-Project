from rich import print as pprint

import GPS as gp


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
    def __init__(self) -> None:
        pprint("[green bold][NAVIGATION] Compass module started![/green bold]")
