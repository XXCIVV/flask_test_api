import time
from flask import Flask, request, jsonify, Response
import jsonpickle
import json
import numpy as np
import os
import cv2
import base64

app = Flask(__name__)


UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index(): 
    return "BU PROJECT MDT TESTING"

@app.route('/uploads', methods=['POST'])
def upload_image():

    # Log raw request data (useful for debugging)
    print(type(request.data))

    try:
        # Get the JSON data containing the Base64 encoded image
        data = request.get_json()
        if 'image_data' not in data:
            return jsonify({"success": False, "message": "No image data found in request"})
        
        # Decode the Base64 string back to binary data
        image_data = base64.b64decode(data['image_data'])

        # Convert the binary data to a NumPy array
        np_arr = np.frombuffer(image_data, np.uint8)

        # Decode the NumPy to image
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if image is None:
            return jsonify({"success": False, "message": "Failed to decode image. The data may be corrupted or in an unsupported format."})
        
        # Save the image to local
        image_filename = os.path.join(UPLOAD_FOLDER, f'received_image_{int(time.time())}.png')
        cv2.imwrite(image_filename, image)
        
        # Encode the response using jsonpickle 
        response = {
            "success": True,
            "message": "Image received and processed",
            "image_shape": image.shape,
            "filename": image_filename,
        }

        # Return the response as a JSON-encoded string
        return jsonpickle.encode(response)
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)

    
