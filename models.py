'''
Created on Mar 30, 2018

@author: arocha
'''

import mongoengine

questionTypes = ('shortAnswer', 'essay', 'trueFalse', 'multipleChoice', 'matching', 'ranking')

class User(mongoengine.Document):
    email = mongoengine.EmailField(required=True, unique=True)
    name = mongoengine.StringField(required=True)
    forms = mongoengine.ListField(mongoengine.ObjectIdField())
        
class Form(mongoengine.Document):
    owner = mongoengine.ObjectIdField(required=True)
    isTest = mongoengine.BooleanField(required=True)
    questions = mongoengine.ListField(required=True)
    userAnswers = mongoengine.ListField(mongoengine.ListField(mongoengine.ObjectIdField()))
    correctAnswers = mongoengine.ListField(mongoengine.ObjectIdField())
        
class Question(mongoengine.Document):
    form = mongoengine.StringField(required=True)
    questionType = mongoengine.StringField(required=True, choices=questionTypes)
    question = mongoengine.StringField(required=True)
    choices = mongoengine.ListField()
    order = mongoengine.ListField()
    points = mongoengine.IntField(default=5)
    
class Answer(mongoengine.Document):
    owner = mongoengine.ObjectIdField(required=True) #Either User or Form
    question = mongoengine.ObjectIdField(required=True)
    answer =  mongoengine.StringField(required=True)