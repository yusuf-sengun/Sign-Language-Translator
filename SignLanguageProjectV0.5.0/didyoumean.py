from spellchecker import SpellChecker
import cv2
class didYouMean:
    def __init__(self):
         self.spell=SpellChecker()
         
         
         
    def correction(self,word,img):   
        
        candidatesList=list(self.spell.candidates(word))
        candidatesList=self.preprocessCandidatesList(candidatesList,self.spell.correction(word))
        for i in range(len(candidatesList)): 
            cv2.putText(img,str(i+1)+"->"+candidatesList[i],(450,(i)*20+100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0), 1, cv2.LINE_AA)
        
        while True:
            cv2.imshow("Image",img)
            k=cv2.waitKey(1)
            for i in range(len(candidatesList)):
               if k==i+49:
                  return candidatesList[i]
            if k==27:
                break
            

        return ""

    def preprocessCandidatesList(self,candidatesList,bestMatchWord):
        print(bestMatchWord)
        print(candidatesList)
        bestMatchWordIndex=candidatesList.index(bestMatchWord)
        candidatesList[0],candidatesList[bestMatchWordIndex]=candidatesList[bestMatchWordIndex],candidatesList[0]
        candidatesList=candidatesList[:9]
        return candidatesList
