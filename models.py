'''
Created on Mar 10, 2018

@author: arocha
'''

import uuid, ast
from sqlalchemy.orm import sessionmaker#, relationship
from sqlalchemy import create_engine, Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

DEBUG = True
DATABASE = 'db.sqlite3'
PREFIXES = {'U': 'User', 'T': 'Test', 'S': 'Survey', 'Q': 'Question', 'A': 'Answer'}
Base = declarative_base()

class Users(Base):
    __tablename__ = "Users"
    
    id = Column('id', String, primary_key=True, unique=True)
    forms = Column('forms', String, unique=True)
    
    def get_id(self):
        return str(self.id)
    
    def get_forms(self):
        return ast.literal_eval(self.forms)
    
    #def __str__(self):
    #    return "["+str(self.id)+", "+str(self.forms)+"]"

class Forms(Base):
    __tablename__ = "Forms"
    
    id = Column('id', String, primary_key=True, unique=True)
    ownerID = Column('ownerID', String, ForeignKey('Users.id'))
    questions = Column('questions', String, unique=True)
    userAnswers = Column('userAnswers', String, unique=True)
    correctAnswers = Column('correctAnswers', String, unique=True)
 
    def get_id(self):
        return str(self.id)
    
    def get_ownerID(self):
        return str(self.ownerID)
    
    def get_questions(self):
        return ast.literal_eval(self.questions)
    
    def get_userAnswers(self):
        return ast.literal_eval(self.userAnswers)
    
    def get_correctAnswers(self):
        return ast.literal_eval(self.correctAnswers)
    
    #def __str__(self):
    #    return "["+str(self.id)+", "+str(self.owner)+", "+str(self.questions)+", "+str(self.correctAnswers)+", "+str(self.userAnswers)+"]"
    
class Questions(Base):
    __tablename__ = "Questions"
    
    id = Column('id', String, primary_key=True, unique=True)
    formID = Column('formID', String, ForeignKey('Forms.id'))
    questionType = Column('questionType', String)
    question = Column('question', String)
    choices = Column('choices', String)
    order = Column('order', String)
    
    def get_id(self):
        return str(self.id)
    
    def get_formID(self):
        return str(self.formID)
    
    def get_questionType(self):
        return str(self.questionType)
    
    def get_question(self):
        return str(self.question)
    
    def get_choices(self):
        return ast.literal_eval(self.choices)
    
    def get_order(self):
        return ast.literal_eval(self.order)
    
    #def __str__(self):
    #    return "["+str(self.id)+", "+str(self.questionType)+", "+str(self.question)+", "+str(self.choices)+", "+str(self.order)+"]"
    
class Answers(Base):
    __tablename__ = "Answers"
    
    id = Column('id', String, primary_key=True, unique=True)
    userID = Column('ownerID', String, ForeignKey('Users.id'))
    questionID = Column('questionID', String, ForeignKey('Questions.id'))
    answer = Column('answer', String)
    
    def get_id(self):
        return str(self.id)
    
    def get_userID(self):
        return str(self.userID)
    
    def get_questionID(self):
        return str(self.questionID)
    
    def get_answer(self):
        if str(self.answer).title() in {'True', 'False'}:
            return bool(self.answer)
        elif '[' in str(self.answer):
            try:
                a = ast.literal_eval(self.answer)
            except:
                a = str(self.answer)
        return a
    
    #def __str__(self):
    #    return "["+str(self.id)+", "+str(self.questionType)+", "+str(self.answer)+"]"

engine = create_engine('sqlite:///'+DATABASE, echo=DEBUG)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

def generateUUID(prefix=''):
    if prefix and prefix in PREFIXES.keys():
        return str(prefix).upper()+str(uuid.uuid4().int)[1:]
    return str(uuid.uuid4().int)

def query(model, identity=None):
    session = Session()
    if identity:
        query = session.query(model).filter(model.id == str(identity)).one()
    else:
        query = session.query(model).all()
    session.close()
    return query

'''
def add(model):
    session = Session()
    if(isinstance(model, list)):
        session.bulk_save_objects(model)
    else:
        session.add(model)
    session.commit()
    session.close()

def update(model, new, identity):
    session = Session()
    query = session.query(model).filter(model.id == str(identity)).first()
    query = new
    session.close()
    return query
    
def delete(model, identity):
    session = Session()
    query = session.query(model).filter(model.id == str(identity)).one()
    session.delete(query)
    session.close()
    return query
'''