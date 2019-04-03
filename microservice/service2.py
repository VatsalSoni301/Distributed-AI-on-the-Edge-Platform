from flask import Flask,request, render_template,jsonify

app = Flask(__name__)

@app.route('/getdetails')
def getdetails():
    return jsonify(
        username="vatsal",
        email="abc"
    )

if __name__ == '__main__':
    app.run(port=8878,debug=True)