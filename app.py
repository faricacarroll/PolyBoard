from flask import Flask, render_template, request, url_for, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Sell

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
    items = session.query(Sell)
    return render_template('dashboard.html', items=items)

@app.route('/dashboard/sell/new', methods=['GET', 'POST'])
def sell_new():
    if request.method == 'POST':
        new_item = Sell(item=request.form['item'], desc=request.form['desc'], price=request.form['price'])
        session.add(new_item)
        session.commit()
        return redirect(url_for('dashboard'))
    else:
        return render_template('sell_new.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
