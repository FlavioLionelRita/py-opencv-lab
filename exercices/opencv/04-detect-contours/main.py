import cv2
import numpy as np

cap=cv2.VideoCapture(0)
while True:
    ret,frame=cap.read()
    if ret==True:
        # Grayscale
        gray=cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 3)
        _,th=cv2.threshold(gray,160,255,cv2.THRESH_BINARY_INV)
        cnts,_ =cv2.findContours(th,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame,cnts,-1,(255,0,0),2)

        cv2.imshow('gray',gray)
        cv2.imshow('th',th)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF==ord('s'):
            break
cap.release()
cv2.destroyAllWindows()