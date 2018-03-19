'''
Created on Mar 10, 2018

@author: arocha
'''

import models
from question import question as q
from answer import answer as a

class form:
    def __init__(self, userID, formID):
        self.userID = userID
        self.formID = formID
        self.isTest = formID[:1].upper() == 'T'
        if formID in {'S','T'} or not self.get():
            self.isOwner = True
            self.ownerID = self.userID
            self.questions = []
            self.userAnswers = {}
            self.correctAnswers = []
            self.put()
    
    def get_questions(self):
        Qs = []
        for qID in self.questions:
            Qs.append(q(qID))
        return Qs
    
    def get_userAnswers(self):
        uA = {}
        for uID in self.userAnswers.keys():
            As, answers = [], self.userAnswers[uID]
            for aID in answers:
                As.append(a(aID))
            uA[uID] = As
        return uA
    
    def get_correctAnswers(self):
        cA = []
        for aID in self.correctAnswers:
            cA.append(a(aID))
        return cA
    
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
            session.add(models.Forms(id=models.generateUUID(self.formID[:1]), ownerID=self.ownerID, questions=str(self.questions), userAnswers=str(self.userAnswers), correctAnswers=str(self.correctAnswers)))
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
        
    def addQuestion(self, questionType, question=None, choices=None, order=None):        
        if self.isOwner:
            qN = q(models.generateUUID('q'), questionType, question, choices, order)
        self.questions.append(qN.questionID)
        self.put()
        return qN.questionID
        
    def addAnswer(self, questionID, answer=None, order=None):
        #print(models.generateUUID('a')+" "+self.userID+" "+questionID+" "+order)
        if answer:
            aN = a(models.generateUUID('a'), self.userID, questionID, answer)
        else:
            aN = a(models.generateUUID('a'), self.userID, questionID, order)
        if self.isOwner:
            self.correctAnswers.append(aN.answerID)
        else:
            self.userAnswers.append(aN.answerID)
        return aN.answerID
        