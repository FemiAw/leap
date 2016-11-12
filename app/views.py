from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'name': 'Konstantin'}
    return render_template('index.html', title='Leap', user=user)
