def temp():
    fhand = open("/sys/bus/w1/devices/28-01186c811dff/temperature")
    tempf = int(fhand.read()) / 1000
    fhand.close()
    return tempf
