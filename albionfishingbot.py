import numpy as np
import cv2
from mss.darwin import MSS as mss
from PIL import Image
import time
import pyautogui as pg
import imutils
import mss
import numpy
import pyautogui
from datetime import datetime

print('\nPreprare fishing...(1 sec)')

template = cv2.imread("jow.png", cv2.IMREAD_GRAYSCALE)
w, h = template.shape[::-1]
color_yellow = (0,255,255)
mon = {'top': 125, 'left': 200, 'width': 150, 'height': 150}
monitor = {"top": 150, "left": 100, "width": 600, "height": 500}
time.sleep(1)

def process_image(original_image):

    processed_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("OpenCV/NewPlace0", processed_image)
    #cv2.waitKey(25)
    processed_image = cv2.Canny(processed_image, threshold1=200, threshold2=300)
    #cv2.imshow("OpenCV/NewPlace1", processed_image)
    #cv2.waitKey(25)
    return processed_image

def newTook(xPos, yPos, index):

    time.sleep(0.01)
    pyautogui.moveTo(xPos, yPos, duration=0.1)
    pyautogui.click(button='left')
    pyautogui.click(button='left')
    pyautogui.click(button='right')

    time.sleep(0.01)
    pyautogui.mouseDown(button='left')
    time.sleep(2)
    pyautogui.mouseUp(button='left')

def catching(index):

    with mss.mss() as sct:

        #screenWidth, screenHeight = pyautogui.size()

        startXPos = 0
        startYPos = 0

        while(True):

            screenshotreal = sct.grab(monitor)
            #print(screenshotreal.size)
            img = numpy.array(screenshotreal)
            gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= 0.7)

            for pt in zip(*loc[::-1]):
                #print(pt)

                #cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3)
                #cv2.imshow("OpenCV/Mon", img)
                #cv2.waitKey(1)

                if startXPos == 0 and startYPos == 0:
                    startXPos = (pt[0] + w / 2) / 2
                    startYPos = (pt[1] + h / 2) / 2
                #print(startXPos, startYPos)

                currentXPos = pt[0] / 2
                #print(currentXPos)

                if currentXPos < startXPos - 35:
                    pyautogui.mouseDown(button='left')
                    break
                else:
                    pyautogui.mouseUp(button='left')
                    break
            else:
                return

def screen_record(xPos, yPos):

    with mss.mss() as screenshot:

        while(True):

            croppedImage = screenshot.grab(mon)
            croppedImage = np.array(croppedImage)
            processed_image = process_image(croppedImage)
            mean = np.mean(processed_image)

            if  mean <= float(0.3):
                break
            else:
                time.sleep(0.01)
                continue

def fishing(index):
    startTickTime = datetime.now()
    pos = (150,200)
    if index % 2 == 0:
        pos = (140,210)
    newTook(pos[0], pos[1], index)
    screen_record(pos[0], pos[1])

    pyautogui.mouseDown(button='left')
    time.sleep(1)
    pyautogui.mouseUp(button='left')

    catching(index)
    endTickTime = datetime.now()
    return (startTickTime, endTickTime)


startTime = datetime.now()
print(f'Start fishing time: {startTime.strftime("%H:%M:%S")} \n')

i = 0
fails_count = 0
while True:

    startTickTime, endTickTime = fishing(i)

    #if ((endTickTime.second - startTickTime.second) < 20):
        #fails_count += 1

    print(f'  [{i}] Fishing time: {datetime.now() - startTime}')#' Fails: {fails_count}')

    i += 1
