'''
Created on Mar 30, 2018

@author: arocha
'''

import models

if __name__ == "__main__":
    models.flush()
    f = None
    for u in models.User.objects:
        f = models.Form(name="Testing tEst Form", owner=u, published=True, isTest=True)
        f.save()
        q = models.Question(form=f, questionType='trueFalse', question="This statement is True.")
        f.questions = [ q ]
        u.forms = [ f ]
        q.save()
        f.save()
        u.save()
    
    print("USERS")
    for u in models.User.objects:
        print(u.name)
        print(u.email)
        print(u.forms)
        print("\n")
    
    print("FORMS")
    for f in models.Form.objects:
        print(f.owner)
        print(f.published)
        print(f.isTest)
        print(f.questions)
        print(f.userAnswers)
        print(f.correctAnswers)
        print("\n")
        
    print("QUESTIONS")
    for q in models.Question.objects:
        print(q.form)
        print(q.questionType)
        print(q.question)
        print(q.choices)
        print(q.order)
        print(q.points)
        print("\n")