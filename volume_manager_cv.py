import cv2
import mediapipe as mp
import time
import math
import handTrackingModule as hmt
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetDeviceEnumerator().GetDefaultAudioEndpoint(0, 1).Activate(
   IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(devices, POINTER(IAudioEndpointVolume))

pTime = 0
cTime = 0
dist = 0

cap = cv2.VideoCapture(0)

detector = hmt.handDetector()

while True:
    success, img = cap.read()
    img = detector.findHands(img)

    lmList = detector.findPosition(img) 

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    if lmList:
        x1 = lmList[4][1]
        x2 = lmList[8][1]
        y1 = lmList[4][2]
        y2 = lmList[8][2]
        dist = (math.hypot(x2-x1,y2-y1))/(img.shape[1])

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,255),3)
    if(dist > 0.333):
        dist = 0.333

    cv2.putText(img, "Volume: "+str(int(300*dist)%100) + "%", (80,70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 3)
    volume.SetMasterVolumeLevelScalar((dist*3), None)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break