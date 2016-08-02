from flask import Flask, render_template, request, url_for, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Sell, Ride, Textbook

app = Flask(__name__)

engine = create_engine('sqlite:///bulletin.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/', methods=['GET', 'POST'])
def landing():
    return render_template('index.html')

@app.route('/dashboard/')
def dashboard():
    sell_items = session.query(Sell)
    ride_items = session.query(Ride)
    textbook_items = session.query(Textbook)
    return render_template('dashboard.html', sell_items = sell_items, ride_items=ride_items, textbook_items=textbook_items)

@app.route('/dashboard/sell/new', methods=['GET', 'POST'])
def sell_new():
    if request.method == 'POST':
        sell_item = Sell(item=request.form['item'], desc=request.form['desc'], price=request.form['price'])
        session.add(sell_item)
        session.commit()
        return redirect(url_for('dashboard'))
    else:
        return render_template('sell_new.html')

@app.route('/dashboard/ride/new', methods=['GET', 'POST'])
def ride_new():
    if request.method == 'POST':
        ride_item = Ride(origin=request.form['origin'], destination=request.form['destination'], price=request.form['price'])
        session.add(ride_item)
        session.commit()
        return redirect(url_for('dashboard'))
    else:
        return render_template('ride_new.html')

@app.route('/dashboard/textbook/new', methods=['GET', 'POST'])
def textbook_new():
    if request.method == 'POST':
        textbook_item = Textbook(lecture=request.form['lecture'], textbook=request.form['textbook'], price=request.form['price'])
        session.add(textbook_item)
        session.commit()
        return redirect(url_for('dashboard'))
    else:
        return render_template('textbook_new.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
