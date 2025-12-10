import cv2
import mediapipe as mp
import time
import math
import handTrackingModule as hmt

pTime = 0
cTime = 0
dist = 0

cap = cv2.VideoCapture(0)

detector = hmt.handDetector()

while True:
    success, img = cap.read()
    img = detector.findHands(img)

    lmList = detector.findPosition(img, draw=False) 

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    fingers = 0

    if lmList:
        palm = math.hypot(lmList[0][2] - lmList[5][2], lmList[0][1]-lmList[5][1])
        
        if(math.hypot(lmList[4][1]-lmList[2][1], lmList[4][2]-lmList[2][2]) < math.hypot(lmList[4][1]-lmList[5][1], lmList[4][2]-lmList[5][2])):
            fingers += 1
        
        i = 8
        while i < 21:
            if(math.hypot(lmList[0][1]-lmList[i][1], lmList[0][2]-lmList[i][2]) > (palm*1.2)):
                fingers += 1
            i += 4


    cv2.putText(img, str(int(fps)), (10,40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 1)
    cv2.putText(img,str(fingers), (90,70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break