import numpy as np
import cv2
 
# Create a black image
img = np.zeros((512,512,3), np.uint8)
 
# Draw a diagonal blue line with thickness of 5 px
cv2.line(img,(0,0),(511,511),(255,0,0),5)

#FONT_HERSHEY_SIMPLEX
#FONT_HERSHEY_PLAIN
#FONT_HERSHEY_DUPLEX
#FONT_HERSHEY_COMPLEX
#FONT_HERSHEY_TRIPLEX
#FONT_HERSHEY_COMPLEX_SMALL
#FONT_HERSHEY_SCRIPT_SIMPLEX
#FONT_HERSHEY_SCRIPT_COMPLEX
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.5
fontColor = (255,255,255)
lineType = 1
cv2.putText(img, "hello", (200, 200), font, fontScale, fontColor, lineType)

x1 = 50
y1 = 50
x2 = 150
y2 = 150
cv2.rectangle(img, (x1, y1), (x2, y2), (0, 128, 0), 1)

pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
pts = pts.reshape((-1,1,2))
cv2.polylines(img,[pts],True,(0,255,255))

cv2.imshow("OpenCV Draw", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

