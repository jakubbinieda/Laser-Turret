import cv2
import numpy as np
import dlib
import time
from math import hypot

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("landmarks.dat")

def midPoint(p1 ,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

def getEye(eyePoints, facialLandmarks):
    leftPoint = (facialLandmarks.part(eyePoints[0]).x, facialLandmarks.part(eyePoints[0]).y)
    rightPoint = (facialLandmarks.part(eyePoints[3]).x, facialLandmarks.part(eyePoints[3]).y)
    centerTop = midPoint(facialLandmarks.part(eyePoints[1]), facialLandmarks.part(eyePoints[2]))
    centerBottom = midPoint(facialLandmarks.part(eyePoints[5]), facialLandmarks.part(eyePoints[4]))

    horLine = cv2.line(frame, leftPoint, rightPoint, (0, 255, 0), 2)
    verLine = cv2.line(frame, centerTop, centerBottom, (0, 255, 0), 2)

    xdiff = (leftPoint[0] - rightPoint[0], centerTop[0] - centerBottom[0])
    ydiff = (leftPoint[1] - rightPoint[1], centerTop[1] - centerBottom[1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)

    d = (det(*(leftPoint, rightPoint)), det(*(centerTop,centerBottom)))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def calibration(angle) :
    if angle > 5.5: angle-=1.5
    elif angle < 1: angle+=1
    return angle

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    for face in faces:
        landmarks = predictor(gray, face)

        eyeMiddle=getEye([36, 37, 38, 39, 40, 41], landmarks)
        f=open("./views/coordinates.ejs","w")
        angleHor=eyeMiddle[0]/(1280/90)/10
        angleVer=eyeMiddle[1]/(720/90)/10
        
        angleHor=calibration(angleHor)
        angleVer=calibration(angleVer)
        
        f.write("<div id='angleHor'>"+str(angleHor)+"</div><div id='angleVer'>"+str(angleVer)+"</div>")
        f.close()


    frame = cv2.resize(frame, (640, 360))
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
