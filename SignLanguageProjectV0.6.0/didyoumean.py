from spellchecker import SpellChecker
import cv2
class didYouMean:
    def __init__(self):
         self.spell=SpellChecker()      
         
    def correction(self,word,img):   
        candidatesList=list(self.spell.candidates(word))
        candidatesList=self.preprocessCandidatesList(candidatesList,self.spell.correction(word))
        return candidatesList


    def preprocessCandidatesList(self,candidatesList,bestMatchWord):
        print(bestMatchWord)
        print(candidatesList)
        bestMatchWordIndex=candidatesList.index(bestMatchWord)
        candidatesList[0],candidatesList[bestMatchWordIndex]=candidatesList[bestMatchWordIndex],candidatesList[0]
        return candidatesList
