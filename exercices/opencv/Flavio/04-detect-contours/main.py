import cv2
import numpy as np



rect = {'x' :280,'y' : 50, 'w' : 300, 'h':300}

color = (0,255,255)
color_punto = (0,255,0)

bg = None
bgROI= None

#Verde
verdeBajo = np.array([36, 100, 20], np.uint8)
verdeAlto = np.array([70, 255, 255], np.uint8)

naranjaBajo = np.array([11, 100, 20], np.uint8)
naranjaAlto = np.array([19, 255, 255], np.uint8)

cap=cv2.VideoCapture(0)
while True:
    ret,frame=cap.read()
    if ret==True:
        # Grayscale        
        cv2.rectangle(frame,(rect['x'],rect['y'] ),(rect['x']+rect['w'] ,rect['y']+rect['h']),color,1)
        ROI = frame[rect['y']:rect['x'],rect['y']+rect['h']:rect['x']+rect['w']]
        # grayROI=cv2.cvtColor(ROI,cv2.COLOR_RGB2GRAY)
        imageHSV = cv2.cvtColor(ROI, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(imageHSV, naranjaBajo, naranjaAlto)
        cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0] #Reemplaza por 1, si tienes OpenCV3
        cnts = sorted(cnts,key=cv2.contourArea,reverse=True)[:1]
        
        for cnt in cnts:
            hull2 = cv2.convexHull(cnt)
            # defects = cv2.convexityDefects(cnt,hull2)

            cv2.drawContours(ROI,[hull2],0,(255,0,0),2)

            epsilon = 0.01*cv2.arcLength(hull2,True)
            approx = cv2.approxPolyDP(hull2,epsilon,True)
            # print(approx)ii

            for p in approx:
                cv2.circle(ROI,(p[0][0],p[0][1]),5,color_punto,-1)


        # if bg is not None:
            # dif = cv2.absdiff(grayROI, bgROI)
            # cv2.imshow('dif',dif)

            # _, th = cv2.threshold(dif, 30, 255, cv2.THRESH_BINARY)
            # th2 = cv2.medianBlur(th, 1)
            # # cv2.imshow('th2',th2)
            # th = cv2.medianBlur(th, 7)



            # cnts, _ = cv2.findContours(th,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # cnts = sorted(cnts,key=cv2.contourArea,reverse=True)[:1]
            
            # for cnt in cnts:
            #     # Contorno encontrado a través de cv2.convexHull
            #     hull1 = cv2.convexHull(cnt)
            #     cv2.drawContours(ROI,[hull1],-1,(255,0,0),2)

            # gray = cv2.GaussianBlur(gray, (7, 7), 3)

            # _,th=cv2.threshold(gray,160,255,cv2.THRESH_BINARY_INV)
            # cnts,_ =cv2.findContours(th,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            # cv2.drawContours(frame,cnts,-1,(255,0,0),2)

            # cv2.imshow('gray',gray)
            
        cv2.imshow('ROI',ROI)
        cv2.imshow('frame',frame)        
        k = cv2.waitKey(20)	
        if k == ord('i'):
            bg = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            bgROI = bg[rect['y']:rect['x'],rect['y']+rect['h']:rect['x']+rect['w']]
        if k == 27:
            break

cap.release()
cv2.destroyAllWindows()