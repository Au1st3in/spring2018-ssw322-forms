'''
    UNUSED MODULE, REPLACED BY MODELS
'''

import uuid
import sqlite3

DATABASE = "db.sqlite3"
COLUMNS = {"Users" : ["id", "forms"],
           "Forms" : ["id", "ownerID", "questions", "correctAnswers", "userAnswers"],
           "Questions" : ["id", "questionType", "question", "choices", "order"],
           "Answers" : ["id", "questionType", "answer"]}

def generateUUID():
        return str(uuid.uuid4().int)[1:]


def query(table, tag, identity=None):
    q = []
    if(table.title() not in COLUMNS.keys() or tag not in COLUMNS[table.title()]):
        raise ValueError
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    if(identity):
        cur.execute("SELECT "+tag+" FROM "+table.title()+" WHERE id = '"+identity+"'")
    else:
        cur.execute("SELECT "+tag+" FROM "+table.title())
    for fetch in cur.fetchall():
        q.append(fetch[0])
    conn.close()
    return q

def commit(table, cols):
    if(table.title() not in COLUMNS.keys() or len(cols) != len(COLUMNS[table.title()])):
        raise ValueError
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    s = "INSERT INTO "+table.title()+"("
    for col in COLUMNS[table.title()]:
        s += col+","
    s += ") VALUES("
    for var in cols:
        s+= str(var)+","
    s += ");"
    cur.execute(s)
    conn.commit()
    conn.close()