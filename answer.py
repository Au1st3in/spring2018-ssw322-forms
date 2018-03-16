'''
Created on Mar 10, 2018

@author: arocha
'''

import models

class answer:
    
    def __init__(self, answerID, userID, questionID=None, a=None):
        self.answerID = answerID
        self.userID = userID
        if not self.get():
            if questionID and a:
                self.questionID = questionID
                self.answer = a
            else:
                raise ValueError()
    
    def get(self):
        if self.answerID in models.query(models.Answers.id):
            a = models.query(models.Answers, str(self.answerID))
            self.questionID = a.get_questionID()
            self.answer = a.get_answer()
            return True
        return False
    
    def put(self):
        session = models.Session()
        if self.answerID in models.query(models.Answers.id):
            query = session.query(models.Answers).filter(models.Answers.id == str(self.answerID)).first()
            query.questionID = str(self.questionID)
            query.answer = str(self.answer)
        else:
            session.add(models.Answers(id=self.answerID, questionID=self.questionID, answer=str(self.answer)))
        session.commit()
        session.close()
        return True
    
    def remove(self):
        session = models.Session()
        query = session.query(models.Answers).filter(models.Answers.id == str(self.answerID)).one()
        session.delete(query)
        session.commit()
        session.close()
        return True