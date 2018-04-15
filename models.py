'''
Created on Mar 30, 2018

@author: arocha
'''

import mongoengine, pymongo, json

with open('config.json') as cfg:
    config = json.load(cfg)

questionTypes = ('shortAnswer', 'essay', 'trueFalse', 'multipleChoice', 'matching', 'ranking')

class User(mongoengine.Document):
    email = mongoengine.EmailField(required=True, unique=True)
    name = mongoengine.StringField(required=True)
    forms = mongoengine.ListField(mongoengine.ReferenceField('Form'))
        
class Form(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    owner = mongoengine.ReferenceField('User', required=True)
    published = mongoengine.BooleanField(required=True, default=False)
    isTest = mongoengine.BooleanField(required=True)
    questions = mongoengine.ListField(mongoengine.ReferenceField('Question'), default=[])
    userAnswers = mongoengine.ListField(mongoengine.ListField(mongoengine.ReferenceField('Answer')), default=[])
    correctAnswers = mongoengine.ListField(mongoengine.ReferenceField('Answer'), default=[])
        
class Question(mongoengine.Document):
    form = mongoengine.ReferenceField('Form')
    questionType = mongoengine.StringField(required=True, choices=questionTypes)
    question = mongoengine.StringField(required=True, default="")
    choices = mongoengine.ListField(default=[])
    order = mongoengine.ListField(default=[])
    points = mongoengine.IntField(default=5)
    
class Answer(mongoengine.Document):
    owner = mongoengine.ReferenceField('User', required=True) #Either User or Form
    question = mongoengine.ReferenceField('Question', required=True)
    answer =  mongoengine.StringField(required=True)

def user(user_id):
    if user_id:
        for u in User.objects:
            if(user_id == str(u.id)):
                return u
    return None

def form(form_id):
    if form_id:
        for f in Form.objects:
            if(form_id == str(f.id)):
                return f
    return None

def question(question_id):
    if question_id:
        for q in Question.objects:
            if(question_id == str(q.id)):
                return q
    return None

def answer(answer_id):
    if answer_id:
        for a in Answer.objects:
            if(answer_id == str(a.id)):
                return a
    return None

mongoengine.connect(config['mongodb']['db'], host='mongodb+srv://'+config['mongodb']['user']+':'+config['mongodb']['pass']+'@ssw322-jg1uf.mongodb.net/')

def flush():
    client = pymongo.MongoClient('mongodb+srv://'+config['mongodb']['user']+':'+config['mongodb']['pass']+'@ssw322-jg1uf.mongodb.net/test')
    client.drop_database(config['mongodb']['db'])
    client.close()
    user = User(email=config['admin']['email'], name=config['admin']['name'], forms=[])
    user.save()