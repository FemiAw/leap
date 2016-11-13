"""

    Leap - Intelligent Recruitment
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import B
import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

# create application

app = Flask(__name__)

# Configuration

ALLOWED_EXTENSIONS = set(['pdf'])
app.config['UPLOAD_FOLDER'] = './uploads/'

# Local Data
X = {}


# Application



@app.route('/')
@app.route('/index')
def index():
    user = {'name': 'Konstantin'}
    return render_template('index.html', title='Leap', user=user)

@app.route('/question')
@app.route('/question/')
def question():
    return render_template('question.html', title='Question')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():

    #text = request.form['text']
    #print(text)

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            #text = request.form['text']
            #print(text)
            filename = secure_filename(file.filename)
            # create dict with file path and link to job posting
            X[os.path.join(app.config['UPLOAD_FOLDER'], filename)] = request.form['text']
            print(X)
            #print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            #redirect to homepage
            return redirect(url_for('index',
                                    filename=filename))
    return render_template('upload.html', title='Upload')
