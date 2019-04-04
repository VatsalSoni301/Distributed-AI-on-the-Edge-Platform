from flask import Flask,request, render_template
import os,json
from threading import Thread
from time import sleep
import time
import datetime
import requests
import numpy
from Logger import Logger
import logging

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = set(['txt', 'json', 'png', 'jpg', 'jpeg', 'gif', 'zip'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

###################################################
logger = Logger('amqp://admin:admin@10.42.0.1//')
my_logger = logging.getLogger('test_logger')
my_logger.setLevel(logging.DEBUG)

# rabbitmq handler
logHandler = Logger('amqp://admin:admin@10.42.0.1//')

# adding rabbitmq handler
my_logger.addHandler(logHandler)
################################################

@app.route('/user/<username>')
def user(username):
    return '<h2>Hello, %s </h2>' % username


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post Id is : %s ' %post_id


@app.route('/')
def index():
	my_logger.debug('RequestManager Service \t Running successfully')
	return render_template('index.html')

@app.route('/inference')
def inference():
    return render_template('inference.html')

@app.route('/inferenceService', methods=['GET', 'POST'])
def inferenceService():
	model_name = request.form['model_name']
	model_file = request.files['model_file']
	action_file = request.files['action_file']
	print(model_name)
	if model_file.filename == '':
		return "Test Data file not found"

	if action_file.filename == '':
		return "Action file not found"

	if model_file and allowed_file(model_file.filename):
		filename = secure_filename(model_file.filename)
		model_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		folder = filename

	if action_file and allowed_file(action_file.filename):
		filename = secure_filename(action_file.filename)
		action_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

	# Fetch details from db 

	deployIp = "10.42.0.157"
	deployPort = 8501
	url = "http://"+deployIp+":"+str(deployPort)+"/v1/models/"+model_name+":predict"

	file1 = open(model_file.filename,"r+")  
	inputData = file1.read()
	inputData = list(inputData.split(", ")) 

	formatData = []
	for j in inputData:
		formatData.append(float(j))

	dict_data = {"signature_name":"predict_images","instances":[{"images":formatData}]}
	data1 = json.dumps(dict_data)
	response=requests.post(url,data=data1)
	# print(response)
	data = response.json()

	# Threading for notification service

	return str(numpy.argmax(data['predictions'][0]))

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

