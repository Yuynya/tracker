import os

import autopy
import cv2
import htm
import pyautogui

indexImg=1
img=None
reqImg=0
wScr, hScr = autopy.screen.size()
def mouseMenegement():
    cap = cv2.VideoCapture(0)
    detector = htm.handDetector()
    while True:
        success, img = cap.read()
        reqImg=1
        img = detector.findHands(img)
        hCam, wCam, channels = img.shape
        lmList, bbox = detector.findPosition(img)
        #   index of fingers
        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]
            fingers = detector.fingersUp()

            if fingers[1] == 1 and fingers[2] == 0:
                realX=(1-x1/wCam)*wScr
                realY=(y1/hCam)*(hScr+220)
                print('real x-Y', realX,realY)
                pyautogui.moveTo(realX, realY)

            if fingers[1] == 1 and fingers[2] == 1:
                print(1)
                length, img, lineInfo = detector.findDistance(8, 12, img)
                if length < 40:
                    print(3)
                    cv2.circle(img, (lineInfo[4], lineInfo[5]),
                               15, (0, 255, 0), cv2.FILLED)
                    pyautogui.click()
                    print(2)
            #if fingers[0]==1 and yBig > y1 :
               # pyautogui.scroll(100)
            if fingers[3] == 1 and fingers[1] == 1 and fingers[2] == 1:
                pyautogui.scroll(100)

            #if fingers[0]==1 and yBig <y1 :
                #pyautogui.scroll(-100)
            if fingers[4] == 1 and fingers[1] == 1 and fingers[2] == 1:
                pyautogui.scroll(-100)
            if fingers[4]==1 and fingers[1]==1 and fingers[2]!=1:
                cv2.circle(img, (lmList[8][1:]), 10, (0, 0, 255), -1)
                pyautogui.click(button='right')
        if indexImg==1:
            cv2.imwrite( '1.jpg', img)
            ++indexImg
            if os.path.exists('2.jpg'):
                os.remove('2.jpg')
        else:
            cv2.imwrite('2.jpg', img)
            --indexImg
            if os.path.exists('1.jpg'):
                os.remove('1.jpg')
        print('---')
        #main.Ui_MainWindow.showCam()
        print('++++')

        cv2.imshow("Img", img)
        cv2.waitKey(1)
async def call():
    mouseMenegement()

