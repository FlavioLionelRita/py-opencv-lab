import numpy as np
import cv2
from matplotlib import pyplot as plt

cap=cv2.VideoCapture(0)
while True:
    ret,frame=cap.read()
    if ret==True:
        # Grayscale
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 3)
        edges = cv2.Canny(gray,20,30)
        cv2.imshow('gray',gray)
        cv2.imshow('edges',edges)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF==ord('s'):
            break
cap.release()
cv2.destroyAllWindows()