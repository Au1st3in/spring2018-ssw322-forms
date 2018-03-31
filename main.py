import mongoengine, json, models, random

from flask import Flask, redirect, render_template, request, url_for, jsonify
from flask_oauth2_login import GoogleLogin

app = Flask(__name__)
app.config.update(
    DEBUG=models.config['flask']['debug'],
    SERVER_NAME=models.config['flask']['host']+':'+str(models.config['flask']['port']),
    SECRET_KEY=models.config["google_oauth"]["client_secret"],
    GOOGLE_LOGIN_REDIRECT_SCHEME="http",
    GOOGLE_LOGIN_CLIENT_ID=models.config["google_oauth"]["client_id"],
    GOOGLE_LOGIN_CLIENT_SECRET=models.config["google_oauth"]["client_secret"]
)

if app.debug:
    from flask_debugtoolbar import DebugToolbarExtension
    debug_toolbar = DebugToolbarExtension()
    debug_toolbar.init_app(app)

google_login = GoogleLogin(app)

@app.route('/login')
def login():
    if request.cookies.get('user_id'):
        return redirect('/dash')
    return redirect(google_login.authorization_url())

@google_login.login_success
def login_success(token, profile):
    #if not 'hd' in profile or profile['hd'] != 'stevens.edu':
    #    return redirect('/')
    user = None
    response = redirect(url_for('dash'))
    for u in models.User.objects:
        if(u.email == profile['email']):
            user = u
            response.set_cookie('user_id', str(user.id))         
            break
    if(not user):
        user = models.User(name=profile['name'], email=profile['email'], forms=[])
        user.save()
        response.set_cookie('user_id', str(user.id))
    return response #return jsonify(token=token, profile=profile)

@google_login.login_failure
def login_failure(e):
    if app.debug:
        return jsonify(error=str(e))
    return redirect('/')

@app.route('/logout')
def logout():
    response = redirect(url_for('index'))
    if request.cookies.get('user_id'):
        response.set_cookie('user_id', expires=0)
    return response

def logged_in():
    """ """
    user_id = request.cookies.get('user_id')
    if user_id:
        for f in models.Form.objects:
            if(len(f.questions)==0):
                for q in f.questions:
                    q.delete()
                for uA in f.userAnswers:
                    uA.delete()
                for cA in f.correctAnswers:
                    cA.delete()
                f.delete()
    return user(user_id)

def user(user_id):
    if user_id:
        for u in models.User.objects:
            if(user_id == str(u.id)):
                return u
    return None

def form(form_id):
    if form_id:
        for f in models.Form.objects:
            if(form_id == str(f.id)):
                return f
    return None

def question(question_id):
    if question_id:
        for q in models.Question.objects:
            if(question_id == str(q.id)):
                return q
    return None

def answer(answer_id):
    if answer_id:
        for a in models.Answer.objects:
            if(answer_id == str(a.id)):
                return a
    return None


@app.route('/')
def index():
    user = logged_in()
    if user:
        return redirect('/dash')
    return render_template('index.html', user=user)

@app.route('/dash')
def dash():
    user = logged_in()
    if user:
        return render_template('dash.html', user=user)
    return redirect('/')


@app.route('/create-test')
def create_test():
    user = logged_in()
    if user:
        return render_template('create.html', user=user, formType="test", name=None)
    return redirect('/')

@app.route('/create-test', methods=['POST'])
def create_test_post():
    user = logged_in()
    if user:
        name = request.form['text'].strip()
        form = models.Form(name=name, owner=user, isTest=True)
        form.save()
        return render_template('create.html', user=user, isTest=form.isTest, name=name)
    return redirect('/')

@app.route('/create-survey')
def create_survey():
    user = logged_in()
    if user:
        return render_template('create.html', user=user, isTest=False)
    return redirect('/')

@app.route('/<state>') #formID?add=QT&num=NUM
def questions(state):
    user = logged_in()
    if user:
        form = form(state)
        if form:
            question = models.Question(form=form, questionType=request.args.get('add', type=str))
            question.save()
            return render_template('questions/'+str(state)+'.html', user=user, form=form, question=question, questionNumber=request.args.get('num', type=int))
    return redirect('/')

"""
@app.route('/view/<formID>', methods=['GET', 'POST'])
def take(formID):
    form = None
    for f in Form.objects:
        if(f.id == formID):
            form = f
    if(form):
        return #TODO RENDER FORM VIEW
    return redirect('/') #FORM NOT FOUND"""


if __name__ == "__main__":
    app.run()
