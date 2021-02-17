import cv2
import numpy as np

class Color:
	def __init__(self,name,low,high):
		self.name = name
		self.low = np.array(low, np.uint8)
		self.high = np.array(high, np.uint8)

class Shape:
	def __init__(self,color,contour):		
		self.color = color
		self.contour = contour
		self.name = Shape.shapeName(contour)
		self.x, self.y, self.w, self.h = cv2.boundingRect(contour)

	def label(self):
		return self.name + ' ' + self.color

	@staticmethod	
	def shapeName(approx):
		if len(approx) == 3:return 'triangle'
		if len(approx) == 4:
			x, y, w, h = cv2.boundingRect(approx)
			ratio = float(w)/h
			if ratio == 1:return 'square '
			else: return 'rectangle'
		if len(approx) == 5:return 'pentagon'
		if len(approx) == 6: return 'hexagon'
		if len(approx) > 10:return 'circle'
		return 'undefined'		

class Analyzer:
	def __init__(self):
		self.colors = Analyzer.getColors()

	@staticmethod
	def getColors():
		list=[]
		list.append(Color('red',[0, 100, 20],[10, 255, 255]))
		list.append(Color('red',[175, 100, 20],[180, 255, 255]))
		list.append(Color('orange',[11, 100, 20],[19, 255, 255]))
		list.append(Color('yellow',[20, 100, 20],[32, 255, 255]))
		list.append(Color('green',[36, 100, 20],[70, 255, 255]))
		list.append(Color('violet',[130, 100, 20],[145, 255, 255]))
		list.append(Color('pink',[146, 100, 20],[170, 255, 255]))
		return list
		
	def color(self,img):
		for color in self.colors:
			mask = cv2.inRange(img, color.low, color.high)
			cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
			if len(cnts)>0: return color.name
		return 'undefined'

	def findContours(self,img):
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		canny = cv2.Canny(gray, 10,150)
		canny = cv2.dilate(canny,None,iterations=1)
		canny = cv2.erode(canny,None,iterations=1)
		cnts,_ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #OpenCV 4
		return cnts

	def shapes(self,image):
		list=[]
		imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		imZeros = np.zeros(image.shape[:2], dtype='uint8')
		cnts=self.findContours(image)
		for c in cnts:
			epsilon = 0.01*cv2.arcLength(c,True)
			approx = cv2.approxPolyDP(c,epsilon,True)
			imAux = cv2.drawContours(imZeros, [c], -1, 255, -1)
			# cv2.imshow('imAux',imAux)
			maskHSV = cv2.bitwise_and(imageHSV,imageHSV, mask=imAux)
			# cv2.imshow('maskHSV',maskHSV)
			color = self.color(maskHSV)
			list.append(Shape(color,approx))
		return list	

analizer =Analyzer()	
image = cv2.imread('figurasColores2.png')
#image = cv2.imread('2.jpg')
shapes=analizer.shapes(image)
for s in shapes:
	cv2.putText(image,s.label(),(s.x,s.y-5),1,0.8,(0,255,0),1)

cv2.imshow('imagen',image)
cv2.waitKey(0)
cv2.destroyAllWindows()