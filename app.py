import base64

import pandas as pd
from flask import Flask, request, jsonify
import numpy as np
import base64
import pickle
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import tensorflow as tf

model = tf.keras.models.load_model("pills_efficientNetB0.h5")
print(model.summary())
app = Flask(__name__)


@app.route('/')
def index():
    return "Hello world"


@app.route('/upload', methods=['POST'])
def upload():
    img_string = request.form.get("data")
    print(type(img_string))
    img = base64.b64decode(img_string)
    print(type(img))

    img = Image.open(BytesIO(img))

    pixels = np.asarray(img, dtype='float32')
    print(pixels.shape)
    pixels = pixels/255.
    print(pixels.shape)
    pred = model.predict( np.array( [pixels,] ))
    print(pred)

    return jsonify({"test":"test"})



if __name__ == '__main__':
    app.run(debug=True)