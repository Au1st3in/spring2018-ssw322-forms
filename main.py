'''
Created on Mar 10, 2018

@author: arocha
'''

#import database

import models

if __name__ == "__main__":
    '''print(database.query('id', 'forms'))'''
    
    user = models.query(models.Users.id)
    
    print('Hello '+str(user))
