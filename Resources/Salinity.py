from Sensors import Sensor
from Refractometer import ImageProcessing

# RT is the Reading temperature, CT is the Calibrated temperature. 20 in "at" is the calibrated temperature at which the Device was factory calibrated!!

image = ImageProcessing()
sensor = Sensor()


def salinity(ct=25):
    refraction = image.refraction()
    if refraction == "Failed":
        return "Failed"
    brix = (1 - refraction) * 100
    brix = 6.3
    rt = sensor.Temperature()
    at = 20 + rt - ct
    af = (
        -0.4647
        - 0.03971 * at
        + 0.004669 * (at ** 2)
        - 0.00009287 * (at ** 3)
        + 0.0000008152 * (at ** 4)
    )
    tds = 0.85 * (brix + af)
    print(brix, tds, sep=" || ")
    psu = tds
    return psu
