from flask import Flask,request, render_template
from werkzeug import secure_filename
import os,json
from threading import Thread
from time import sleep
import time
import datetime
import requests
import numpy
from Logger import Logger
import logging
import smtplib, ssl

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = set(['txt', 'json', 'png', 'jpg', 'jpeg', 'gif', 'zip'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

###################################################
logger = Logger('amqp://admin:admin@192.168.43.54//')
my_logger = logging.getLogger('test_logger')
my_logger.setLevel(logging.DEBUG)

# rabbitmq handler
logHandler = Logger('amqp://admin:admin@192.168.43.54//')

# adding rabbitmq handler
my_logger.addHandler(logHandler)
################################################

@app.route('/inference')
def inference():
    return render_template('inference.html')

@app.route('/inferenceService', methods=['GET', 'POST'])
def inferenceService():
    my_logger.debug('Inferencing Service \t Started inference')
    model_name = request.form['model_name']
    model_file = request.files['model_file']
    action_file = request.files['action_file']
    if model_file.filename == '':
        return "Test Data file not found"

    if action_file.filename == '':
        return "Action file not found"

    if model_file and allowed_file(model_file.filename):
        filename = secure_filename(model_file.filename)
        model_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    if action_file and allowed_file(action_file.filename):
        act_filename = secure_filename(action_file.filename)
        action_file.save(os.path.join(app.config['UPLOAD_FOLDER'], act_filename))

    result = ""
    with open(filename) as json_file:
        listOfDict = json.load(json_file)
        url = listOfDict['url']
        del listOfDict['url']
        response=requests.post(url,data=json.dumps(listOfDict))
        data = response.json()
        result = data
        # result = str(numpy.argmax(data['predictions'][0]))

    print("Mailed")
    print(result)

    # For notification service

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "johan.stark95@gmail.com"  # Enter your address
    receiver_email = "kansagara.darshan97@gmail.com"  # Enter receiver address
    password = "1friend1"
    message = """\
    Subject: Result

    Your predicted output is.""" + str(result)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

    return str(result)


@app.route('/user/<username>')
def user(username):
    return '<h2>Hello, %s </h2>' % username


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post Id is : %s ' %post_id


@app.route('/')
def index():
    my_logger.debug('RequestManager Service \t Started RMS')
    return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def caller_function(sched) :
    
    URL='http://127.0.0.1:8890/deployService'
    print("Caller function called")
    r=requests.post(url=URL,data=json.dumps(sched))

def deployHandler(jsonfile,folderName):
    sched = {}
    my_logger.debug('DeployHandler Service \t In deployHandler')
    with open(jsonfile) as json_file:
        listOfDict = json.load(json_file)
        print(listOfDict)
        print("list ",type(listOfDict))
        # mountpoint="abc"
        cmd = "unzip " + folderName
        os.system(cmd)
        # folderName = folderName[0:6]
        for i in listOfDict['ModelList']:
            print("single dict",i)
            print(type(i))
            # r = json.dumps(i)
            # print("rrrrrrrrrrrrrrrrr",r)
            # print("type r",type(r))
            thread = Thread(target=caller_function,args=(i,))
            thread.start()
            #Fetch the model detail from config file and stor in db
            


        # url='http://127.0.0.1:8882/ScheduleService'
        # response = requests.post(url,data=r)

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
        deployHandler(filename,folder)
        
        # print(response)
        print("Request Manager")
        # deployModelPhase(filename,folder)
        return render_template('index.html')

    return "404"

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=9000,debug=True,threaded=True)

