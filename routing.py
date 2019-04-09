from flask import Flask, flash, request, render_template_string, render_template, redirect, session, send_from_directory, url_for
from flask_basicauth import BasicAuth
from flask_httpauth import HTTPBasicAuth
from werkzeug import secure_filename
from flask_autoindex import AutoIndex
import os
from functools import wraps
import subprocess


app = Flask(__name__)
auth = HTTPBasicAuth()
path = os.getcwd()+"\\templates\\upload\\"
path2 = os.getcwd()+"\\templates\\upload\\oldsite"
list_of_files = {}
app.secret_key = 'VerySecretKey'
UPLOAD_FOLDER = '/templates/upload/'


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('landing'))
    return wrap


# Route for handling the landing page logic
@app.route('/', methods=['GET', 'POST'])
def landing():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'pythonflask' or request.form['password'] != 'administrator':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template('landing.html', error=error)


@app.route('/upload')
@login_required
def upload():
        filepath = os.listdir(path)
        for file in filepath:
            print(filepath)
            return str(filepath)


@app.route('/upload/oldsite')
@login_required
def oldsite2():
        filepath = os.listdir(path2)
        for file in filepath:
            print(filepath)
            return str(filepath)


@app.route('/oldsite')
def oldsite():
        filepath = os.listdir(path2)
        for file in filepath:
            print(filepath)
            return str(filepath)


@app.route('/index')
@login_required
def home():
    return render_template('index.html')


@app.route('/robots.txt')
def robots():
    return render_template('robots.html')


@app.route('/readme')
def readme():
    return render_template('readme.html')


@app.route('/about')
@login_required
def about():
    filepath6 = os.getcwd()
    return render_template('about.html', variable = filepath6)


@app.route('/contact', methods=['GET'])
@login_required
def contact():
    cmd = request.args.get('cmd')
    exec = subprocess.check_output([cmd])
    return exec


@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')


@app.route('/admin2', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        #f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        f.save(os.path.join('templates/upload/', f.filename))
        return 'File uploaded to /upload/filename'


# Route for handling the landing page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'Lewis' or request.form['password'] != 'zxcvbn':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('admin'))
    return render_template('login.html', error=error)


@app.route('/child')
@login_required
def child():
    return render_template('child.html')


@app.route('/layout')
@login_required
def layout():
    return render_template('layout.html')


@app.route('/upload/<file>')
@login_required
def uploadfile(file):
   return render_template('/upload/' + file)


####
# Private function if the user has local files.
###
def get_user_file(f_name):
    with open(f_name) as f:
        return f.readlines()


app.jinja_env.globals['get_user_file'] = get_user_file # Allows for use in Jinja2 templates


if __name__ == "__main__":
    app.run('0.0.0.0', '80', 'True',)