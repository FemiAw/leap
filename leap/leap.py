"""

    Leap - Intelligent Recruitment
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

import numpy, requests, PyPDF2, nltk, urllib2, os
from collections import Counter
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

# create application

app = Flask(__name__)

# Configuration

ALLOWED_EXTENSIONS = set(['pdf'])
app.config['UPLOAD_FOLDER'] = './uploads/'

# Local Data
X = []


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
            X.append(request.form['text'])
            X.append(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            #X[os.path.join(app.config['UPLOAD_FOLDER'], filename)] = request.form['text']
            print(X)
            #print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            #redirect to homepage
            return redirect(url_for('job',
                                    filename=filename))
    return render_template('upload.html', title='Upload')


@app.route('/job/')
def job():
    if len(X) > 0:
        content = extractJobDescript(X[0])
        cv = tokenizePdf(X[1])
        snapchat = JobProfile(X[0])
        match = snapchat.getMatchRate(cv)

    return render_template('job.html', content=content, match=match)

def extractJobDescript(url):
    r = urllib2.urlopen(url).read()
    soup = BeautifulSoup(r)
    letters = soup.find_all("div", {"id": "content"})
    lobby = []
    for element in letters:
        lobby.append(element.get_text())
    return lobby[0].strip().replace("\n", "")

def tokenizePdf(file_name):
    def load_raw(file_name):
        with open(file_name, 'rb') as f:
            pdfReader = PyPDF2.PdfFileReader(f)
            cv = []
            for i in range(0, pdfReader.getNumPages()):
                text = pdfReader.getPage(i).extractText()
                zn = nltk.word_tokenize(text)
                cv.append(zn)
            return [val for sublist in cv for val in sublist]

    try:
        return(load_raw(file_name))
    except UnicodeDecodeError:
        print("File cannot be loaded")

class JobProfile():

    def __init__(self, url):
        self.job_content = self.extractJobDescript(url)
        self.unigram = self.tokenator(self.job_content)
        self.word_counter = Counter(self.unigram)
        self.vocab = set(self.job_content)

    def extractJobDescript(self, url):
        r = urllib2.urlopen(url).read()
        soup = BeautifulSoup(r)
        letters = soup.find_all("div", {"id": "content"})
        lobby = []
        for element in letters:
            lobby.append(element.get_text())
        return lobby[0].strip().replace("\n", "")

    def tokenator(self, some_string):
        return nltk.word_tokenize(some_string)

    def getWordProb(self, key):
        return float(self.word_counter[key]) / float(len(self.unigram)*100)

    def getMatchRate(self, candidate_vocab):
        prob = 0
        for word in candidate_vocab:
            prob += self.getWordProb(word)
            print(prob)
        return prob
