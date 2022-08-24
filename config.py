import subprocess
import os


def configure():
    subprocess.call("sudo modprobe w1-gpio", shell=True)
    subprocess.call("sudo modprobe w1-therm", shell=True)
    subprocess.call("sudo chmod 777 /dev/serial0", shell=True)
    subprocess.call("sudo chown pi:pi /dev/serial0", shell=True)
