from flask import Flask, render_template,jsonify
import requests,json
app = Flask(__name__)

@app.route('/')
def index():
	response = requests.get('http://127.0.0.1:8878/getdetails')
	res = response.json()
	print(res)
	return res['username']

if __name__ == '__main__':
    app.run(port=8876,debug=True)