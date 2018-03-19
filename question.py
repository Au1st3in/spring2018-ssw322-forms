'''
Created on Mar 10, 2018

@author: arocha
'''

import models
#from random import shuffle

questionTypes = ['shortAnswer', 'essay', 'trueFalse', 'multipleChoice', 'matching', 'ranking']

class question:
    
    def __init__(self, questionID, qT, q, c, o):
        self.questionID = questionID
        if not self.get():
            if(qT in questionTypes):
                self.questionType = str(qT)
                self.question = str(q)
                self.choices, self.order = c, o
                self.put()
            else:
                raise ValueError()
        return
    
    def get(self):
        if self.questionID in models.query(models.Questions.id):
            q = models.query(models.Questions, str(self.questionID))
            self.questionType = q.get_questionType()
            self.question = q.get_question()
            self.choices = q.get_choices()
            self.order = q.get_order()
            return True
        return False

    def put(self):
        session = models.Session()
        if self.questionID in models.query(models.Questions.id):
            query = session.query(models.Questions).filter(models.Questions.id == str(self.questionID)).first()
    
            query.questionType = str(self.questionType)
            query.question = str(self.question)
            query.choices = str(self.choices)
            query.order = str(self.order)
            
        else:
            session.add(models.Questions(id=self.questionID, questionType=self.questionType, question=self.question, choices=str(self.choices), order=str(self.order)))
        session.commit()
        session.close()
        return True
    
    def remove(self):
        session = models.Session()
        query = session.query(models.Questions).filter(models.Questions.id == str(self.questionID)).one()
        session.delete(query)
        session.commit()
        session.close()
        return True
    
    
        '''
        if questionID in models.query(models.Questions.id):
            q = question(models.query(models.Questions.id, str(questionID)))
            self.questionType = q.get_questionType()
            self.question = q.get_question()
            self.choices = q.get_choices()
            self.order = q.get_order()
        else:
            if(qT in self.questionTypes and type(qT) is str):
                self.questionType, self.question = str(qT), str(q)
                self.answer, self.choices, self.order = a, c, o
                
                if(self.isTest and ((a and self.questionType in self.questionTypes[:4]) or (o and self.questionType in self.questionTypes[4:]))):
                    answer(self.questionID, a)
                elif(self.isTest and not ((a and self.questionType in self.questionTypes[:4]) or (o and self.questionType in self.questionTypes[4:]))):
                    raise ValueError()
                
                
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
            
        #database.commit('Question', [self.questionID, self.questionType, self.question, self.choices, self.order])'''
        
        