from flask import Flask, request, render_template
from werkzeug import secure_filename
import os
import json
import schedule
from threading import Thread
from time import sleep
import time
import requests
import datetime
from Logger import Logger
import logging

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = set(['txt', 'json', 'png', 'jpg', 'jpeg', 'gif', 'zip'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

###################################################
# logger = Logger('amqp://admin:admin@10.42.0.239//')
# my_logger = logging.getLogger('test_logger')
# my_logger.setLevel(logging.DEBUG)

# # rabbitmq handler
# logHandler = Logger('amqp://admin:admin@10.42.0.239//')

# # adding rabbitmq handler
# my_logger.addHandler(logHandler)
################################################

c = 0
fg = 0


def send(filename, modelname, port, ip, uname, passw, cmd, inp_str_ip):
    print("Run Model")
    start_script = "start_"+modelname+".sh"
    cmd3 = "nohup sshpass -p " + passw + " ssh -o StrictHostKeyChecking=no " + ip + " -l " + uname + " bash "+ start_script + " &"
    print(cmd3)
    os.system(cmd3)
    
    # if modelname == "my_model":
    # url = "http://"+ip+":"+str(port)+"/v1/models/"+modelname+":predict"
    # else:
    #     url = "http://"+ip+":"+str(port)+"/v1/models/"+modelname+"/versions/1"+":predict"

    # cmd4 = "python process.py " + filename + " " +inp_str_ip + " " + url + " output.txt &"

    # os.system(cmd4)


def endFunction(modelname, starttag, endtag, repeat, passw, ip, uname):
    print("End Model")
    end_script = "stop_"+modelname+".sh"
    endcmd = "nohup sshpass -p " + passw + " ssh -o StrictHostKeyChecking=no " + ip + " -l " + uname + " bash "+ end_script + " &"
    os.system(endcmd)
    if repeat == "NO":
        schedule.clear(starttag)
        schedule.clear(endtag)


@app.route('/ScheduleService', methods=['GET', 'POST'])
def ScheduleService():
    print("Schedule")
    # my_logger.debug('Scheduler Service \t Start Scheduler')
    listOfDict = {}
    port = 45098
    global c
    global fg

    if fg == 0:
        fg = 1
        once()

    # data = request.get_json()
    data =request.data
    datadict=json.loads(data)
    print(type(datadict))
    print(datadict)
    data = datadict
    print("---------------------------",type(data))
    print(data)
    starttag = "tag"+str(c)
    c = c + 1
    endtag = "tag"+str(c)
    # print("---------------------@@@@@@@@@@@@@@@@@@@@@")
    if data['end'] != "NA" and data['repeat'] == "YES":
        schedule.every().day.at(data['start']).do(send, filename=data['filename'], modelname=data['modelname'], port=data['port'], ip=data['ip'],
													uname=data['uname'], passw=data['password'], cmd=data['start_command'], inp_str_ip=data['InputStreamIp']).tag(starttag)
        schedule.every().day.at(data['end']).do(endFunction, modelname=data['modelname'],
												starttag=starttag, endtag=endtag, repeat=data['repeat'], passw=data['password'], ip=data['ip'], uname=data['uname']).tag(endtag)
    elif data['end'] != "NA" and data['repeat'] == "NO":
	    schedule.every().day.at(data['start']).do(send, filename=data['filename'], modelname=data['modelname'], port=data['port'], ip=data['ip'], uname=data['uname'], passw=data['password'], cmd=data['start_command'],inp_str_ip=data['InputStreamIp']).tag(starttag)
	    schedule.every().day.at(data['end']).do(endFunction, modelname=data['modelname'],
											starttag=starttag, endtag=endtag, repeat=data['repeat'], passw=data['password'], ip=data['ip'], uname=data['uname']).tag(endtag)
    elif data['start'] == "NA" and data['end'] == "NA" and data['count'] == 1:
	    now = datetime.datetime.now()
	    start_hour = ""
	    start_minute = ""
	    end_hour = ""
	    end_minute = ""

	    if now.hour < 10:
		    start_hour = "0" + str(now.hour)
	    else:
		    start_hour = str(now.hour)
	    if now.minute + 1 < 10:
		    start_minute = "0" + str(now.minute+1)
	    else:
		    start_minute = str(now.minute+1)

	    start = start_hour + ":" + start_minute
	    end = now + datetime.timedelta(minutes=int(data['interval']+1))

	    if end.hour < 10:
		    end_hour = "0" + str(end.hour)
	    else:
		    end_hour = str(end.hour)
	    if end.minute < 10:
		    end_minute = "0" + str(end.minute)
	    else:
		    end_minute = str(end.minute)
	    end = end_hour + ":" + end_minute
	    print(start, end)
	    schedule.every().day.at(start).do(send, filename=data['filename'], modelname=data['modelname'], port=data['port'], ip=data['ip'], uname=data['uname'], passw=data['password'], cmd=data['start_command'],inp_str_ip=data['InputStreamIp']).tag(starttag)
	    schedule.every().day.at(end).do(endFunction,
										modelname=data['modelname'], starttag=starttag, endtag=endtag, repeat=data['repeat'], passw=data['password'], ip=data['ip'], uname=data['uname']).tag(endtag)
    else:
	    for j in range(data['count']):
		    if j == 0:
			    now = datetime.datetime.now()
		    start_hour = ""
		    start_minute = ""
		    end_hour = ""
		    end_minute = ""
		    if now.hour < 10:
			    start_hour = "0" + str(now.hour)
		    else:
			    start_hour = str(now.hour)
		    if now.minute + 1 < 10:
			    start_minute = "0" + str(now.minute+1)
		    else:
			    start_minute = str(now.minute+1)
		    start = start_hour + ":" + start_minute
		    end = now + datetime.timedelta(minutes=int(data['interval']+1))
		    if end.hour < 10:
			    end_hour = "0" + str(end.hour)
		    else:
			    end_hour = str(end.hour)
		    if end.minute < 10:
			    end_minute = "0" + str(end.minute)
		    else:
			    end_minute = str(end.minute)

		    end = end_hour + ":" + end_minute
		    print(start, end)
		    schedule.every().day.at(start).do(send, filename=data['filename'], modelname=data['modelname'], port=data['port'], ip=data['ip'], uname=data['uname'], passw=data['password'], cmd=data['start_command'],inp_str_ip=data['InputStreamIp']).tag(starttag)
		    schedule.every().day.at(end).do(endFunction,
											modelname=data['modelname'], starttag=starttag, endtag=endtag, repeat=data['repeat'], passw=data['password'], ip=data['ip'], uname=data['uname']).tag(endtag)
		    now = now + \
				datetime.timedelta(minutes=int(data['repeat_period']))
    c = c + 1
    # my_logger.debug('Scheduler Service \t Done Scheduler')
    return "From Schedule"


def once():
    thread = Thread(target=threaded_function)
    thread.start()


def threaded_function():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8000, debug=True,threaded=True)
