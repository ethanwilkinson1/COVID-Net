import base64
import numpy as np
import io
from PIL import Image
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from flask import request
from flask import jsonify
from flask import Flask

app = Flask(__name__)

### This code was adapted from a tutorial series, provided 
### by the owners of DeepLizard. They should receive most of the credit.
### DeepLizard (2018) VGG16-Cats-and-Dogs (Version 1.0) [Source code]. 
### https://deeplizard.com/learn/video/XgzxH6G-ufA 

def get_model():
    global model
    model = load_model('model-1-ADAM-0.001.h5') 
    print("NETWORK LOADED!")

def preprocess_image(image, target_size):
    if image.mode != "L":
        image = image.convert("L")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image /= 255
    return image

print("LOADING NEURAL NETWORK...")
get_model()

@app.route("/covid-net", methods=["POST"])
def predict():
    message = request.get_json(force=True)
    encoded = message['image']
    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))
    processed_image = preprocess_image(image, target_size=(299, 299))

    prediction = model.predict(processed_image).tolist()

    response = {
        'prediction': {
            'normal': (1 - prediction[0][0]), 
            'covid': prediction[0][0]
        }
    }
    return jsonify(response)

