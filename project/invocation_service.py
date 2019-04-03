from flask import Flask,request, render_template
from werkzeug import secure_filename
import os,json,schedule
from threading import Thread
from time import sleep
import time
import datetime

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = set(['txt', 'json', 'png', 'jpg', 'jpeg', 'gif', 'zip'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

c = 0
fg = 0

def send(filename,modelname,port,ip,uname,passw,cmd,inp_str_ip) :
	print("ABCCCCCCC")
	cmd3 = "nohup sshpass -p " + passw + " ssh " + ip + " -l " + uname + " '" + cmd + "'" + " &"
	print(cmd3)
	os.system(cmd3)
    # tt = filename
    # if tt == "mnist":
    #     url = "http://"+ip+":"+str(port)+"/v1/models/"+modelname+":predict"
    # else:
    #     url = "http://"+ip+":"+str(port)+"/v1/models/"+modelname+"/versions/1"+":predict"
    # cmd4 = "python process.py " + filename + " " +inp_str_ip + " " + url + " output.txt &"
    # os.system(cmd4)
    
def endFunction(endCmd,starttag,endtag,repeat):
	os.system(endCmd)
	if repeat == "NO":
		schedule.clear(starttag)
		schedule.clear(endtag)

def runcmd(strcmd):
	os.system(strcmd)


def deployModelPhase(jsonfile,folderName):
    listOfDict = {}
    port = 45098
    global c
    global fg

    if fg == 0:
    	fg = 1
    	once()

    commands = '''
if [ -x "$(command -v docker)" ]; then
    echo "Update docker"
else
    echo "Install docker"
    sudo apt-get install curl
    sudo curl -sSL https://get.docker.com/ | sh
fi
    '''
    
    scheduletorun = []
    sched = {}

    with open(jsonfile) as json_file:
        listOfDict = json.load(json_file)

        cmd = "unzip " + folderName
        os.system(cmd)
        folderName = folderName[0:6]

        for i in listOfDict['ModelList'] : 
            ip = i['DeployIp']
            fname=i["Type"]
            uname = i['DeployUserName']
            password = i['DeployPassword']
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
            port = port + 1

            print("------------",modelfilename)
            dynamic1 = "unzip " + modelfilename
            dynamic2 = "echo " + password + " | sudo -S apt-get update"
            dynamic3 = "echo " + password +" | sudo -S docker pull tensorflow/serving"
            dynamic4 = "sudo docker stop $(echo " + password + " | sudo -S docker ps -aq)"
            dynamic5 = "echo " + password + " | sudo -S docker run -p 8500:8500 -p 8501:8501 --mount type=bind,source=/home/"+uname+"/"+modelpath+",target=/models/"+modelName+" -e MODEL_NAME="+modelName+" -t tensorflow/serving"
            dynamic6 = "nohup sshpass -p " + password + " ssh " +  ip +" -l " + uname + " 'docker stop $(docker ps -aq)'" + " &"
            commands = dynamic1 + "\n" + commands + "\n" + dynamic3 +"\n" + dynamic4 + "\n"

            f = open("script.sh","w+")
            f.write(commands)
            f.close()
            path = folderName + "/"
            cmd1 = "sshpass -p " + password + " scp " + "script.sh " + uname + "@" + ip + ":script.sh"
            cmd2 = "sshpass -p " + password + " scp " + path + modelfilename + " " + uname + "@" + ip + ":" + modelfilename
            cmd3 = "nohup sshpass -p " + password + " ssh " + ip + " -l " + uname + " bash script.sh &"

            os.system(cmd1)
            os.system(cmd2)
            os.system(cmd3)
            # t1 = threading.Thread(target=runcmd, args=(cmd3,)) 
            # t1.start();
            sched = {'InputStreamIp': stream_ip,'filename':fname,'modelname':modelName,'uname':uname,'password':password,'ip':ip,'port':8501,'start_command':dynamic5,'end_command':dynamic6,
            											'start':start,'end':end,'repeat':repeat,'count':count,'interval':interval,'repeat_period':repeat_period}
            scheduletorun.append(sched)

        # thread = Thread(target = threaded_function)
        # thread.start()
        for i in scheduletorun:
        	starttag = "tag"+str(c)
        	c = c + 1
        	endtag = "tag"+str(c)
        	if i['end']!="NA" and i['repeat']=="YES":
        		
        		schedule.every().day.at(i['start']).do(send,filename=i['filename'],modelname=i['modelname'],port=i['port'],ip=i['ip'],uname=i['uname'],passw=i['password'],cmd=i['start_command'],inp_str_ip=i['InputStreamIp']).tag(starttag)
        		schedule.every().day.at(i['end']).do(endFunction,endCmd=i['end_command'],starttag=starttag,endtag=endtag,repeat=i['repeat']).tag(endtag)
        	elif i['end']!="NA" and i['repeat']=="NO":
        		schedule.every().day.at(i['start']).do(send,filename=i['filename'],modelname=i['modelname'],port=i['port'],ip=i['ip'],uname=i['uname'],passw=i['password'],cmd=i['start_command'],inp_str_ip=i['InputStreamIp']).tag(starttag)
        		schedule.every().day.at(i['end']).do(endFunction,endCmd=i['end_command'],starttag=starttag,endtag=endtag,repeat=i['repeat']).tag(endtag)
        	elif i['start'] == "NA" and i['end'] == "NA" and i['count']==1:
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
        		end = now + datetime.timedelta(minutes = int(i['interval']+1))

        		if end.hour < 10:
        			end_hour = "0" + str(end.hour)
        		else:
        			end_hour = str(end.hour)
        		if end.minute < 10:
        			end_minute = "0" + str(end.minute)
        		else:
        			end_minute = str(end.minute)
        		end = end_hour + ":" + end_minute
        		print(start,end)
        		schedule.every().day.at(start).do(send,filename=i['filename'],modelname=i['modelname'],port=i['port'],ip=i['ip'],uname=i['uname'],passw=i['password'],cmd=i['start_command'],inp_str_ip=i['InputStreamIp']).tag(starttag)
        		schedule.every().day.at(end).do(endFunction,endCmd=i['end_command'],starttag=starttag,endtag=endtag,repeat=i['repeat']).tag(endtag)
        	else:
        		for j in range(count):
        			if j==0:
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
	        		end = now + datetime.timedelta(minutes = int(i['interval']+1))
	        		if end.hour < 10:
        				end_hour = "0" + str(end.hour)
        			else:
        				end_hour = str(end.hour)
        			if end.minute < 10:
        				end_minute = "0" + str(end.minute)
        			else:
        				end_minute = str(end.minute)

	        		end = end_hour + ":" + end_minute
	        		print(start,end)
        			schedule.every().day.at(start).do(send,filename=i['filename'],modelname=i['modelname'],port=i['port'],ip=i['ip'],uname=i['uname'],passw=i['password'],cmd=i['start_command'],inp_str_ip=i['InputStreamIp']).tag(starttag)
        			schedule.every().day.at(end).do(endFunction,endCmd=i['end_command'],starttag=starttag,endtag=endtag,repeat=i['repeat']).tag(endtag)
        			now=now+datetime.timedelta(minutes = int(i['repeat_period']))
        	c = c + 1
                    

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
        # model_name = request.form['model_name']
        # input_type = request.form['input_file_type']
        # interval = request.form['interval']

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
            # print(filename)

        # print(model_name)
        # print(input_type)
        # print(interval)
        deployModelPhase(filename,folder)
        return render_template('index.html')

    return "404"

# @app.route('/abc')
def once():
	thread = Thread(target = threaded_function)
	thread.start()

def threaded_function():
    # pass
    while True: 
        schedule.run_pending() 
        time.sleep(1)


if __name__ == '__main__':
    app.run(port=8879,debug=True)

