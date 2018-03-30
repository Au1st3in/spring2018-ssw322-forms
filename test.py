'''
Created on Mar 30, 2018

@author: arocha
'''

import pymongo, mongoengine, json

with open('config.json') as cfg:
    config = json.load(cfg)

if __name__ == "__main__":
    
    questionTypes = ('shortAnswer', 'essay', 'trueFalse', 'multipleChoice', 'matching', 'ranking')
    
    
    #client = pymongo.MongoClient('mongodb+srv://'+config['mongodb']['user']+':'+config['mongodb']['pass']+'@ssw322-jg1uf.mongodb.net/test')
    #client.drop_database(config['mongodb']['db'])
    
    mongoengine.connect(config['mongodb']['db'], host='mongodb+srv://'+config['mongodb']['user']+':'+config['mongodb']['pass']+'@ssw322-jg1uf.mongodb.net/')
    
    class User(mongoengine.Document):
        email = mongoengine.EmailField(required=True, unique=True)
        name = mongoengine.StringField(required=True)
        forms = mongoengine.ListField(mongoengine.ObjectIdField())
        
    class Form(mongoengine.Document):
        owner = mongoengine.ObjectIdField(required=True)
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
    
    for user in User.objects:
        print(user.name)