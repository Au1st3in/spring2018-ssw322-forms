'''
Created on Mar 10, 2018

@author: arocha
'''

import models
from user import user
from form import form
from question import questionTypes
from random import shuffle

def display(userID, formID):
    f = form(userID, formID)
    return

def create(userID, formID):
    done = False
    f = form(userID, formID)
    
    while(not done):
        qChoice, question, answer, choice, order = 0, None, None, None, None
        while(qChoice not in range(1, len(questionTypes)+2)):
            print("\nSelect a question type to create (Enter Anything Else to Quit): ")
            for i in range(1, len(questionTypes)+1):
                    print(str(i)+". "+str(questionTypes[i-1]))
            print('7. Quit')
            try:
                qChoice = int(input())
            except:
                qChoice = 7
                
        if(qChoice in {1,2}):
            question = input(questionTypes[qChoice-1]+" Question: ")
            if(f.isTest and choice == 1):
                answer = input(questionTypes[qChoice-1]+" Answer: ")
        elif(qChoice == 3):
            question = input(questionTypes[qChoice-1]+" Question: ")
            if(f.isTest):
                answer = bool(input(questionTypes[qChoice-1]+" Answer: "))
        elif(qChoice == 4):
            doneChoice, count, choice = False, 1, []
            while(not doneChoice):
                choice.append(input(questionTypes[qChoice-1]+" Choice #"+str(count)+" (Input DONE when finished): "))
                if(choice[count-1].upper() == "DONE"):
                    doneChoice = True
                    del choice[-1]
                else:
                    count += 1

            if(f.isTest):
                answerChoice = False
                while(not answerChoice):
                    for i in range(1, len(choice)+1):
                        print(str(i)+". "+str(choice[i-1]))
                    aChoice = int(input("Select correct Answer: "))
                    if(aChoice in range(1, len(choice)+1)):
                        answer = choice[aChoice-1]
                        answerChoice = True
        elif(qChoice == 5):
            doneMatch, count, t1, t2 = False, 1, [], []
            print("Input Matchers first, then Matchees")
            while(not doneMatch):
                t1.append(input(questionTypes[qChoice-1]+" Matcher #"+str(count)+" (Input DONE when finished): "))
                if(t1[count-1].upper() == "DONE"):
                    doneMatch = True
                    del t1[-1]
                else:
                    count += 1
            for i in range(0, len(t1)):
                if(f.isTest):
                    t2.append(input(questionTypes[qChoice-1]+" Matchee #"+str(count)+" for "+t1[i]+": "))
                else:
                    t2.append(input(questionTypes[qChoice-1]+" Matchee #"+str(count)+": "))
            if(f.isTest):
                answer = tuple(tuple(t1), tuple(t2))
            order = tuple(tuple(shuffle(t1)), tuple(shuffle(t2)))
        elif(qChoice == 6):
            doneRank, count, r = False, 1, []
            while(not doneRank):
                if(f.isTest):
                    r.append(input(questionTypes[qChoice-1]+" Rank #"+str(count)+" (Input DONE when finished): "))
                else:
                    r.append(input(questionTypes[qChoice-1]+" Rankee #"+str(count)+" (Input DONE when finished): "))
                if(r[count-1].upper() == "DONE"):
                    doneRank = True
                    del r[-1]
                else:
                    count += 1

            if(f.isTest):
                answer = tuple(r)
            order = tuple(shuffle(r))
        else:
            done = True
        
        if(not done):
            qID = f.addQuestion(questionTypes[qChoice-1], question, choice, order)
            if(f.isTest):
                f.addAnswer(qID, answer, order)
    display(userID, f.formID)

if __name__ == "__main__":
    logged_in = False
    while(True):
        if(not logged_in):
            users = models.query(models.Users)
            print("Select an existing user or create a new user: ")
            for i in range(1, len(users)+1):
                print(str(i)+". "+str(users[i-1].get_id()))
            print(str(len(users)+1)+". NEW USER")
            uChoice = int(input())
            if(uChoice in range(1, len(users)+1)):
                u = user(users[uChoice-1].get_id())
                u.forms = users[uChoice-1].get_forms()
            else:
                u = user()
                u.forms = []
            logged_in = True
            sChoice = '0'
        if(logged_in):
            while(sChoice not in {'1','2', '3', 'LOGOUT'}):
                print("\nSelect display or create form: \n1. Display\n2. Create\n3. Logout")
                sChoice = input()
            if(sChoice == '1'):
                if(len(u.forms) == 0):
                    print("\nNO FORMS TO Display")
                    sChoice = '0'
                else:
                    dChoice = 0
                    while(dChoice not in len(u.forms)+1):
                        print("Select form to display: ")
                        for i in range(1, len(u.forms)+1):
                            print(str(i)+". "+str(u.forms[i-1]))
                        dChoice = int(input())
                    display(u.userID, u.forms[dChoice-1])
            elif(sChoice == '2'):
                cChoice = 0
                formType = {1:'S',2:'T'}
                while(cChoice not in {1,2}):
                    print("Select form type to create: \n1. Survey\n2. Test")
                    cChoice = int(input())
                create(u.userID, formType[cChoice])
                sChoice = '1'
            elif(sChoice.upper() == 'LOGOUT' or sChoice == '3'):
                logged_in = False
                u.put()