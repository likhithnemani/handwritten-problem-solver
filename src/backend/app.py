from flask import Flask
import base64
import json
from io import BytesIO
from flask.globals import request
from flask_cors import CORS
from predict import predict_solution

app = Flask(__name__)
CORS(app)

@app.route('/')
def root():
    return json.dumps({
        'success': True,
        'status': 200,
        'message': 'Hello World'
    })

@app.route('/predict', methods=['post'])
def predict():
    print(request)
    if request.form:
        operation = BytesIO(base64.urlsafe_b64decode(request.form['predict']))
        x = predict_solution(operation)
        return json.dumps({
            'success': True,
            'status': 200,
            'data': x
        })
    else:
        return json.dumps({
            'success': False,
            'status': 500,
            'message': 'No file received'
        })

if __name__ == '__main__':
    app.run(debug=True)