import cv2
import numpy as np



rect = {'x' :280,'y' : 50, 'w' : 300, 'h':300}

color = (0,255,255)
bg = None
bgROI= None

cap=cv2.VideoCapture(0)
while True:
    ret,frame=cap.read()
    if ret==True:
        # Grayscale        
        cv2.rectangle(frame,(rect['x'],rect['y'] ),(rect['x']+rect['w'] ,rect['y']+rect['h']),color,1)
        ROI = frame[rect['y']:rect['x'],rect['y']+rect['h']:rect['x']+rect['w']]
        grayROI=cv2.cvtColor(ROI,cv2.COLOR_RGB2GRAY)

        cv2.imshow('ROI',ROI)
        cv2.imshow('frame',frame)

        if bg is not None:
            dif = cv2.absdiff(grayROI, bgROI)
            cv2.imshow('dif',dif)

            _, th = cv2.threshold(dif, 30, 255, cv2.THRESH_BINARY)
            th2 = cv2.medianBlur(th, 1)
            cv2.imshow('th2',th2)
            th = cv2.medianBlur(th, 7)

            cnts, _ = cv2.findContours(th,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = sorted(cnts,key=cv2.contourArea,reverse=True)[:1]
            
            # gray = cv2.GaussianBlur(gray, (7, 7), 3)

            # _,th=cv2.threshold(gray,160,255,cv2.THRESH_BINARY_INV)
            # cnts,_ =cv2.findContours(th,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            # cv2.drawContours(frame,cnts,-1,(255,0,0),2)

            # cv2.imshow('gray',gray)
            

        k = cv2.waitKey(20)	
        if k == ord('i'):
            bg = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            bgROI = bg[rect['y']:rect['x'],rect['y']+rect['h']:rect['x']+rect['w']]
        if k == 27:
            break

cap.release()
cv2.destroyAllWindows()