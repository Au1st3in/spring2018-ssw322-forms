'''
Created on Mar 10, 2018

@author: arocha
'''
import models
from random import shuffle

class question:
    questionTypes = ['shortAnswer', 'essay', 'trueFalse', 'multipleChoice', 'matching', 'ranking']
    
    def __init__(self, qT, q=None, c=None, o=None):
        if(qT in self.questionTypes and type(qT) is str):
            self.questionType = qT
            self.questionID = models.generateUUID();
            self.question, self.choices, self.order = None, None, None
            if(self.questionType in self.questionTypes[:3] and isinstance(q, str)):
                self.question = q
            if(self.questionType == self.questionTypes[4] and isinstance(q, str) and isinstance(c, list)):
                self.question = q
                self.choices = c    
            if(self.questionType == self.questionTypes[4] and isinstance(o, tuple)):
                self.order = o
            elif(self.questionType == self.questionTypes[5] and isinstance(o, list)):
                self.order = o
            self.put()
        else:
            raise ValueError()
    
    def id(self):
        return str(self.questionID)
        
    def put(self):
        if(not self.questionType in self.questionTypes or (not self.question and self.choice) or (self.question and self.order) or (self.choices and self.order) or (not (self.question or self.choices or self.order)) or (self.question and self.choices and self.order)):
            raise ValueError()
        if self.order:
            if isinstance(self.order, tuple):
                self.order = (shuffle(self.order[0]), shuffle(self.order[1]))
            else:
                self.order = shuffle(self.order)
        elif self.choices:
            self.choices = shuffle(self.choices)
            
        database.commit('Question', [self.questionID, self.questionType, self.question, self.choices, self.order])