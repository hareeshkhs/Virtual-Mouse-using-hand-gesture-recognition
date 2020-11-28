import cv2
import numpy as np
import math
import pyautogui
from pynput.mouse import Button, Controller
from datetime import datetime
mouse = Controller()
pyautogui.FAILSAFE = False
sx, sy = 1366, 768
framex , framey = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, framex)
cap.set(4, framey)
cap.set(10, 150)
old = [0, 0]
cursor=0
drag=0
rightclick=0
leftdouble=0
oldt = datetime.strptime('2015-01-01 01:00:00', '%Y-%m-%d %H:%M:%S')
mycolors = [[95, 153, 0, 127, 255, 255],
            [25, 52, 72, 102, 255, 255],
            [0, 199, 186, 255, 255, 255]]
mycolorvalues = [[255, 0, 0],
                 [0, 255, 0],
                 [0, 165, 255]]
mycolortext = ["BLUE","GREEN","ORANGE"]

def findcolor(img, mycolors, mycolorvalues, mycolortext):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    l1 = []
    width = []
    for color in mycolors:
        lo = np.array(color[0:3])
        up = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lo, up)
        # cv2.imshow(str(color[0]),mask)
        kernal = np.ones((5, 5), "uint8")
        # For red color
        erode = cv2.erode(mask, kernal)
        mask1 = cv2.dilate(erode, kernal)
        res = cv2.bitwise_and(img, img, mask=mask1)
        x, y, wid = getContours(img, mask1, count, mycolorvalues, mycolortext)
        cv2.circle(img, (x, y), 5, (0, 0, 255), cv2.FILLED)
        count += 1
        # cv2.imshow("image",img)
        l1.append(x)
        l1.append(y)
        width.append(wid)
        print(x, y)
    #print("At STR:", l1)
    if(min(l1[0],l1[1],l1[2],l1[3])>0):
       c1 = abs((l1[2] + l1[0]) // 2)
       c2 = abs((l1[3] + l1[1]) // 2)
       #print("c1:", c1, "c2:", c2)
       cv2.line(img, (l1[0], l1[1]), (l1[2], l1[3]), (0, 0, 255), 2)
       cv2.circle(img, (c1, c2), 5, (0, 0, 255), cv2.FILLED)
       result1 = round((((l1[2] - l1[0]) ** 2) + ((l1[3] - l1[1]) ** 2)) ** 0.5)
       #print("result:", result1)
       widmax1 = max(width[0], width[1])
       #print("widthmaxbg:", widmax1)
       if (result1 > 0 and result1 <= widmax1 + 10):
           signbg = 1
       else:
           signbg = 0
    else:
        if(l1[0]==0):
            c1=l1[2]
            c2=l1[3]
        if(l1[2]==0):
            c1=l1[0]
            c2=l1[1]
        signbg = 0
    #print("At MID:", l1)
    if (min(l1[0],l1[1],l1[4],l1[5])>0):
        c3 = abs((l1[4] + l1[0]) // 2)
        c4 = abs((l1[5] + l1[1]) // 2)
        #print("c3:", c3, "c4:", c4)
        cv2.line(img, (l1[0], l1[1]), (l1[4], l1[5]), (0, 0, 255), 2)
        cv2.circle(img, (c3, c4), 5, (0, 0, 255), cv2.FILLED)
        result2 = round((((l1[4] - l1[0]) ** 2) + ((l1[5] - l1[1]) ** 2)) ** 0.5)
        widmax2 = max(width[0], width[2])
        #print("widthmaxbo:", widmax2)
        if (result2 > 0 and result2 <= widmax2 + 10):
            signbo = 1
        else:
            signbo = 0
    else:
        signbo=0
    #print("At End:",l1)
    if (min(l1[2],l1[3],l1[4],l1[5])>0):
        c5 = abs((l1[2] + l1[4]) // 2)
        c6 = abs((l1[3] + l1[5]) // 2)
        #print("c5:", c5, "c6:", c6)
        cv2.line(img, (l1[2], l1[3]), (l1[4], l1[5]), (0, 0, 255), 2)
        cv2.circle(img, (c5, c6), 5, (0, 0, 255), cv2.FILLED)
        result3 = round((((l1[2] - l1[4]) ** 2) + ((l1[3] - l1[5]) ** 2)) ** 0.5)
        widmax3 = max(width[1], width[2])
        #print("widthmaxbo:", widmax3)
        if (result3 > 0 and result3 <= widmax3 + 5):
            signog = 1
        else:
            signog = 0
    else:
        signog=0

    if (min(l1)>0):
        centroid1 = round((l1[0] + l1[2] + l1[4]) // 3)
        centroid2 = round((l1[1] + l1[3] + l1[5]) // 3)
        d1 = round((((l1[0] - centroid1) ** 2) + ((l1[1] - centroid2) ** 2)) ** 0.5)
        d2 = round((((l1[2] - centroid1) ** 2) + ((l1[3] - centroid2) ** 2)) ** 0.5)
        d3 = round((((l1[4] - centroid1) ** 2) + ((l1[5] - centroid2) ** 2)) ** 0.5)
        widmax4 = max(width)
        if (d1<=widmax4+3 and d2<=widmax4+3 and d3<=widmax4+3):
            signcen = 1
        else:
            signcen = 0
    else:
        signcen = 0
    return c1, c2, signbg, signbo, signog, signcen


def getContours(imgResult, img, count, mycolorvalues, mycolortext):
    x, y, w, h = 0, 0, 0, 0
    contours, hierarchy = cv2.findContours(img,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    l = len(contours)
    max_area = 0
    max_index = -1
    i = 0
    while (i < l):
        area = cv2.contourArea(contours[i])
        if (area > max_area):
            max_area = area
            max_index = i
        i += 1
    if (l > 0):
        if (max_area > 500):
            x, y, w, h = cv2.boundingRect(contours[max_index])
            imgResult = cv2.rectangle(imgResult, (x, y),
                                      (x + w, y + h),
                                      (mycolorvalues[count]), 2)

            cv2.putText(imgResult, mycolortext[count], (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (mycolorvalues[count]))

    return x + w // 2, y + h // 2, w


while True:
    succuss, img = cap.read()
    imgResult = img.copy()
    new = []
    x, y, sign, signbo, signog, signcen = findcolor(img, mycolors, mycolorvalues, mycolortext)
    print("px:", x, "py:", y, "sign:", sign, "signbo:", signbo, "signog:", signog, "signcen:", signcen)
    new.append(x)
    new.append(y)
    a = new[0] - old[0]
    b = new[1] - old[1]
    distance = math.sqrt(a ** 2 + b ** 2)
    #Action for Left CLick
    if(signcen==0):
        if (sign == 1 and abs(distance) < 3):
            if(cursor==2 and round((datetime.now() - newt).total_seconds())):
                pyautogui.click(button='left')
                cursor=0
            cursor=1
            newt = datetime.now()
        if (sign == 0 and abs(distance) < 3):
            if(cursor==1):
                cursor=2
            if(cursor!=0 and round((datetime.now() - newt).total_seconds())>1.5):
                cursor=0
    #2. Action for Right Click
    if (signog == 1 and signcen == 0):
        rightclick=1
    if(signog == 0 and rightclick == 1 and signcen==0):
        pyautogui.click(button='right')
        rightclick=0
    #3. Action for Left Double Click
    if(signcen!=1):
        if (signbo == 1 and signcen ==0):
            leftdouble=1
        if (signbo == 0 and leftdouble==1 and signcen == 0):
            pyautogui.doubleClick()
            leftdouble=0
    #4. Action for Mouse Movement
    if (abs(distance) > 5 and sign == 1):
        pyautogui.moveRel(2*(-a), 2*b)
    #5. Action for Drag & Drop
    if (signcen == 0 and drag >= 1):
        mouse.release(Button.left)
        drag = 0
        ones=0
    if (signcen == 1 and sign==1 and drag==0):
        mouse.press(Button.left)
        drag = drag+1
    old = new
    cv2.imshow("Result", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
