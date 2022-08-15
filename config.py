import subprocess


def configure():
    subprocess.call("sudo modprobe w1-gpio", shell=True)
    subprocess.call("sudo modprobe w1-therm", shell=True)
