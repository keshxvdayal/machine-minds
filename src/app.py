from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_dance.contrib.google import make_google_blueprint, google
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError
from requests.models import Response
from dotenv import load_dotenv

from os import environ

load_dotenv()





# -------------------- Main App --------------------
app = Flask(__name__)
app.secret_key = 'super'
CORS(app)
api = Api(app)
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










# -------------------------------------------------------------------------------------------------
# ---------------------------------------- DATABASE MODELS ----------------------------------------
# -------------------------------------------------------------------------------------------------
class User(db.Model):
    email    = db.Column(db.String(200), primary_key=True, nullable=False)
    username = db.Column(db.String(30), nullable=False)










# ------------------------------------------------------------------------------------------------
# ---------------------------------------- ROUTES / VIEWS ----------------------------------------
# ------------------------------------------------------------------------------------------------
@app.route('/')
def page_index():
    if not google.authorized: return redirect(url_for('google.login'))
    
    username = session.get('username')
    email    = session.get('email')
    return render_template('index.html', username=username, email=email)



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
    user = User.query.get(resp['email'])
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






if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)