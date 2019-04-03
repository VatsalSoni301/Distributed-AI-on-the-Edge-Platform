from flask import Flask,request, render_template
from werkzeug import secure_filename
import os,json,schedule
from threading import Thread
from time import sleep
import time
import datetime
import requests

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = set(['txt', 'json', 'png', 'jpg', 'jpeg', 'gif', 'zip'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/user/<username>')
def user(username):
    return '<h2>Hello, %s </h2>' % username


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post Id is : %s ' %post_id


@app.route('/')
def index():
    return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/deploy', methods=['GET', 'POST'])
def deploy():
    if request.method == 'GET':
        return "Bad Request"
    else:
        if 'model_file' not in request.files:
            #flash('No file part')
            return "No model_file file uploaded"

        if 'config_file' not in request.files:
            #flash('No file part')
            return "No config_file file uploaded"

        model_file = request.files['model_file']
        # model_file.save(secure_filename(model_file.filename))

        config_file = request.files['config_file']
        # config_file.save(secure_filename(model_file.filename))

        if model_file.filename == '':
            return "No model_file selected file"

        if config_file.filename == '':
            return "No config_file selected file"

        if model_file and allowed_file(model_file.filename):
            filename = secure_filename(model_file.filename)
            model_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            folder = filename

        if config_file and allowed_file(config_file.filename):
            filename = secure_filename(config_file.filename)
            config_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

 
        # response = requests.get('http://127.0.0.1:8880/logged?log=abcd')
        print("Call Deploy")
        url='http://127.0.0.1:8890/deployService?model=iris'#Fetch the model detail from config file and stor in db
        response = requests.get(url)
        # print(response)
        print("Request Manager")
        # deployModelPhase(filename,folder)
        return render_template('index.html')

    return "404"

if __name__ == '__main__':
    app.run(port=8879,debug=True,threaded=True)

