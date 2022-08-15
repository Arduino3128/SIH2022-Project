import cv2
import numpy as np

originalImage = cv2.imread("file.jpg")
fromCenter = False
showCrosshair = False
grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
grayImage[grayImage > 10] = 255
(thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 100, 255, cv2.THRESH_BINARY)
r = cv2.selectROI(
    "Select ROI", blackAndWhiteImage, fromCenter=fromCenter, showCrosshair=showCrosshair
)
print(r)
bck = originalImage.copy()
bck = bck[r[1] : r[1] + r[3], r[0] : r[0] + r[2]]
blackAndWhiteImage = blackAndWhiteImage[r[1] : r[1] + r[3], r[0] : r[0] + r[2]]
edges = cv2.Canny(blackAndWhiteImage, 200, 255)
maxLoc = np.nonzero(edges)
r = list(zip(maxLoc[1], maxLoc[0]))
r = r[0] + r[-1]
r = (r[0], r[1] + 2, r[2], r[3] - 2)
print(r)
cv2.rectangle(bck, (r[0], r[1]), (r[2], r[3]), (0, 255, 0), 1)
img = blackAndWhiteImage[r[1] : r[3], r[0] : r[2]]
cv2.imshow("Black white image", blackAndWhiteImage)
origSize = np.shape(img)
origSize = origSize[0] * origSize[1]
print(origSize)
newSize = np.sum(img >= 250)
print(newSize)
cv2.imshow("Cropped", img)
cv2.imshow("Orginal", bck)

print(f"Percentage Refracted: {newSize/origSize*100}")
print(f"Percentage Reflected: {(1-newSize/origSize)*100}")

cv2.waitKey(0)
cv2.destroyAllWindows()
