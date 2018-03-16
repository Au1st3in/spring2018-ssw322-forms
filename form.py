'''
Created on Mar 10, 2018

@author: arocha
'''

import models
from question import question

class form:
    def __init__(self, userID, formID):
        self.userID = userID
        self.formID = formID
        self.isTest = formID[:1].upper() == 'T'
        if formID in {'S','T'} or not self.get():
            self.isOwner = True
            self.questions = []
            self.userAnswers = {}
            self.correctAnswers = []
            self.put(models.generateUUID(formID[:1]), self.userID, self.questions, self.userAnswers, self.correctAnswer)
    
    def get(self):
        if self.formID in models.query(models.Forms.id):
            f = models.query(models.Forms, str(self.formID))
            self.isOwner = self.userID == f.get_ownerID()
            self.questions = f.get_questions()
            self.userAnswers =  f.get_userAnswers()
            if self.isTest:
                self.correctAnswers = f.get_correctAnswers()
            else:
                self.correctAnswers = []
            return True
        return False
    
    def put(self):
        session = models.Session()
        if self.formID in models.query(models.Forms.id):
            query = session.query(models.Forms).filter(models.Forms.id == str(self.formID)).first()
            query.questions = str(self.questions)
            query.userAnswers = str(self.userAnswers)
            query.correctAnswers = str(self.correctAnswers)
        else:
            session.add(models.Forms(id=self.formID, ownerID=self.ownerID, questions=str(self.questions), userAnswer=str(self.userAnswers), correctAnswers=str(self.correctAnswers)))
        session.commit()
        session.close()
        return True
    
    def remove(self):
        session = models.Session()
        query = session.query(models.Forms).filter(models.Forms.id == str(self.formID)).one()
        correctAnswers, questions, userAnswers = query.get_correctAnswers(), query.get_questions(), query.get_userAnswers()
        session.delete(query)
            
        for answer in correctAnswers:
            query = session.query(models.Answers).filter(models.Answers.id == str(answer)).one()
            session.delete(query)
            
        for question in questions:
            query = session.query(models.Questions).filter(models.Questions.id == str(question)).one()
            session.delete(query)
    
            for answer in userAnswers[str(question)]:
                query = session.query(models.Answers).filter(models.Answers.id == str(answer)).one()
                session.delete(query)
        session.commit()
        session.close()
        return True
        
    
    def question(self, questionType, q=None, a=None, choices=None, order=None):        
        if self.isOwner:
            '''q1 = question(questionType, q, choices, order)
            if self.isTest:
                a1 = answer(questionType, a)
                self.correctAnswers.append(a1)
            self.questions.append(q1)'''
        