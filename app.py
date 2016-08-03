from flask import Flask, render_template, request, url_for, redirect, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Sell, Ride, Textbook
from flask_oauth import OAuth

SECRET_KEY = 'this is a random key'
DEBUG = True
FACEBOOK_APP_ID = '1744249119148531'
FACEBOOK_APP_SECRET = 'daecd314a8e4a2c25c16cbe02ba07a2f'

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)

# DB
engine = create_engine('sqlite:///bulletin.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
db_session = DBSession()

@app.route('/', methods=['GET', 'POST'])
def landing():
    return render_template('index.html')

@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    return 'Logged in as id=%s name=%s redirect=%s' % \
        (me.data['id'], me.data['name'], request.args.get('next'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


@app.route('/dashboard/')
def dashboard():
    sell_items = db_session.query(Sell)
    ride_items = db_session.query(Ride)
    textbook_items = session.query(Textbook)
    return render_template('dashboard.html', sell_items = sell_items, ride_items=ride_items, textbook_items=textbook_items)

@app.route('/dashboard/sell/new', methods=['GET', 'POST'])
def sell_new():
    if request.method == 'POST':
        sell_item = Sell(item=request.form['item'], desc=request.form['desc'], price=request.form['price'])
        db_session.add(sell_item)
        db_session.commit()
        return redirect(url_for('dashboard'))
    else:
        return render_template('sell_new.html')

@app.route('/dashboard/ride/new', methods=['GET', 'POST'])
def ride_new():
    if request.method == 'POST':
        ride_item = Ride(origin=request.form['origin'], destination=request.form['destination'], price=request.form['price'])
        db_session.add(ride_item)
        db_session.commit()
        return redirect(url_for('dashboard'))
    else:
        return render_template('ride_new.html')

@app.route('/dashboard/textbook/new', methods=['GET', 'POST'])
def textbook_new():
    if request.method == 'POST':
        textbook_item = Textbook(lecture=request.form['lecture'], textbook=request.form['textbook'], price=request.form['price'])
        db_session.add(textbook_item)
        db_session.commit()
        return redirect(url_for('dashboard'))
    else:
        return render_template('textbook_new.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
