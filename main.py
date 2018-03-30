import json

from flask import Flask, g, jsonify, redirect, render_template, request, send_from_directory, session
from flask_oauth2_login import GoogleLogin

import mongoengine, pymongo

from models import User, Form, Question, Answer

with open('config.json') as cfg:
    config = json.load(cfg)

app = Flask(__name__)
app.config.update(
    DEBUG = config['flask']['debug'],
    SERVER_NAME = config['flask']['host']+':'+str(config['flask']['port']),
    SECRET_KEY= config["google_oauth"]["client_secret"],
    GOOGLE_LOGIN_REDIRECT_SCHEME="http",
    GOOGLE_LOGIN_CLIENT_ID=config["google_oauth"]["client_id"],
    GOOGLE_LOGIN_CLIENT_SECRET=config["google_oauth"]["client_secret"]
)

google_login = GoogleLogin(app)

mongoengine.connect(config['mongodb']['db'], host='mongodb+srv://'+config['mongodb']['user']+':'+config['mongodb']['pass']+'@ssw322-jg1uf.mongodb.net/')

if app.debug:
    from flask_debugtoolbar import DebugToolbarExtension
    debug_toolbar = DebugToolbarExtension()
    debug_toolbar.init_app(app)

@app.route('/login')
def login():
    if g.user is not None:
        return redirect('/dashboard')
    return redirect(google_login.authorization_url())

@app.before_request
def before_request():
    if 'user_id' in session:
        for u in User.objects:
            if(session['user_id'] == str(u.id)):
                g.user = u
                return
    g.user = None
    return

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

@google_login.login_success
def login_success(token, profile):
    for u in User.objects:
        if(u.email == profile['email']):
            g.user = u
            session['user_id'] = str(u.id)
            
            print(u.id)
            print(session['user_id'])
            
            break
    if(not g.user):
        u = User(name = profile['name'], email = profile['email'], forms = [])
        session['user_id'] = str(u.id)
        u.save()
        g.user = u
    
        print(u.id)
        print(session['user_id'])
    
    session['logged_in'] = True
    return redirect('/') #jsonify(token=token, profile=profile)

@google_login.login_failure
def login_failure(e):
    session['logged_in'] = False
    return redirect('/') #jsonify(error=str(e))





@app.route('/')
def index():
    print(g.user)
    return """<html><a href="/login">Login with Google</a>"""

@app.route('/dashboard', methods=['GET', 'POST'])
def dash():
    if g.user:
        return """<html>YESSSS"""
    return """<html>NOPE"""

@app.route('/view/<formID>', methods=['GET', 'POST'])
def display(formID):
    form = None
    for f in Form.objects:
        if(f.id == formID):
            form = f
    if(form):
        return #TODO RENDER FORM VIEW
    return redirect('/') #FORM NOT FOUND

@app.route('/create/<formType>', methods=['GET', 'POST'])
def create(formType):
    if(formType.lower() == 'test'):
        return
    elif(formType.lower() == 'survey'):
        return
    return redirect('/dashboard')



if __name__ == "__main__":
    app.run()
