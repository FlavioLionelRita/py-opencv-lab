import cv2
cam=cv2.VideoCapture(0)
while(cam.isOpened()):
    ret,img=cam.read()
    if ret==True:
        cv2.imshow('webcam',img)
        if cv2.waitKey(1) & 0xFF==ord('s'):
            break
cam.release()
cv2.destroyAllWindows()

