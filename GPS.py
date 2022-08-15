from concurrent.futures import thread
import time
import serial
from threading import Thread

speed_kmph=lat_degmin=long_degmin=gps_quality=0
ThreadPool = []

class NEO6M:
    def __init__(self):
        pass

    def dms(self,coord):
        coord = str(coord)
        coord_deg = int(coord[0:coord.index(".")-2])
        coord_min = float(coord[coord.index(".")-2::])
        return (coord_deg,coord_min)

    def MTKsum(self,data):
        try:
            check = ord(data[1])
            for char in data[2:-3]:
                check ^= ord(char)
            check = hex(check).upper()
            if int(check[2::],base=16)==int(data.split("*")[-1],base=16):
                return "Verified"
            else:
                return "Failed" 
        except:
            return "Failed"        


    def handler(self):
        global speed_kmph,lat_degmin,long_degmin,gps_quality
        while (self.run and self.serial_conn.isOpen()):
            try:
                try:
                    data = str(self.serial_conn.readline().decode()).strip()
                except:
                    continue
                if self.MTKsum(data)=="Failed":
                    continue
                data = data.split(",")
                match data[0]:
                    case "$GPGSV":
                        msg_total = data[1] 
                        msg_num = data[2]
                        snr = data[7]

                    case "$GPGLL":
                        utc_timestamp = data[5]
                        gpgll_status = data[6]

                    case "$GPRMC":
                        gprmc_status = data[2]

                    case "$GPVTG":
                        speed_kots=data[5]
                        speed_kmph=data[7]

                    case "$GPGGA":
                        utc_position = data[1]
                        lat = data[2]
                        lat_dir = data[3]
                        long = data[4]
                        long_dir = data[5]
                        gps_quality = data[6]
                        sat_count = data[7]
                        HDOP = data[8]
                        altitude = data[9]
                        last_recv = data[13]
                        lat_degmin = self.dms(lat)
                        long_degmin = self.dms(long)

                    case "$GPGSA":
                        pass

                    case _:
                        pass
            except:
                pass

    def start(self, port, baudrate = 9600):
        global ThreadPool
        if ThreadPool==[]:
            try:
                self.serial_conn = serial.Serial(port, baudrate)
            except:
                return f"Failed to connect {port} at {baudrate} baudrate."
            self.thread = Thread(target=self.handler)
            self.run = True
            self.thread.start()
            ThreadPool.append(self.thread)
            return "OK"
    
    def stop(self):
        global ThreadPool
        if self.thread.is_alive():
            self.run = False
            self.thread.join()
        ThreadPool.remove(self.thread)
