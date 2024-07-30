from flask import Flask, render_template, redirect, url_for, session, request, jsonify, make_response
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_dance.contrib.google import make_google_blueprint, google
import matplotlib.backends
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError
from requests.models import Response

from matplotlib import pyplot as plt
import matplotlib
from io import BytesIO

import pygal
import pygal.style

from dotenv import load_dotenv

from consts import *

from os import environ
from datetime import datetime

load_dotenv()





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
# -------------------- Pygal config --------------------
matplotlib.use('Agg')
plt.style.use('dark_background')
# Change the radius of the points
plt.rcParams['lines.markersize'] = 5
# Turn off the markings in x and y axis
plt.rcParams['xtick.bottom'] = False
plt.rcParams['xtick.labelbottom'] = False
plt.rcParams['ytick.left'] = False
plt.rcParams['ytick.labelleft'] = False
# Set background color to transparent
plt.rcParams['figure.facecolor'] = '#00000000'
plt.rcParams['axes.facecolor']   = '#00000000'
chart_style = pygal.style.NeonStyle
chart_style.transition        = '0.3s ease-out'
chart_style.background        = 'transparent'
chart_style.foreground        = 'rgba(200, 200, 200, 1)'
chart_style.foreground_strong = 'rgba(255, 255, 255, 1)'
chart_style.colors            = ('#ff5995', '#b6e354', '#8cedff', '#9e6ffe', '#899ca1', '#f8f8f2', '#bf4646', '#f92672', '#82b414', '#fd971f', '#56c2d6', '#808384', '#8c54fe')











# -------------------------------------------------------------------------------------------------
# ---------------------------------------- DATABASE MODELS ----------------------------------------
# -------------------------------------------------------------------------------------------------
class User(db.Model):
    email    = db.Column(db.String(200), primary_key=True, nullable=False)
    username = db.Column(db.String(30), nullable=False)

class ForumPost(db.Model):
    post_id   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author    = db.Column(db.String(30), db.ForeignKey('user.username'), nullable=False)
    title     = db.Column(db.String(200), nullable=False)
    content   = db.Column(db.Text(2000), nullable=False)
    submitted = db.Column(db.DateTime, nullable=False)

class ForumComment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author     = db.Column(db.String(30), db.ForeignKey('user.username'), nullable=False)
    post_id    = db.Column(db.Integer, db.ForeignKey('forum_post.post_id'), nullable=False)
    content    = db.Column(db.Text, nullable=False)
    submitted  = db.Column(db.DateTime, nullable=False)
    






# -----------------------------------------------------------------------------------------------
# ---------------------------------------- API ENDPOINTS ----------------------------------------
# -----------------------------------------------------------------------------------------------
class EndpointSubmitComment(Resource):
    def post(self):
        if not google.authorized: return {'message': 'Not authorized. Please login'}, 401

        post_id = request.get_json().get('post_id')
        content = request.get_json().get('content')
        if not post_id or not content: return {'message': 'Invalid form data'}, 400
        comment = ForumComment(author=session['username'], post_id=post_id, content=content, submitted=datetime.now())
        db.session.add(comment)
        db.session.commit()
        return {'message': 'Comment submitted successfully', 'success': True}, 200
api.add_resource(EndpointSubmitComment, '/api/forum/post-comment')





# ------------------------------------------------------------------------------------------------
# ---------------------------------------- ROUTES / VIEWS ----------------------------------------
# ------------------------------------------------------------------------------------------------
@app.route('/')
def page_index():
    # if not google.authorized: return redirect(url_for('google.login'))
    
    username = session.get('username')
    email    = session.get('email')
    return render_template('index.html', username=username, email=email)



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

    return redirect(url_for('page_index'))



@app.route('/logout/')
def page_logout():
    if not google.authorized: return render_template('logout-fail.html')
    session.clear()
    return render_template('logout.html')



@app.route('/guides/')
def page_guide():
    ret = sorted(GUIDES.items())
    return render_template('guides/index.html', guides=ret)



@app.route('/guides/<int:guide_id>/')
def page_guide_id(guide_id:int):
    if guide_id not in GUIDES: return 'Invalid guide ID', 400
    
    fn = GUIDES[guide_id]
    fp = f'guides/{fn}'
    return redirect(url_for('static', filename=fp))



@app.route('/forum/')
def page_forum():
    posts = ForumPost.query.all()
    return render_template('forum/index.html', posts=posts)



@app.route('/forum/submit', methods=['GET', 'POST'])
def page_forum_submit():
    if not google.authorized: return redirect(url_for('google.login'))
    
    if request.method == 'POST':
        title   = request.form.get('title')
        content = request.form.get('content')
        if not title or not content: return 'Invalid form data', 400
        post = ForumPost(author=session['username'], title=title, content=content, submitted=datetime.now())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('page_forum_post', post_id=post.post_id))
    
    return render_template('forum/submit.html')



@app.route('/forum/post/<int:post_id>/')
def page_forum_post(post_id:int):
    post = db.session.get(ForumPost, post_id)
    comments = ForumComment.query.filter_by(post_id=post_id).all()
    return render_template('forum/post.html', post=post, comments=comments)



@app.route('/playground/')
def page_playground():
    return render_template('playground.html')



@app.route('/plot/level<int:level>/')
def page_plot(level:int):
    if level == 1:
        # Create a simple scatter plot
        X = [1, 2, 3, 4, 5]
        Y = [2, 3, 4, 5, 6]
        fig, ax = plt.subplots(1,1)
        ax:matplotlib.axes.Axes
        ax.scatter(X, Y)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Level 1')
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
    app.run(debug=True)