import cv2
import numpy as np
import os
import urllib.request
import subprocess

class Recognition :
    def __init__(self,targetPath, storeWidth=80,storeHeight=72): 
        self.targetPath =targetPath       
        self.storeWidth = storeWidth
        self.storeHeight = storeHeight          

    def capture(self,cap):
        pos,neg=0,0
        if not os.path.exists(self.targetPath):os.makedirs(self.targetPath)
        if not os.path.exists(self.targetPath+'/pos'):os.makedirs(self.targetPath+'/pos')
        if not os.path.exists(self.targetPath+'/neg'):os.makedirs(self.targetPath+'/neg')

        # Se utiliza el primer frame para calcular las posicion y tamano de captura en base al tamano del frame y de la imagen a almacenar
        ret, frame = cap.read()
        if ret == False: return
        h, w, c = frame.shape 
        #obtengo el centro
        cx,cy = int(w/2),int(h/2)
        # calculo el factor entre el tamano de la captura y el de almacenado
        factor= (h*0.5)/self.storeHeight
        # calculo el alto y ancho de captura
        capHeight=int(self.storeHeight*factor)
        capWidth=int(self.storeWidth*factor)
        # calculo las posiciones a dibujar el rectangulo de captura
        x1,y1 = int(cx-(capWidth/2)),int(cy-(capHeight/2))
        x2,y2 = int(cx+(capWidth/2)),int(cy+(capHeight/2))        
        
        while True:
            ret, frame = cap.read()
            if ret == False: return
            cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,0))
            obj = frame[y1:y2,x1:x2]
            resized = cv2.resize(obj,(self.storeWidth,self.storeHeight))
            k = cv2.waitKey(1)            
            if k==ord('p'):
                cv2.imwrite(self.targetPath+'/pos/img_{}.jpg'.format(pos),resized)
                pos = pos + 1
            if k==ord('n'):
                cv2.imwrite(self.targetPath+'/neg/img_{}.jpg'.format(neg),resized)
                neg = neg + 1    
            if k == 27: return
            cv2.imshow('frame',frame)
            cv2.imshow('capture',resized)

    def storeRawImages(self):
        neg_images_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n00523513'   
        neg_image_urls = urllib.request.urlopen(neg_images_link).read().decode()
        neg_path=self.targetPath+'/neg'
        pic_num = 1
        
        if not os.path.exists(neg_path):os.makedirs(neg_path)            
        for i in neg_image_urls.split('\n'):
            try:
                print(i)
                fullpath=neg_path+"/"+str(pic_num)+".jpg"
                urllib.request.urlretrieve(i, fullpath)
                img = cv2.imread(fullpath,cv2.IMREAD_GRAYSCALE)
                # should be larger than samples / pos pic (so we can place our image on it)
                resized_image = cv2.resize(img, (self.storeWidth,self.storeHeight))
                cv2.imwrite(fullpath,resized_image)
                pic_num += 1
                
            except Exception as e:
                print(str(e))

    def createDescriptor(self,type):
        fullPath=self.targetPath+'/'+type
        endLine=None        
        os.path.basename(self.targetPath)             
        for img in os.listdir(fullPath):
            if type == 'pos':endLine = ' 1 0 0 {} {} \n'.format(self.storeWidth,self.storeHeight)
            else: endLine='\n'                    
            line = type+'/'+img+endLine
            with open(self.targetPath+'/'+type+'.dat','a') as f:
                f.write(line)

    def createDescriptors(self):
        self.createDescriptor('pos')
        self.createDescriptor('neg')   

    def createVector(self):
        count=len(open(self.targetPath+'/pos.dat').readlines()) 
        p = subprocess.Popen(['opencv_createsamples', '-info', 'pos.dat', '-num', str(count), '-w', str(self.storeWidth), '-h', str(self.storeHeight),'-vec', 'pos.vec'], cwd=self.targetPath).wait()

    def training(self):
        numPos=len(open(self.targetPath+'/pos.dat').readlines())
        numNeg=len(open(self.targetPath+'/neg.dat').readlines())
        p = subprocess.Popen(['opencv_traincascade', '-data', './', '-vec','./pos.vec','-bg','./neg.dat','-numPos', str(numPos),'-numNeg', str(numNeg),'-numStages', str(2), '-w', str(self.storeWidth), '-h', str(self.storeHeight)], cwd=self.targetPath).wait()

path=os.getcwd()+'/data'
recognition = Recognition(path)
cap=cv2.VideoCapture(0)
recognition.capture(cap)
cap.release()
cv2.destroyAllWindows()
recognition.storeRawImages()
recognition.createDescriptors()  
recognition.createVector()
recognition.training()
