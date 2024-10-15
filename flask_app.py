from flask import Flask, request, jsonify, Response
import jsonpickle
import numpy as np
import os
import cv2

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def index(): 
    return "BU PROJECT MDT TESTING"

@app.route('/uploads', methods=['POST'])
def decode():
    r = request
    nparray = np.fromstring(r.data, np.uint8)

    # decode
    img = cv2.imdecode(nparray, cv2.IMREAD_COLOR)

    # send to client
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])}

    # encode using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="/application/json")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)

    
