from flask import Flask, jsonify, make_response
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
        x,t = predict_solution(operation)
        if type(x) == list:
            x = ",".join(str(i) for i in x)
        return make_response(jsonify({
            "solution": x,
            "equation": t
        }),200)
    else:
        return make_response(jsonify({
            'message': 'No file received'
        }),500)

if __name__ == '__main__':
    app.run(debug=True,port=6003,host="0.0.0.0")
