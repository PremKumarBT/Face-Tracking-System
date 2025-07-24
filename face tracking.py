import cv2
import cvzone
from cvzone.FaceDetectionModule import FaceDetector
import pyfirmata
import numpy as np
import mediapipe

cap = cv2.VideoCapture(0)
ws, hs = 1280, 720
cap.set(3, ws)
cap.set(4, hs)

if not cap.isOpened():
    print("Camera couldn't Access!!!")
    exit()

port = "COM5"
board = pyfirmata.Arduino(port)
servo_pinX = board.get_pin('d:9:s') 
servo_pinY = board.get_pin('d:10:s') 
servo_pinXT = board.get_pin('d:5:s')
servo_pinYT = board.get_pin('d:6:s')

detector = FaceDetector()
servoPos = [90, 90] 

while True:
    success, img = cap.read()
    img, bboxs = detector.findFaces(img, draw=False)

    if bboxs:
        fx, fy = bboxs[0]["center"][0], bboxs[0]["center"][1]
        pos = [fx, fy]
        servoX = np.interp(fx, [0, ws], [180, 0])
        servoY = np.interp(fy, [0, hs], [180, 0])
        if servoX < 0:
            servoX = 0
        elif servoX > 180:
            servoX = 180
        if servoY < 0:
            servoY = 0
        elif servoY > 180:
            servoY = 180

        servoPos[0] = servoX
        servoPos[1] = servoY

        cv2.circle(img, (fx, fy), 80, (0, 255, 0), 2)
        cv2.putText(img, str(pos), (fx+15, fy-15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2 )
        #cv2.line(img, (0, fy), (ws, fy), (255, 255, 255), 2)  
        #cv2.line(img, (fx, hs), (fx, 0), (255, 255, 255), 2)  
        cv2.circle(img, (fx, fy), 15, (0, 255, 0), cv2.FILLED)
        cv2.putText(img, "FACE TRACKED", (850, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3 )
    else:
        cv2.putText(img, "NO FACE", (880, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
        cv2.circle(img, (640, 360), 80, (0, 255, 0), 2)
        cv2.circle(img, (640, 360), 15, (0, 255, 0), cv2.FILLED)
        #cv2.line(img, (0, 360), (ws, 360), (0, 0, 0), 2)  
        #cv2.line(img, (640, hs), (640, 0), (0, 0, 0), 2)  

    cv2.putText(img, f'Axis X: {int(servoPos[0])} deg', (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    cv2.putText(img, f'Axis Y: {int(servoPos[1])} deg', (50, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

    servo_pinX.write(servoPos[0])
    servo_pinY.write(servoPos[1])
    servo_pinXT.write(servoPos[0])
    servo_pinYT.write(servoPos[1])

    cv2.imshow("Image", img)
    cv2.waitKey(1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()