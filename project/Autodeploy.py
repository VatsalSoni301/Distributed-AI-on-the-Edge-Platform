import os,json

def deployModelPhase(jsonfile):
	listOfDict = {}
	port = 45002

	# print(listOfDict)

	commands='''
sudo -S apt-get install python3.6
sudo -S apt-get python3-pip -y
pip3 install pandas --user
pip3 install tensorflow --user
pip3 install sklearn --user
echo "deb [arch=amd64] http://storage.googleapis.com/tensorflow-serving-apt stable tensorflow-model-server tensorflow-model-server-universal" | sudo tee /etc/apt/sources.list.d/tensorflow-serving.list && \
curl https://storage.googleapis.com/tensorflow-serving-apt/tensorflow-serving.release.pub.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install tensorflow-model-server -y
sudo apt-get upgrade tensorflow-model-server
pip3 install tensorflow-serving-api --user
	'''
	commands_docker = '''
if [ -x "$(command -v docker)" ]; then
    echo "Update docker"
else
    echo "Install docker"
    $ curl -fsSL https://get.docker.com -o get-docker.sh
	$ sh get-docker.sh
fi
sudo docker pull tensorflow/serving
	'''
	
	with open(jsonfile) as json_file:  
		listOfDict = json.load(json_file)

		for i in listOfDict['ModelList'] : 
			ip = i['DeployIp']
			uname = i['DeployUserName']
			password = i['DeployPassword']
			modelfilename = i['FileName']
			modelName = i['Modelname']
			modelpath = i["ModelPath"]

			port = port + 1

			dynamic1 = "unzip " + modelfilename
			dynamic2 = "echo " + password + " | sudo -S apt-get update"
			dynamic3 = "tensorflow_model_server --rest_api_port=" + str(port) + " --model_name=" + modelName + " --model_base_path=" + "/home/"+uname+"/"+modelpath
			
			dynamic3_docker = "sudo docker run -p 8500:8500 -p 8501:8501 --mount type=bind,source=/home/"+uname+"/"+modelpath+",target=/models/"+modelName+" -e MODEL_NAME="+modelName+" -t tensorflow/serving"
			# commands = dynamic1 +"\n" + dynamic2 + "\n" +commands + "\n" + dynamic3
			commands = dynamic1 +"\n" + dynamic2 + "\n" + dynamic3
			commands_docker = dynamic1 + "\n" + commands_docker + dynamic3_docker

			f = open("script.sh","w+")
			f.write(commands_docker)
			f.close()

			cmd1 = "sshpass -p " + password + " scp script.sh " + uname + "@" + ip + ":script.sh"
			cmd2 = "sshpass -p " + password + " scp " + modelfilename + " " + uname + "@" + ip + ":" + modelfilename
			cmd3 = "sshpass -p " + password + " ssh " + ip + " -l " + uname + " bash script.sh"

			os.system(cmd1)
			os.system(cmd2)
			os.system(cmd3)


def index():
	Jsonfile = "config.json"
	deployModelPhase(Jsonfile)

index()