from flask import Flask,request,jsonify
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

@app.route('/logged',methods=['GET'])
def logged():
	logmsg = request.args.get('log')
	app.logger.debug(logmsg)
	return "Log Successfully"


if __name__ == '__main__':
	handler = RotatingFileHandler('LogFile.log', maxBytes=100000, backupCount=1)
	handler.setLevel(logging.INFO)
	app.logger.addHandler(handler)
	# logging.basicConfig(filename='error.log')
	app.run(port=8880,debug=True)