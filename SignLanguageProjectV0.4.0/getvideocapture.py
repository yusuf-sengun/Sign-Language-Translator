import cv2
import numpy as np
import prediction
from spellchecker import SpellChecker

class getVideoCapture:
    def __init__(self):
        spell=SpellChecker()
        self.cap = cv2.VideoCapture(0)
        self.prediction=prediction.Prediction()
        while(self.cap.isOpened()):
            
           self.createRectangleOnVideo()
           croppedImage = self.getImageOnRectangle()
           extractedSkin=self.extractSkin(croppedImage)
           contours,thresHoldedImage=self.preprocessImage(croppedImage,extractedSkin)
           self.putTextToVideo(self.prediction.myString)
           
           if self.isHandInRectangle(contours):
               targetOfImage= max(contours,key=lambda x: cv2.contourArea(x))
               if cv2.contourArea(targetOfImage) > 2500:         
                   self.prediction.predictLetter(thresHoldedImage)
                   self.printPredictedLetter()   
           else:
               self.prediction.totalPredictCount=0
               if self.prediction.letterList:
                   self.prediction.clearList()

           dataset_img=cv2.imread(r'C:\Users\olgun\Desktop\SEProject\Dataset\amer_sign2.png')
           cv2.imshow('Dataset',dataset_img)
           cv2.imshow("Image",self.img)
           key=cv2.waitKey(33)
           if key == ord('q'):
               cv2.destroyAllWindows()
               break
           elif key==ord('y'):
               print(spell.correction(self.prediction.myString))
               print(spell.candidates(self.prediction.myString))
           elif key==ord('\b'):
              self.prediction.myString=self.prediction.myString[:-1]
           elif key==ord(' '):
               self.prediction.myString+='_'
        
        
    def createRectangleOnVideo(self):
        start_point=(300,300)
        end_point=(100,100)
        color=(0,255,0)
        thickness=0
        self.ret, self.img = self.cap.read()
        self.img = cv2.flip(self.img, 1)    
        cv2.rectangle(self.img,start_point,end_point,color,thickness)
        
    def getImageOnRectangle(self):
        start_point=(300,300)
        end_point=(100,100)
        return self.img[end_point[0]:start_point[0],end_point[0]:start_point[0]]
    
    def extractSkin(self,croppedImage):
        lowerSkinColor = np.array([0,58,50], dtype=np.uint8)
        upperSkinColor = np.array([30,255,255], dtype=np.uint8)
        hsv = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2HSV)
        return cv2.inRange(hsv, lowerSkinColor, upperSkinColor)
        
    def preprocessImage(self,croppedImage,extractedSkin):
        grayedImage=cv2.cvtColor(croppedImage,cv2.COLOR_BGR2GRAY)    
        bluredImage=cv2.GaussianBlur(grayedImage,(5,5),2)
        thresHoldedImage = cv2.adaptiveThreshold(bluredImage,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
        _, thresHoldedImage = cv2.threshold(thresHoldedImage, 70, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        contours,hierarchy=cv2.findContours(extractedSkin.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        return contours,thresHoldedImage
    def putTextToVideo(self,text):
        cv2.putText(self.img,self.prediction.myString,(150,400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1, cv2.LINE_AA)
        
    def isHandInRectangle(self,contours):
        if len(contours)>0:
            return True
        return False
    
    def printPredictedLetter(self):
       color=(0,255,0)
       counter=0
       for pred_letter,pred_acc,pred_count in zip(self.prediction.letterList,self.prediction.probList,self.prediction.countList):
           color_list=(0,0,255)
           if(pred_acc>=0.95):
               color_list=(0,128,0)#green
           elif(pred_acc>0.8):
               color_list=(255,255,0)#yellow
           cv2.putText(self.img,pred_letter,(counter*150,50), cv2.FONT_HERSHEY_SIMPLEX, 2, color_list, 3, cv2.LINE_AA)
           cv2.rectangle(self.img,(450,5),(600,35),(0,0,255),-1)
           cv2.rectangle(self.img,(450,5),(450+self.prediction.totalPredictCount*2,35),color,-1)
           formatted_pred_acc=format(round(pred_acc,2)*100,'.2f')
           cv2.putText(self.img,"%"+formatted_pred_acc,(counter*150,90), cv2.FONT_HERSHEY_SIMPLEX, 1, color_list, 1, cv2.LINE_AA)
           cv2.putText(self.img,str(pred_count),(counter*150,400), cv2.FONT_HERSHEY_SIMPLEX, 1, color_list, 1, cv2.LINE_AA)
           counter+=1
