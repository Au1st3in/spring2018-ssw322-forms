'''
Created on Mar 16, 2018

@author: arocha
'''

import models

class user:
    
    def __init__(self, userID=None):
        if userID:
            self.userID = userID
        else:
            self.userID = models.generateUUID('u')
        if not self.get():
            self.forms = []
    
    def get(self):
        if self.userID in models.query(models.Users.id):
            self.forms = models.query(models.Users, str(self.userID)).get_forms()
            return True
        return False
    
    def put(self):
        session = models.Session()
        if self.userID in models.query(models.Users.id):
            query = session.query(models.Users).filter(models.Users.id == str(self.userID)).first()
            query.forms = str(self.forms)
        else:
            session.add(models.Users(id=self.userID, forms=str(self.forms)))
        session.commit()
        session.close()
        return True
    
    def remove(self):
        session = models.Session()
        query = session.query(models.Users).filter(models.Users.id == str(self.userID)).one()
        forms = query.get_forms()
        session.delete(query)
        
        for form in forms:
            query = session.query(models.Forms).filter(models.Forms.id == str(form)).one()
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