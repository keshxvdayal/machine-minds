from flask import Flask, render_template, redirect, url_for, session, request, jsonify, make_response, send_from_directory
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_dance.contrib.google import make_google_blueprint, google
import matplotlib.backends
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError
from requests.models import Response

from sklearn.preprocessing import MinMaxScaler
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.metrics import log_loss
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import ExtraTreesClassifier


from matplotlib import pyplot as plt
import matplotlib
from io import BytesIO
import numpy as np
from pandas import DataFrame

import pygal
import pygal.style

from dotenv import load_dotenv

from consts import *

from os import environ
from datetime import datetime
import json

load_dotenv()




'''
levels-config.json will be like

{
    "1": {
        "classifier": "knn",
        "hyperparameters-fix": {
            "metric": "euclidean"
        },
        "hyperparameters-input": [
            ["n_neighbors", "int"]
        ]
    }
}

levels-data will be like

{
    "1": {
        "X": [[1, 2], [3, 4], [5, 6]],
        "Y": [0, 1, 0]
    }
}
'''





# -------------------- Main App --------------------
app = Flask(__name__)
api = Api(app)
app.secret_key = 'super'
CORS(app)
# -------------------- Database config --------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
# -------------------- Session config --------------------
app.config['SESSION_TYPE']             = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY']       = db
app.config['SESSION_SQLALCHEMY_TABLE'] = 'sessions'
Session(app)
# -------------------- Google Auth config --------------------
environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # ONLY ON LOCAL ENV
blueprint = make_google_blueprint(
    client_id     = environ['GOOGLE_CLIENT_ID'],
    client_secret = environ['GOOGLE_CLIENT_SECRET'],
    scope         = ['email'],
    offline       = True,
    redirect_to   = 'page_authorized'
)
app.register_blueprint(blueprint, url_prefix='/login')
# -------------------- Levels stuff --------------------
with open('levels-config.json', 'r') as f: LEVELS_CONFIG = json.load(f)
with open('levels-data.json', 'r') as f:   LEVELS_DATA = json.load(f)
# -------------------- Pygal config --------------------
matplotlib.use('Agg')
plt.style.use('dark_background')
# Change the radius of the points
plt.rcParams['lines.markersize'] = 1
# Turn off the markings in x and y axis
plt.rcParams['xtick.bottom'] = False
plt.rcParams['xtick.labelbottom'] = False
plt.rcParams['ytick.left'] = False
plt.rcParams['ytick.labelleft'] = False
# Set figure DPI
plt.rcParams['figure.dpi'] = 200
# # Set background color to transparent
plt.rcParams['figure.facecolor'] = '#00000000'
# plt.rcParams['axes.facecolor']   = '#00000000'
# chart_style = pygal.style.NeonStyle
# chart_style.transition        = '0.3s ease-out'
# chart_style.background        = 'transparent'
# chart_style.foreground        = 'rgba(200, 200, 200, 1)'
# chart_style.foreground_strong = 'rgba(255, 255, 255, 1)'
# chart_style.colors            = ('#ff5995', '#b6e354', '#8cedff', '#9e6ffe', '#899ca1', '#f8f8f2', '#bf4646', '#f92672', '#82b414', '#fd971f', '#56c2d6', '#808384', '#8c54fe')










# -------------------------------------------------------------------------------------------------
# ---------------------------------------- DATABASE MODELS ----------------------------------------
# -------------------------------------------------------------------------------------------------
class User(db.Model):
    email    = db.Column(db.String(200), primary_key=True, nullable=False)
    username = db.Column(db.String(30), nullable=False)

class ForumPost(db.Model):
    post_id   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author    = db.Column(db.String(200),  nullable=False)
    title     = db.Column(db.String(200), nullable=False)
    content   = db.Column(db.Text(2000),  nullable=False)
    submitted = db.Column(db.DateTime,    nullable=False)

class ForumComment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author     = db.Column(db.String(200), nullable=False)
    post_id    = db.Column(db.Integer,     nullable=False)
    content    = db.Column(db.Text,        nullable=False)
    submitted  = db.Column(db.DateTime,    nullable=False)
    
class Score(db.Model):
    email   = db.Column(db.String(200), primary_key=True, nullable=False)
    level   = db.Column(db.String(20),  primary_key=True, nullable=False)
    score   = db.Column(db.Float,       nullable=False)
    answers = db.Column(db.String(200), nullable=False)










# -----------------------------------------------------------------------------------------------
# ---------------------------------------- API ENDPOINTS ----------------------------------------
# -----------------------------------------------------------------------------------------------
class EndpointSubmitComment(Resource):
    def post(self):
        if not google.authorized: return {'message': 'Not authorized. Please login'}, 401

        post_id = request.get_json().get('post_id')
        content = request.get_json().get('content')
        if not post_id or not content: return {'message': 'Invalid form data'}, 400
        comment = ForumComment(author=session['email'], post_id=post_id, content=content, submitted=datetime.now())
        db.session.add(comment)
        db.session.commit()
        return {'message': 'Comment submitted successfully', 'success': True}, 200
api.add_resource(EndpointSubmitComment, '/api/forum/post-comment')



class ChangeUsername(Resource):
    def post(self):
        if not google.authorized: return {'message': 'Not authorized. Please login'}, 401

        username = request.get_json().get('new-username')
        if not username: return {'message': 'Invalid form data'}, 400
        # Check if the username is the same lol
        if session['username'] == username: return {'message': 'You already have this username bruh'}, 400
        # Check if the username is already taken
        if User.query.filter_by(username=username).first(): return {'message': 'Username already taken'}, 400
        # Else, update the username
        user = db.session.get(User, session['email'])
        user.username = username
        db.session.commit()
        session['username'] = username
        return {'message': 'Username changed successfully', 'success': True}, 200
api.add_resource(ChangeUsername, '/api/user/change-username')



class SubmitBasicScore(Resource):
    def post(self):
        if not google.authorized: return {'message': 'Not authorized. Please login'}, 401

        req_json = request.get_json()
        level    = req_json['level']
        score    = req_json['score']
        answers  = req_json['answers']
        answers  = ', '.join(f'{k}:{v}' for k,v in answers.items())

        # Check if the user has already submitted a score for this level
        prev_score = db.session.query(Score).filter_by(email=session['email'], level=f'basic-{level}').first()
        # If the user hasnt ever submitted a score for this level
        if not prev_score:
            score = Score(email=session['email'], level=f'basic-{level}', score=score, answers=answers)
            db.session.add(score)
            db.session.commit()
        # If the new score is better than (or same as) the previous one
        elif score >= prev_score.score:
            prev_score.score   = score
            prev_score.answers = answers
            db.session.commit()
        return {'message': 'Score submitted successfully', 'success': True}, 200
api.add_resource(SubmitBasicScore, '/api/submit-basic-level')







# ------------------------------------------------------------------------------------------------
# ---------------------------------------- ROUTES / VIEWS ----------------------------------------
# ------------------------------------------------------------------------------------------------
@app.route('/')
def page_index():   
    username = session.get('username')
    email    = session.get('email')
    if google.authorized:
        url  = url_for('page_dashboard')
        text = 'Dashboard'
    else:
        url  = url_for('google.login')
        text = 'Signup / Login'

    return render_template('index.html', username=username, email=email, url=url, text=text)



@app.route('/pfp/<username>')
def page_pfp(username:str):
    return redirect(f'https://api.dicebear.com/9.x/pixel-art/svg?seed={username}')



@app.route('/dashboard/')
def page_dashboard():
    if not google.authorized:
        session['redirect'] = url_for('page_dashboard')
        return redirect(url_for('google.login'))
    
    # Basically we have levels like "basic-13" and "advanced-1". Basic levels should always come first and ofc numerical order should be maintained
    sort_levels = lambda x: (0 if x.split('-')[0]=='basic' else 1 , x.split('-')[1] )

    user   = db.session.get(User, session['email'])
    scores = db.session.query(Score).filter_by(email=session['email']).all()
    scores = sorted(scores, key=lambda x: sort_levels(x.level))
    return render_template('dashboard.html', user=user, scores=scores)



@app.route('/login/')
def page_login():
    if not google.authorized: return redirect(url_for('google.login'))
    return redirect(url_for('page_index'))



@app.route('/authorised/')
def page_authorized():
    if not google.authorized: return redirect(url_for('google.login'))
    
    # Get his info
    try: resp:Response = google.get('/oauth2/v1/userinfo')
    except TokenExpiredError: return redirect(url_for('google.login'))
    except: return 'Internal Server Error', 500
    # Check if the responses are valid
    if not resp.ok:                    return f'Failed to fetch user info, please <a href="{url_for("google.login")}">login again</a>'
    resp:dict = resp.json()
    if not resp.get('verified_email'): return 'Email not verified'
    if not resp.get('email'):          return 'Unable to fetch email'
    
    email = resp['email']
    user  = db.session.get(User, email)
    # If we have never seen this user before, add him to the database
    if not user:
        username = email.split('@')[0]
        user = User(email=resp['email'], username=resp['email'].split('@')[0])
        db.session.add(user)
        db.session.commit()
    else:
        username = user.username
    # Save the user's info in the session
    session['email']    = email
    session['username'] = username

    # If needs to redirected anywhere
    if 'redirect' in session:
        return redirect(session.pop('redirect'))
    return redirect(url_for('page_index'))




@app.route('/logout/')
def page_logout():
    if not google.authorized: return render_template('logout-fail.html')
    session.clear()
    return render_template('logout.html')



@app.route('/guides/')
def page_guides():
    ret = sorted(GUIDES.items())
    return render_template('guides/index.html', guides=ret)



@app.route('/guides/<int:guide_id>/')
def page_guide_id(guide_id:int):
    if not google.authorized:
        session['redirect'] = url_for('page_guide_id', guide_id=guide_id)
        return redirect(url_for('google.login'))
    
    if guide_id not in GUIDES: return 'Invalid guide ID', 400
    
    fn = GUIDES[guide_id]
    fp = f'guides/{fn}'
    return redirect(url_for('static', filename=fp))



@app.route('/forum/')
def page_forum():
    order  = ForumPost.submitted.desc()
    
    # Join the posts with their authors as to get the username
    clause = User.email == ForumPost.author
    cols   = [ForumPost.post_id, ForumPost.title, ForumPost.content, ForumPost.submitted, User.username]
    posts  = ForumPost.query.join(target=User, onclause=clause).add_columns(*cols).order_by(order).all()
    
    print(posts)
    return render_template('forum/index.html', posts=posts)



@app.route('/forum/submit', methods=['GET', 'POST'])
def page_forum_submit():
    if not google.authorized:
        session['redirect'] = url_for('page_forum_submit')
        return redirect(url_for('google.login'))
    
    if request.method == 'POST':
        title   = request.form.get('title')
        content = request.form.get('content')
        if not title or not content: return 'Invalid form data', 400
        post = ForumPost(author=session['email'], title=title, content=content, submitted=datetime.now())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('page_forum_post', post_id=post.post_id))
    
    return render_template('forum/submit.html')



@app.route('/forum/post/<int:post_id>/')
def page_forum_post(post_id:int):
    post      = db.session.get(ForumPost, post_id)
    post.username = db.session.get(User, post.author).username
    comments = ForumComment.query.filter_by(post_id=post_id)
    order    = ForumComment.submitted.desc()
    # Join comments with their authors as to get the username
    clause   = User.email == ForumComment.author
    cols     = [ForumComment.content, ForumComment.submitted, User.username]
    comments = comments.join(target=User, onclause=clause).add_columns(*cols).order_by(order).all()
    return render_template('forum/post.html', post=post, comments=comments)



@app.route('/playground/')
def page_playground():
    return render_template('playground/index.html')


@app.route('/playground/basic')
def page_playground_basic():
    return render_template('playground/basic/index.html')

@app.route('/playground/basic/level<int:level>/')
def page_playground_basic_level(level:int):
    if not google.authorized:
        session['redirect'] = url_for('page_playground_basic_level', level=level)
        return redirect(url_for('google.login'))
    return render_template(f'playground/basic/{level}.html')

@app.route('/playground/advanced/')
def page_playground_advanced():
    return render_template('playground/advanced/index.html')

@app.route('/playground/advanced/level<int:level>/')
def page_playground_advanced_level(level:int):
    if not google.authorized:
        session['redirect'] = url_for('page_playground_advanced_level', level=level)
        return redirect(url_for('google.login'))
    return render_template(f'playground/advanced/{level}.html')

@app.route('/playground/creative')
def page_playground_creative():
    return redirect('https://msr8.pythonanywhere.com')



@app.route('/plot/level<level>/')
def page_plot(level:int):
    if level not in LEVELS_CONFIG: return 'Invalid level', 400

    config    = LEVELS_CONFIG.get(level)
    data      = LEVELS_DATA.get(level)
    data['X'] = MinMaxScaler().fit_transform(data['X'])
    fix_hyperparameters = config['hyperparameters-fix']

    fig, ax = plt.subplots(1,1)
    ax: matplotlib.axes.Axes
    ax.set_title(f'Level {level}')
    x = data['X'][:, 0]
    y = data['X'][:, 1]
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.1, 1.1)

    if level == '1':
        prev_markersize = plt.rcParams['lines.markersize']
        plt.rcParams['lines.markersize'] = 10
    
    ax.scatter(x, y, c=data['Y'], cmap='rainbow')

    if level == '1': plt.rcParams['lines.markersize'] = prev_markersize

    # "show" represents whether to show the decision boundary or not
    if request.args.get('show'):
        # Get the hyperparameters
        inp_hyperparameters = {}
        
        for arg,dtype in config['hyperparameters-input']:
            if not request.args.get(arg): return f'{arg} not provided', 400
            inp_hyperparameters[arg] = request.args.get(arg)
            if   dtype == 'int':      inp_hyperparameters[arg] = int(inp_hyperparameters[arg])
            elif dtype == 'float':    inp_hyperparameters[arg] = float(inp_hyperparameters[arg])
        hyperparameters = fix_hyperparameters | inp_hyperparameters
        
        # Make the classifier
        classifier = config['classifier']
        if   classifier == 'knn':       clf = KNeighborsClassifier(**hyperparameters)
        elif classifier == 'svm':       clf = SVC(**hyperparameters)
        elif classifier == 'dtree':     clf = DecisionTreeClassifier(**hyperparameters)
        elif classifier == 'etrees':    clf = ExtraTreesClassifier(**hyperparameters)
        else: return 'Invalid classifier', 400

        # Fit the classifier
        clf.fit(data['X'], data['Y'])
        # Plot the decision boundary
        alpha = 0.2 if level not in ['6','7'] else 0.35 # Override for level 6 and 7 (cause hard to see decision boundaries)
        DecisionBoundaryDisplay.from_estimator(clf, data['X'], ax=ax, alpha=alpha, cmap='rainbow')
        # Calculate the log-loss (by testing the classifier on the same data)
        y_pred = clf.predict_proba(data['X'])
        loss   = log_loss(data['Y'], y_pred)
        loss   = round(loss, 4)
        ax.set_xlabel(f'Log-loss: {loss}')

        # Save the score
        answers    = ', '.join([f'{k}={v}' for k,v in inp_hyperparameters.items()])
        prev_score = db.session.query(Score).filter_by(email=session['email'], level=f'advanced-{level}').first()
        # If the user hasnt ever submitted a score for this level
        if not prev_score:
            score = Score(email=session['email'], level=f'advanced-{level}', score=loss, answers=answers)
            db.session.add(score)
            db.session.commit()
        # If the new score is better than (or same as) the previous one
        elif loss <= prev_score.score:
            print(answers)
            prev_score.score   = loss
            prev_score.answers = answers
            db.session.commit()

    # Save the output
    img = BytesIO()
    matplotlib.backends.backend_agg.FigureCanvasAgg(fig).print_png(img)
    # Make the response
    response = make_response(img.getvalue())
    response.headers['Content-Type'] = 'image/png'
    plt.close() # Avoid memory leaks
    return response






# ------------------------------------------------------------------------------------------------
# ---------------------------------------- INITIALISATION ----------------------------------------
# ------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001, threaded=True)