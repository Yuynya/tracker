import math
import cv2
import keyboard as keyboard
import pyautogui
import autopy

import mediapipe as mp

indexOpen=0
indexClose=0
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
wScr, hScr = autopy.screen.size()
def getRightOrLeft(results,img, hands):
    lmListRight = []
    bboxRight = []
    lmListLeft = []
    bboxLeft = []
    for idx, classification in enumerate(results.multi_handedness):

        label = classification.classification[0].label
        text = '{}'.format(label)
        if text == 'Left':
            lmListLeft, bboxLeft = findPosition(img, hands.process(img))
        if text == 'Right':
            lmListRight, bboxRight = findPosition(img, hands.process(img))

    return lmListLeft, bboxLeft, lmListRight, bboxRight

def findPosition(img, results, handNo=0):
    xList = []
    yList = []
    bbox = []
    lmList = []
    if results.multi_hand_landmarks:
        myHand = results.multi_hand_landmarks[handNo]
        for id, lm in enumerate(myHand.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            xList.append(cx)
            yList.append(cy)
            lmList.append([id, cx, cy])
        xmin, xmax = min(xList), max(xList)
        ymin, ymax = min(yList), max(yList)
        bbox = xmin, ymin, xmax, ymax

    return lmList, bbox
def thumbPosition(p1, p2,p3, p4,p5,p6, p7,p8,p9,p10,p11, img, lmList):
    x1, y1 = lmList[p1][1], lmList[p1][2]
    x2, y2 = lmList[p2][1], lmList[p2][2]
    x3, y3 = lmList[p3][1], lmList[p3][2]
    x4, y4 = lmList[p4][1], lmList[p4][2]
    x5, y5 = lmList[p5][1], lmList[p5][2]
    x6, y6 = lmList[p6][1], lmList[p6][2]
    x7, y7 = lmList[p7][1], lmList[p7][2]
    x8, y8 = lmList[p8][1], lmList[p8][2]
    x9, y9 = lmList[p9][1], lmList[p9][2]
    x10, y10 = lmList[p10][1], lmList[p10][2]
    x11, y11 = lmList[p11][1], lmList[p11][2]
    return x1, y1,  x2, y2,x3, y3,x4, y4,x5, y5,x6, y6,x7, y7, x8, y8,x9, y9,x10, y10,x11, y11

def findDistance(finger1, finger2, img, lmList):
    x1, y1 = lmList[finger1][1], lmList[finger1][2]
    x2, y2 = lmList[finger2][1], lmList[finger2][2]
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

    length = math.hypot(x2 - x1, y2 - y1)
    return length, img, [x1, y1, x2, y2, cx, cy]


def fingersUp(lmList):
    fingers = []
    tipIds = [4, 8, 12, 16, 20]
    if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
        fingers.append(1)
    else:
        fingers.append(0)
    for id in range(1, 5):
        if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

def draw(img, results):
    if results.multi_hand_landmarks:
        for num, hand in enumerate(results.multi_hand_landmarks):
            mp_drawing.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                      mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                      )
    return img
indEnd=0
indexClick=0
indexRightClick=0
indUp=0
indDown=0
indF=0
indSF=0
indHome=0
indEsc=0
def mouseContrl(indCam, mainHand):
    global indexClose
    global indexOpen
    global indexClick
    global indexRightClick
    global indEnd
    global indUp
    global indDown
    global indF
    global indSF
    global indHome
    global indEsc
    with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
        indexClose=indexClose
        indexClick=indexClick
        indexRightClick=indexRightClick
        cap = cv2.VideoCapture(indCam)
        while cap.isOpened():
            ret, frame = cap.read()
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            hCam, wCam, channels = img.shape
            img = cv2.flip(img, 1)
            img.flags.writeable = False
            results = hands.process(img)
            img.flags.writeable = True
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                lmListLeft, bboxLeft, lmListRight, bboxRight = getRightOrLeft(results, img, hands)
                if mainHand == 0:
                    if len(lmListLeft) != 0:
                        tx1, ty1, tx2, ty2, px1, py1, px2, py2, ix1, iy1, ix2, iy2, mx1, my1, mx2, my2, rx1, ry1, rx2, ry2, hx, hy = thumbPosition(
                            2, 4, 17, 20, 6, 8, 10, 12, 14, 16, 0, img, lmListLeft)
                        x1, y1 = lmListLeft[8][1:]
                        fingers = fingersUp(lmListLeft)
                        if fingers[1] == 1 and fingers[2] == 0:
                            realX = (x1 / (wCam-wCam/5)) * wScr
                            realY = (y1 / (hCam-hCam/3)) * hScr
                            pyautogui.moveTo(realX, realY)

                        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:

                            length, img, lineInfo = findDistance(8, 12, img, lmListLeft)
                            if length < 50:
                                indexClick+=1
                                if indexClick==2:
                                    indexClick=0
                                    cv2.circle(img, (lineInfo[4], lineInfo[5]),
                                               15, (0, 255, 0), cv2.FILLED)
                                    pyautogui.click()
                            else:
                                indexClick=0

                        print(fingers)
                        if fingers[4] == 1 and fingers[1] == 1 and fingers[2] ==0 and fingers[3] == 0:
                            indexRightClick+=1
                            if indexRightClick==3:
                                indexRightClick=0
                                cv2.circle(img, (lmListLeft[8][1:]), 10, (0, 0, 255), -1)
                                pyautogui.click(button='right')
                        else:
                            indexRightClick=0

                        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                            indexClose += 1
                            print(indexClose)
                            if indexClose==15:
                                break
                        else:
                            indexClose=0

                        if fingers[3] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[4] != 1:
                            indDown+=1
                            print('{}, indUp', indDown)
                            if indDown==3:
                                keyboard.send("page down")
                                indDown=0
                        else:
                            indDown=0
                        if fingers[4] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] != 1:
                            indUp+=1
                            print('{}, indUp', indUp)
                            if indUp==3:
                                keyboard.send("page up")
                                indUp=0
                        else:
                            indUp=0
                        if tx1<tx2 and fingers[4] != 1 and fingers[1] != 1 and fingers[2] != 1 and fingers[3] != 1 and hx<tx1:
                            indHome+=1
                            print('{}, indHome', indHome)
                            if indHome==3:
                                keyboard.send("home")
                                indHome=0
                        else:
                            indHome=0
                        if  tx1>tx2 and fingers[4] != 1 and fingers[1] != 1 and fingers[2] != 1 and fingers[3] != 1:
                            indEnd+=1
                            print('{}, indEnd', indEnd)
                            if indEnd==3:
                                keyboard.send("end")
                                indEnd=0
                        else:
                            indEnd=0

                if mainHand == 1:
                    if len(lmListRight) != 0:
                        tx1, ty1, tx2, ty2, px1, py1, px2, py2, ix1, iy1, ix2, iy2, mx1, my1, mx2, my2, rx1, ry1, rx2, ry2, hx, hy = thumbPosition(
                            2, 4, 17, 20, 6, 8, 10, 12, 14, 16, 0, img, lmListRight)
                        x1, y1 = lmListRight[8][1:]
                        fingers = fingersUp(lmListRight)
                        if fingers[1] == 1 and fingers[2] == 0:
                            realX = (x1 / wCam) * wScr
                            realY = (y1 / hCam) * (hScr + 220)
                            pyautogui.moveTo(realX, realY)

                        if fingers[1] == 1 and fingers[2] == 1 and fingers[3]!=1 and fingers[4] != 1:
                            length, img, lineInfo = findDistance(8, 12, img, lmListRight)

                            if length < 40:
                                indexClick += 1
                                print(indexClick)
                                if indexClick == 2:
                                    indexClick=0
                                    cv2.circle(img, (lineInfo[4], lineInfo[5]),
                                               15, (0, 255, 0), cv2.FILLED)
                                    pyautogui.click()
                            else:
                                indexClick=0

                        if fingers[4] == 1 and fingers[1] == 1 and fingers[2] != 1 :
                            indexClose = 0
                            indexRightClick+=1
                            if indexRightClick==3:
                                indexRightClick=0
                                cv2.circle(img, (lmListRight[8][1:]), 10, (0, 0, 255), -1)
                                pyautogui.click(button='right')
                        else:
                            indexRightClick=0

                        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1 and fingers[
                            0] == 1:
                            indexClose += 1
                            print(indexClose)
                            if indexClose == 15:
                                break
                        else:
                            indexClose=0
                        if fingers[3] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[4] != 1:
                            indDown += 1
                            print('{}, indUp', indDown)
                            if indDown == 3:
                                keyboard.send("page down")
                                indDown = 0
                        else:
                            indDown = 0
                        if fingers[4] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] != 1:
                            indUp += 1
                            print('{}, indUp', indUp)
                            if indUp == 3:
                                keyboard.send("page up")
                                indUp = 0
                        else:
                            indUp = 0
                        if tx1 < tx2 and fingers[4] != 1 and fingers[1] != 1 and fingers[2] != 1 and fingers[
                            3] != 1 and hx < tx1:
                            indHome += 1
                            print('{}, indHome', indHome)
                            if indHome == 3:
                                keyboard.send("home")
                                indHome = 0
                        else:
                            indHome = 0
                        if tx1 > tx2 and fingers[4] != 1 and fingers[1] != 1 and fingers[2] != 1 and fingers[3] != 1:
                            indEnd += 1
                            print('{}, indEnd', indEnd)
                            if indEnd == 3:
                                keyboard.send("end")
                                indEnd = 0
                        else:
                            indEnd = 0
                img = draw(img, results)
                cv2.imshow('', img)
                if cv2.waitKey(10) & 0xFF == 27:  # <<<<< 0xFF
                    break


    indexOpen = 0
    indexClose=0
    cap.release()
    cv2.destroyAllWindows()



