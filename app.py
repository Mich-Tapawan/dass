from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from scripts.nlp import analyze_dass21_symptoms
from scripts.model import DASSModel

app = Flask(__name__)
CORS(app)

DASS_model = DASSModel()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/detect')
def detect():
    return render_template('nlp.html')

@app.route('/model')
def model():
    return render_template('info.html')

@app.route('/processText', methods=['POST'])
def processText():
    try:
        data = request.get_json()
        text = data.get('text')
        response = analyze_dass21_symptoms(text)
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/computeDASS', methods=['POST'])
def compute_dass():
    data = request.get_json()
    DASS_model.load_model()
    res = DASS_model.predict(data['dAnswers'],data['aAnswers'],data['sAnswers'])
    return res

if __name__ == "__main__":
    app.run(debug=True)