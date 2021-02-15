import cv2
import numpy as np


def find(mask):
    list = []
    contornos,_ =cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos:
        area=cv2.contourArea(c)
        if area>3000:
            M=cv2.moments(c)
            if (M["m00"]==0):M["m00"]=1
            x=int(M["m10"]/M["m00"])
            y=int(M["m01"]/M["m00"])
            list.append({"c":c,"x":x,"y":y})
    return list

def show(elemnt):
    c=elemnt['c']
    x=elemnt['x']
    y=elemnt['y']
    
    font=cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame,'{},{}'.format(x,y),(x+10,y),font,0.75,(0,255,0),1,cv2.LINE_AA)
    nuevoContorno=cv2.convexHull(c)
    cv2.drawContours(frame,[nuevoContorno],0,(255,0,0),3)

cap=cv2.VideoCapture(0)
azulBajo=np.array([100,100,20],np.uint8)
azulAlto=np.array([125,255,255],np.uint8)
while True:
    ret,frame=cap.read()
    if ret==True:
        frameHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        mask=cv2.inRange(frameHSV,azulBajo,azulAlto)
        list=find(mask)
        for p in list:show(p)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF==ord('s'):
            break
cap.release()
cv2.destroyAllWindows()


# cap=cv2.VideoCapture(0)
# azulBajo=np.array([100,100,20],np.uint8)
# azulAlto=np.array([125,255,255],np.uint8)
# while True:
#     ret,frame=cap.read()
#     if ret==True:
#         frameHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
#         mask=cv2.inRange(frameHSV,azulBajo,azulAlto)
#         contornos,_ =cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
#         for c in contornos:
#             area=cv2.contourArea(c)
#             if area>3000:
#                 M=cv2.moments(c)
#                 if (M["m00"]==0):M["m00"]=1
#                 x=int(M["m10"]/M["m00"])
#                 y=int(M["m01"]/M["m00"])
#                 font=cv2.FONT_HERSHEY_SIMPLEX
#                 cv2.putText(frame,'{},{}'.format(x,y),(x+10,y),font,0.75,(0,255,0),1,cv2.LINE_AA)
#                 nuevoContorno=cv2.convexHull(c)
#                 cv2.drawContours(frame,[nuevoContorno],0,(255,0,0),3)
#         cv2.imshow('frame',frame)
#         if cv2.waitKey(1) & 0xFF==ord('s'):
#             break
# cap.release()
# cv2.destroyAllWindows()