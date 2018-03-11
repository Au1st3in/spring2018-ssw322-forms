'''
Created on Mar 10, 2018

@author: arocha
'''

import models
import question, answer

class form:
    
    def __init__(self, userID, formID):
        self.correctAnswer = None
        self.questions = []
        
        if formID in models.query(models.Forms.id):
            self.isTest = formID[:1].upper() == 'T'
            self.isOwner = userID == models.query(models.Forms.ownerID, str(formID))
            for q in (models.query(models.Forms, str(formID))).get_questions():
                #self.questions.append()
            
            if self.isTest:
                self.correctAnswer = answer.get(database.query('Forms', 'correctAnswers', str(formID))[0])'''
            
        else:
            
            """ Implement Create Function """
            self.owner = userID

        '''   
        self.questions, self.userAnswers = [], []
        
        self.generateFormID()
        if isTest:
            self.correctAnswer = answer()
        else:
            self.correctAnswer = None '''


    def load(self, formID):
        return

    def addQ(self, questionType, q=None, a=None, c=None, order=None):
        if self.isOwner:
            
    
    def addA(self, questionType, a):
        
    
        