from typing import final
import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
# import playsound as p
from time import sleep
import numpy as np
from pynput.keyboard import Controller

img = cv.VideoCapture(1)
img.set(3, 1280)
img.set(4, 720)

detector = HandDetector(detectionCon=0.8)

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", " "]]

outputtext = ""

keyboard =  Controller()
def draw(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv.rectangle(frames, button.pos, (x + w, y + h), (0,255,0), cv.FILLED)
        cv.putText(frames, button.text,(x + 15, y + 55), cv.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img
class Button():
    def __init__(self, pos , text, size = [75,70]):
        self.pos = pos
        self.text = text
        self.size = size

buttonList = []
for x, key in enumerate(keys[0]):
    buttonList.append(Button([100 * x + 50, 60], key))
for a, key in enumerate(keys[1]):
    buttonList.append(Button([100 * a + 50, 160], key))
for i, key in enumerate(keys[2]):
    buttonList.append(Button([100 * i + 50, 260], key))
    # for i in len(keys):
    #   for j, key in enumerate(keys[i]):
            # buttonList.append(Button([100 * j + 50, 100 * i + 50], key))


while True:
    isTrue, frames = img.read()
    frames = cv.flip(frames, 1)
    frames = detector.findHands(frames, 2)
    lmlist, bboxinfo = detector.findPosition(frames)
    draw(img, buttonList)
    # img = myButton.draw(img)

    if lmlist:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            # mediapipe parameters 
            if x < lmlist[8][0] < x + w and y<lmlist[8][1] < y + h:
                cv.rectangle(frames, (x-5, y-5), (x + w + 5, y + h + 5), (0,0,255), cv.FILLED)
                cv.putText(frames, button.text,(x + 15, y + 55), cv.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                l,_,_=detector.findDistance(8, 12, frames, draw=False)
                print(l)

                if l < 40:
                    keyboard.press(button.text)
                    cv.rectangle(frames, button.pos, (x + w, y + h), (255,0,0), cv.FILLED)
                    cv.putText(frames, button.text,(x + 15, y + 55), cv.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    outputtext += button.text
                    # p.playsound("keypress.mp3", False)
                    # sleep(0.5)
                   

    cv.rectangle(frames, (50, 350), (700, 450), (0,0,0), cv.FILLED)
    cv.putText(frames, outputtext,(60, 425), cv.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    cv.imshow("Video", frames)
    cv.waitKey(20)
