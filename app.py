from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/detect')
def detect():
    return render_template('list.html')

@app.route('/model')
def model():
    return render_template('info.html')


if __name__ == "__main__":
    app.run(debug=True)