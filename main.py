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

def logged_in():
    """ """
    user_id = request.cookies.get('user_id')
    if user_id:
        for u in models.User.objects:
            if(user_id == str(u.id)):
                return u
    return None

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

@app.route('/remove/<state>')
def remove(state):
    """ Removes Form from Database """
    user = logged_in()
    if user:
        f = models.form(state)
        if f in user.forms and f:
            user.forms.remove(f)
            user.save()
            for qF in f.questions:
                qF.delete()
            for caF in f.correctAnswers:
                caF.delete()
            for uaF in f.userAnswers:
                for uA in uaF:
                    uA.delete()
            f.delete()
        return redirect('/dash')
    return redirect('/')

@app.route('/view/<state>')
def view(state):
    """ Displays Form Questions and Answers """
    user = logged_in()
    f = models.form(state)
    if f:
        if(f.published and f.owner==user):
            return render_template('view.html', form=f)
    return take(state)

@app.route('/take/<state>')
def take(state):
    """  """
    user = logged_in()
    f = models.form(state)
    if f:
        if(f.published and f.owner==user):
            return view(state)
        elif(f.published):
            return render_template('take.html', form=f)
        return render_template('unpublished.html', user=user, isTest=f.isTest)
    else:
        return render_template('unpublished.html', user=user, isTest=None)






@app.route('/create/<formType>/temp')
def create_iframe(formType):
    """  """
    user = logged_in()
    if user and formType.lower() in {'test', 'survey'}:
        return render_template('create/_temp.html', isTest=formType.lower()=='test')
    return redirect('/')

@app.route('/create/<formType>', methods=['GET', 'POST'])
def create(formType):
    """  """
    user = logged_in()
    if user and formType.lower() in {'test', 'survey'}:
        form = None
        isTest = (formType.lower() == 'test')
        print(formType)
        print(isTest)
        if request.method == 'POST':
            form = models.Form(owner=user, published=False, isTest=isTest, name=request.form['text'].strip())
            form.save()
            user.forms.append(form)
            user.save()
        if form:
            return render_template('create.html', user=user, formID=form.id, isTest=form.isTest, name=form.name)
        return render_template('create.html', user=user, formID=None, isTest=isTest, name=None)
    return redirect('/')

@app.route('/create/<formType>/<questionType>/<formID>', methods=['GET', 'POST'])
def add_question(formType, questionType, formID):
    """  """
    user = logged_in()
    if user and formType.lower() in {'test', 'survey'}:
        form = models.form(formID)
        if request.method == 'POST' and questionType in models.questionTypes and form:
            a = None
            if questionType in {'shortAnswer', 'essay'}:
                if form.isTest:
                    q = models.Question(form=form, questionType=questionType, question=request.form['question'].strip(), points=int(request.form['points']))
                else:
                    q = models.Question(form=form, questionType=questionType, question=request.form['question'].strip())
            elif questionType == "trueFalse":
                if form.isTest:
                    q = models.Question(form=form, questionType=questionType, question=request.form['question'].strip(), points=int(request.form['points']))
                    a = models.Answer(owner=user, question=q, answer=str(request.form['answer']))
                else:
                    q = models.Question(form=form, questionType=questionType, question=request.form['question'].strip())
            elif questionType == 'multipleChoice':
                choices = []
                for c in range(1, int(request.form['choices'])+1):
                    choices.append(str(request.form['c'+str(c)]))
                if form.isTest:
                    q = models.Question(form=form, questionType=questionType, question=request.form['question'].strip(), points=int(request.form['points']), choices=choices)
                    a = models.Answer(owner=user, question=q, answer=choices[int(request.form['answer'])-1])
                else:
                    q = models.Question(form=form, questionType=questionType, question=request.form['question'].strip(), choices=choices)
            elif questionType == 'matching':
                order = [[],[]]
                for mr in  range(1, int(request.form['matches'])+1):
                    order[0].append(str(request.form['mr'+str(mr)]))
                for me in  range(1, int(request.form['matches'])+1):
                    try:
                        order[1].append(str(request.form['me'+str(me)]))
                    except:
                        order[1].append("")
                if form.isTest:
                    answer = {}
                    for m in order[0]:
                        answer[m] = []
                    for a in  range(1, int(request.form['matches'])+1):
                        answer[(order[0][int(request.form['answer'+str(a)][1])-1])].append(order[1][int(request.form['answer'+str(a)][3])-1])      
                    q = models.Question(form=form, questionType=questionType, question=request.form['question'].strip(), points=int(request.form['points']), order=[random.sample(order[0], len(order[0])),random.sample(order[1], len(order[1]))])
                    a = models.Answer(owner=user, question=q, answer=str(answer))
                else:
                    q = models.Question(form=form, questionType=questionType, question=request.form['question'].strip(), order=order)                  
            elif questionType == 'ranking':
                order = []
                for r in range(1, int(request.form['ranks'])+1):
                    order.append(str(request.form['r'+str(r)]))
                if form.isTest:
                    q = models.Question(form=form, questionType=questionType, question=request.form['question'].strip(), points=int(request.form['points']), order=random.sample(order, len(order)))
                    a = models.Answer(owner=user, question=q, answer=str(order))
                else:
                    q = models.Question(form=form, questionType=questionType, question=request.form['question'].strip(), order=order)
            q.save()
            form.questions.append(q)
            if a:
                a.save()
                form.correctAnswers.append(a)
            form.save()
        if form:
            return render_template('create/'+str(questionType)+'.html', user=user, questions=len(form.questions), formID=form.id, isTest=form.isTest, name=form.name)
    return redirect('/')

@app.errorhandler(404)
def page_not_found(e):
    ''' Page Not Found Redirect '''
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run()
