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
    return models.user(user_id)

@app.route('/')
def index():
    """ Home Login Button Page """
    user = logged_in()
    if user:
        return redirect('/dash')
    return render_template('index.html', user=user)

@app.route('/dash')
def dash():
    """ Logged In User's Dashboard """
    user = logged_in()
    if user:
        return render_template('dash.html', user=user)
    return redirect('/')







@app.route('/publish/<state>')
def publish(state):
    """ Toggles published status for Form """
    user = logged_in()
    if user:
        f = models.form(state)
        f.published = not f.published
        f.save()
        return redirect('/dash')
    return redirect('/')

@app.route('/view/<state>')
def view(state):
    """ Displays Form Questions and Answers """
    user = logged_in()
    f = models.form(state)
    if(f.published or f.owner==user):
        return #PUBLISHED
    return #NOT PUBLISHED

@app.route('/remove/<state>')
def remove(state):
    """ Removes Form from Database """
    user = logged_in()
    if user:
        f = models.form(state)
        f.delete()
        return redirect('/dash')
    return redirect('/')







@app.route('/create-test')
def create_test():
    """  """
    user = logged_in()
    if user:
        return render_template('create.html', user=user, formType="test", name=None)
    return redirect('/')

@app.route('/create-test', methods=['POST'])
def create_test_post():
    """  """
    user = logged_in()
    if user:
        name = request.form['text'].strip()
        form = models.Form(name=name, owner=user, isTest=True)
        form.save()
        return render_template('create.html', user=user, isTest=form.isTest, name=name)
    return redirect('/')

@app.route('/<state>') #formID?add=QT&num=NUM
def questions(state):
    """  """
    user = logged_in()
    if user:
        form = models.form(state)
        if form:
            question = models.Question(form=form, questionType=request.args.get('add', type=str))
            form.questions.append(question)
            question.save()
            form.save()
            return render_template('create/'+question.questionType+'.html', user=user, form=form, question=question, questionNumber=request.args.get('num', type=int))
    return redirect('/')







@app.route('/create-survey')
def create_survey():
    """  """
    user = logged_in()
    if user:
        return render_template('create.html', user=user, isTest=False)
    return redirect('/')





if __name__ == "__main__":
    app.run()
