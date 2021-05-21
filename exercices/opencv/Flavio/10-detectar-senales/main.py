import cv2
import imutils
from os import path
import numpy as np

_path = path.dirname(path.abspath(__file__))


cap = cv2.VideoCapture('house_to_school.mp4')
cap.set(cv2.CAP_PROP_POS_FRAMES, 30*60*13.5)
color = (0,255,255)
# color_punto = (0,0,255)
#Verde
azulBajo = np.array([95, 100, 20], np.uint8)
azulAlto = np.array([125, 255, 255], np.uint8)


rect = {'x' :240,'y' : 100, 'w' : 350, 'h':350}


while cap.isOpened():	
    ret,frame = cap.read()    
    h, w, c = frame.shape
    # Paso 1: Imagen a procesar
    frame = cv2.resize(frame,(int(w/3),int(w/3)))
    cv2.rectangle(frame,(rect['x'],rect['y'] ),(rect['x']+rect['w'] ,rect['y']+rect['h']),color,1)
    
    ROI = frame[rect['y']:rect['y']+rect['h'],rect['x']:rect['x']+rect['w']]

    imageHSV = cv2.cvtColor(ROI, cv2.COLOR_BGR2HSV)
    # Paso 2: Transformar de BGR a HSV
    mask = cv2.inRange(imageHSV, azulBajo, azulAlto)
    cv2.imshow('mask',mask)

    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0] 
    cnts = sorted(cnts,key=cv2.contourArea,reverse=True)[:1]
    for cnt in cnts:
        hull2 = cv2.convexHull(cnt)
        cv2.drawContours(ROI,[hull2],0,(0,0,255),1)

        epsilon = 0.01*cv2.arcLength(hull2,True)
        approx = cv2.approxPolyDP(hull2,epsilon,True)
        # print(approx)

        for p in approx:
            cv2.circle(ROI,(p[0][0],p[0][1]),1,(0,255,0),-1)

    cv2.imshow('ROI',ROI)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) == 27: break
   
cap.release()
cv2.destroyAllWindows()
