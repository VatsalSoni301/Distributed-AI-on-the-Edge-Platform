from flask import Flask,request, render_template
from werkzeug import secure_filename
import os,json
from threading import Thread
from time import sleep
import time,requests
import datetime
from Logger import Logger
import logging

###################################################
# logger = Logger('amqp://admin:admin@10.42.0.239//')
# my_logger = logging.getLogger('test_logger')
# my_logger.setLevel(logging.DEBUG)

# # rabbitmq handler
# logHandler = Logger('amqp://admin:admin@10.42.0.239//')

# # adding rabbitmq handler
# my_logger.addHandler(logHandler)
################################################

app = Flask(__name__)

def caller_function(URL,sched) :
    print("Called")
    
    # print("Caller function called")
    # print(type(sched))
    print("Caller function called")
    r=requests.post(url=URL,data=json.dumps(sched))


@app.route('/deployService',methods=['POST'])
def deployModelPhase():
    # my_logger.debug('Deploy Service \t Started deploy')
    print("Deploy")
    # modelName = request.args.get('model')
    listOfDict = {}
    # jsonfile="config.json"
    folderName="./models/"
    commands = '''
if [ -x "$(command -v docker)" ]; then
    echo "Update docker"
else
    echo "Install docker"
    sudo apt-get install curl
    sudo curl -sSL https://get.docker.com/ | sh
fi
    '''
    # data = request.get_json()

    data =request.data
    datadict=json.loads(data)
    print(type(datadict))
    print(datadict)
    sched = {}
    i=datadict

    if i['Gateway'] == "NO":
        URL = "http://192.168.43.54:5003/get_service_ip/DeploymentService"
        response=requests.get(url=URL)
        loaddata = response.json()

        ip = loaddata['ip']
        port = loaddata['port']
        uname = loaddata['username']
        password = loaddata['password']
    else:
        ip = i['DeployIp']
        uname = i['DeployUserName']
        password = i['DeployPassword']
        port = i['port']

    fname=i["Type"]
    
    modelfilename = i['FileName']
    modelName = i['Modelname']
    modelpath = i["ModelPath"]
    start = i["StartTime"]
    end = i["EndTime"]
    count = i["Count"]
    repeat = i["Repeat"]
    stream_ip = i["InputStream"]
    interval = i["Interval"]
    repeat_period = i["Repeat_Period"]

    print("------------",modelfilename)
    dynamic1 = "unzip " + modelfilename
    dynamic2 = "echo " + password + " | sudo -S apt-get update"
    dynamic3 = "echo " + password +" | sudo -S docker pull tensorflow/serving"
    dynamic4 = "sudo docker stop $(echo " + password + " | sudo -S docker ps -aq)"
    dynamic5 = "echo " + password + " | sudo -S docker run --name=" + "\"" + modelName + "\"" + " -p " + str(port) + ":8501 --mount type=bind,source=/home/"+uname+"/"+modelpath+",target=/models/"+modelName+" -e MODEL_NAME="+modelName+" -t tensorflow/serving"
    # dynamic6 = "nohup sshpass -p " + password + " ssh " +  ip +" -l " + uname + " 'docker kill "+modelName + "'" + " &"
    # dynamic7 = "nohup sshpass -p " + password + " ssh " +  ip +" -l " + uname + " 'docker rm "+modelName + "'" + " &"
    dynamic6 = "echo " + password + " | " +"sudo -S docker kill " + modelName
    dynamic7 = "echo " + password + " | " +"sudo -S docker rm " + modelName

    commands = dynamic1 + "\n" + commands + "\n" + dynamic3 +"\n" + dynamic4 + "\n"

    scriptName = "script_" + modelName + ".sh"
    f = open(scriptName,"w+")
    f.write(commands)
    f.close()

    start_s = "start_"+modelName+".sh"
    f = open(start_s,"w+")
    f.write(dynamic5)
    f.close()

    dynamicX = dynamic6 + "\n" + dynamic7
    stop_s = "stop_"+modelName+".sh"
    f = open(stop_s,"w+")
    # f.write()
    f.write(dynamicX)
    f.close()

    path = folderName
    cmd1 = "sshpass -p " + password + " scp -o StrictHostKeyChecking=no " + scriptName + " " + uname + "@" + ip + ":" + scriptName
    cmd1_1 = "sshpass -p " + password + " scp -o StrictHostKeyChecking=no " + start_s + " " + uname + "@" + ip + ":" + start_s
    cmd1_2 = "sshpass -p " + password + " scp -o StrictHostKeyChecking=no " + stop_s + " " + uname + "@" + ip + ":" + stop_s
    cmd2 = "sshpass -p " + password + " scp -o StrictHostKeyChecking=no " + path + modelfilename + " " + uname + "@" + ip + ":" + modelfilename
    cmd3 = "nohup sshpass -p " + password + " ssh -o StrictHostKeyChecking=no " + ip + " -l " + uname + " bash "+ scriptName + " &"

    print("Before calling")

    # tempcmd = "sshpass -p dhawal@A1 ssh -o StrictHostKeyChecking=no dhawal@10.42.0.1"
    # os.system(tempcmd)
    os.system(cmd1)
    os.system(cmd1_1)
    os.system(cmd1_2)
    os.system(cmd2)
    os.system(cmd3)

    sched = {'InputStreamIp': stream_ip,'filename':fname,'modelname':modelName,'uname':uname,'password':password,'ip':ip,'port':8501,'start_command':dynamic5,'end_command':dynamic6,
                                                'start':start,'end':end,'repeat':repeat,'count':count,'interval':interval,'repeat_period':repeat_period}

            
    print("Call Schedule")
    # my_logger.debug('Deploy Service \t Call Schedule')

    # URL = "http://192.168.43.54:5003/get_service_ip/DeploymentService"
    # response=requests.get(url=URL)
    # sched_data = response.json()
    # s_ip = sched_data['ip']
    # s_port = sched_data['port']
    # url = "http://"+s_ip+":"+s_port+"/ScheduleService"

    url = "http://10.42.0.238:8891/ScheduleService"
    
    # thread = Thread(target=caller_function,args=(url,sched,))
    # thread.start()
    caller_function(url,sched)
    print("After Thread call")

    # r = json.dumps(sched)
    # url='http://127.0.0.1:8882/ScheduleService'
    # response = requests.post(url,data=r)
    # my_logger.debug('Deploy Service \t Done Deploy')
    return "From deploy"
        

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8000,debug=True,threaded=True)
