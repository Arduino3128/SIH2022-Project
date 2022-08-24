from pprint import pp
import numpy as np

from Refractometer import ImageProcessing
from Sensors import Sensor

sensor = Sensor()
image = ImageProcessing()


def density():
    refraction = image.refraction()
    pressure = sensor.Static_Pressure()
    if refraction == "Failed":
        return "Failed"
    brix = (1 - refraction) * 100
    print(brix)
    tempf = sensor.Temperature(unit="F")
    tempc = sensor.Temperature(unit="C")
    p = np.poly1d([182.4601, -775.6821, 1262.7794, -669.5622 - brix])
    value = complex(p.r[-1]).real  # Brix to density
    # value = (brix / (258.6 - ((brix / 258.2) * 227.1))) + 1  # Brix to density

    value += (
        1.313454
        - (0.132674 * tempf)
        + (2.057793e-3 * (tempf ** 2))
        - (2.627634e-6 * (tempf ** 3))
    ) / 1000  # Correction for Temperature

    c1 = 0.0000000005074
    c2 = 0.00000000000326
    c3 = 0.0000000000000416
    value += (
        1 + (c1 + c2 * tempc + c3 * (tempc ** 2)) * (pressure - 101325)
    ) / 1000  # Correction for Pressure
    return value
