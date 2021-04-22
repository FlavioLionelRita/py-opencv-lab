from typing import ClassVar
import cv2
import numpy as np

cap=cv2.VideoCapture(0)
count=1
while True:
    ret,frame=cap.read()
    if ret==False:break
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 3)
    if count%20==0:old=gray
    if count>20:
        diff=cv2.absdiff(gray,old)
        _,th=cv2.threshold(diff,40,255,cv2.THRESH_BINARY)
        cnts,_ =cv2.findContours(th,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            area=cv2.contourArea(c)
            if area>5000:
                x,y,w,h=cv2.boundingRect(c)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2) 
    #cv2.imshow('gray',gray)
    #cv2.imshow('th',th)
    cv2.imshow('frame',frame)
    count=count+1    
    if cv2.waitKey(1) & 0xFF==ord('q'):break
cap.release()
cv2.destroyAllWindows()