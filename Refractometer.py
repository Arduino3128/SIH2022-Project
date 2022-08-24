import RPi.GPIO as GPIO
from time import sleep
import cv2
import numpy as np
import configparser
from rich import print as pprint


# Pin Defination
LaserPin = 12

# Initialize and configure
config_file = configparser.ConfigParser()
GPIO.setmode(GPIO.BCM)
GPIO.setup(LaserPin, GPIO.OUT)
fromCenter = False
showCrosshair = False
sleep(2)  # Wait for 2 seconds to let everything initialize


class Laser:
    def __init__(self):
        pprint("[green bold][REFRACTOMETER] LASER system activated![/green bold]")

    def on(self):
        try:
            GPIO.output(LaserPin, True)
            return "ON"
        except Exception as ERROR:
            return ERROR

    def off(self):
        try:
            GPIO.output(LaserPin, False)
            return "OFF"
        except Exception as ERROR:
            return ERROR


class ImageProcessing:
    def __init__(self):
        pprint("[green bold][REFRACTOMETER] Image processor started![/green bold]")

    def capture(self):
        return "OK"
        try:
            webcam = cv2.VideoCapture(0)
            for _ in range(10):
                check, frame = webcam.read()
                cv2.imwrite(filename="sample.png", img=frame)
            webcam.release()
            return "OK"
        except Exception as ERROR:
            return ERROR

    def process(self):
        config_file.read("config.ini")
        data = config_file["Refractometer"]
        ROI = eval(data.get("calib_value"))
        ROI2 = eval(data.get("crop_value"))
        originalImage = cv2.imread("sample.png")
        grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
        grayImage[grayImage > 10] = 255
        (thresh, blackAndWhiteImage) = cv2.threshold(
            grayImage, 100, 255, cv2.THRESH_BINARY
        )
        blackAndWhiteImage = blackAndWhiteImage[
            ROI2[1] : ROI2[1] + ROI2[3], ROI2[0] : ROI2[0] + ROI2[2]
        ]
        img = blackAndWhiteImage[ROI[1] : ROI[3], ROI[0] : ROI[2]]
        origSize = np.shape(img)
        origSize = origSize[0] * origSize[1]
        newSize = np.sum(img >= 250)
        return newSize / origSize

    def refraction(self):
        capture = "OK"
        if capture != "OK":
            return "Failed"
        data = float(self.process())
        return data

    def calibrate(self):
        # self.capture()
        originalImage = cv2.imread("sample.png")
        grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
        grayImage = cv2.fastNlMeansDenoising(grayImage, None, h=10)
        grayImage[grayImage > 10] = 255
        (thresh, blackAndWhiteImage) = cv2.threshold(
            grayImage, 100, 255, cv2.THRESH_BINARY
        )
        kernel = np.ones((10, 10), np.uint8)
        blackAndWhiteImage = cv2.morphologyEx(
            blackAndWhiteImage, cv2.MORPH_OPEN, kernel
        )
        ROI = cv2.selectROI(
            "Select ROI",
            blackAndWhiteImage,
            fromCenter=fromCenter,
            showCrosshair=showCrosshair,
        )
        cv2.destroyAllWindows()
        ROI2 = ROI
        bck = originalImage.copy()
        bck = bck[ROI[1] : ROI[1] + ROI[3], ROI[0] : ROI[0] + ROI[2]]
        blackAndWhiteImage = blackAndWhiteImage[
            ROI[1] : ROI[1] + ROI[3], ROI[0] : ROI[0] + ROI[2]
        ]
        edges = cv2.Canny(blackAndWhiteImage, 200, 255)
        maxLoc = np.nonzero(edges)
        ROI = list(zip(maxLoc[1], maxLoc[0]))
        ROI = ROI[0] + ROI[-1]
        ROI = (ROI[0], ROI[1] + 4, ROI[2], ROI[3] - 4)
        cv2.rectangle(bck, (ROI[0], ROI[1]), (ROI[2], ROI[3]), (0, 255, 0), 1)
        img = blackAndWhiteImage[ROI[1] : ROI[3], ROI[0] : ROI[2]]
        origSize = np.shape(img)
        origSize = origSize[0] * origSize[1]
        newSize = np.sum(img >= 250)
        cv2.imshow("Monochrome image", blackAndWhiteImage)
        cv2.imshow("ROI Identified on Orginal image", bck)
        cv2.imshow("ROI Image", img)
        refraction = newSize / origSize
        print(refraction * 100)
        if cv2.waitKey(0) == ord("y") or cv2.waitKey(0) == 13:
            cv2.destroyAllWindows()
            with open("config.ini", "w") as configuration:
                config_file["Refractometer"] = {}
                config_file["Refractometer"]["calib_value"] = str(ROI)
                config_file["Refractometer"]["crop_value"] = str(ROI2)
                config_file.write(configuration)
        else:
            self.calibrate()
            cv2.destroyAllWindows()
