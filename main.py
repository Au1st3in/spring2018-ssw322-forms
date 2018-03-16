'''
Created on Mar 10, 2018

@author: arocha
'''

import models
from user import user
from form import form

def display(userID, formID):
    f = form(userID, formID)
    return

def create(userID, formID):
    f = form(userID, formID)
    
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
            while(sChoice not in {'1','2','LOGOUT'}):
                print("Select display or create form: \n1. Display\n2. Create\n\nLOGOUT")
                sChoice = input()
            if(sChoice == '1'):
                if(len(u.forms) == 0):
                    print("NO FORMS TO Display")
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
            elif(sChoice.upper() == 'LOGOUT'):
                logged_in = False
                u.put()