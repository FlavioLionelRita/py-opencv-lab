import cv2
import imutils




cap = cv2.VideoCapture('/home/flavio/develop/py-opencv-lab/docs/data/captures/house_to_school.mp4')
cap.set(cv2.CAP_PROP_POS_FRAMES, 30*60*4)

plateCascades = cv2.CascadeClassifier('./haarcascades/haarcascade_russian_plate_number.xml')
# './haarcascades//haarcascade_fullbody.xml'
# './haarcascades/haarcascade_frontalface_default.xml'


def detectPlate(frame,gray,name):    
    plate = plateCascades.detectMultiScale(gray)   
    for (x,y,w,h) in plate:
        cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
        cv2.putText(frame,'plate',(x,y-10),2,0.7,(0,255,0),2,cv2.LINE_AA)
        if cv2.waitKey(1) == ord('s'):
            cv2.imwrite('./plates/img_{}.jpg'.format(name),frame[y:y+h,x:x+w])



plates = 0
while cap.isOpened():	
    ret,frame = cap.read()    
    h, w, c = frame.shape
    frame = cv2.resize(frame,(int(w/3),int(w/3)))
    frame = imutils.rotate(frame, 90)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #gray = cv2.GaussianBlur(gray, (7, 7), 1)
    #gray = cv2.Canny(gray, 10,150)
    #gray = cv2.dilate(gray,None,iterations=1)
    #gray = cv2.erode(gray,None,iterations=1)
    _,bin1=cv2.threshold(gray,60,255,cv2.THRESH_BINARY)
    _,bin2=cv2.threshold(gray,110,255,cv2.THRESH_BINARY)
    _,bin3=cv2.threshold(gray,180,255,cv2.THRESH_BINARY)
    detectPlate(frame,bin1,str(plates)+'_1')
    detectPlate(frame,bin2,str(plates)+'_2')
    detectPlate(frame,bin3,str(plates)+'_3')
    plates=plates+1
    
    # plate = plateCascades.detectMultiScale(gray)   
    # for (x,y,w,h) in plate:
    #     cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
    #     cv2.putText(frame,'plate',(x,y-10),2,0.7,(0,255,0),2,cv2.LINE_AA)
    #     if cv2.waitKey(1) == ord('s'):
    #         cv2.imwrite('./plates/img_{}.jpg'.format(plates),frame[y:y+h,x:x+w])
    #     plates=plates+1

    cv2.imshow('bin1',bin1) 
    cv2.imshow('bin2',bin2) 
    cv2.imshow('bin3',bin3) 
    #cv2.imshow('gray',gray)    
    cv2.imshow('frame',frame)
	
    if cv2.waitKey(1) == 27: break
   
cap.release()
cv2.destroyAllWindows()

# import cv2
# w_cascade = cv2.CascadeClassifier('cascade.xml')
# cap = cv2.VideoCapture(0)
# while True:
#     ret, img = cap.read()
#     if ret:
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         w = w_cascade.detectMultiScale(image=gray,scaleFactor=1.3,minNeighbors=5)
#         for (x, y, w, h) in w:
#             cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
#             font = cv2.FONT_HERSHEY_SIMPLEX
#             cv2.putText(img, 'kitty', (x - w, y - h), font, 0.5, (11, 255, 255),  2, cv2.LINE_AA)
#         cv2.imshow('img', img)
#         k = cv2.waitKey(0)
#         if k == 27:
#              break 
# cap.release()
# cv2.destroyAllWindows()