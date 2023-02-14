import base64
import os

import pandas as pd
from flask import Flask, request, jsonify
import numpy as np
import base64
import pickle
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import tensorflow as tf
import tensorflow_hub as hub
from api_call import getInfo, getUsage, getDescription, getPrecautions, getWarnings

pill_model = tf.keras.models.load_model("CV models/pills_efficientNetB0.h5")
pack_model = tf.keras.models.load_model("CV models/pack_efficientnet_model_1.h5",
                                        custom_objects={"KerasLayer": hub.KerasLayer})

pill_classes = ['Alaxan', 'Bactidol', 'Bioflu', 'Biogesic', 'DayZinc', 'Decolgen', 'Fish Oil', 'Kremil S', 'Medicol',
                'Neozep']
pack_classes = os.listdir(r"C:\Users\sarin\Documents\Science Fair Data\packaging_images")

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello world"


@app.route('/uploadPill', methods=['POST'])
def uploadPill():
    img_string = request.form.get("data")
    # print(type(img_string))
    img = base64.b64decode(img_string)
    # print(type(img))

    img = Image.open(BytesIO(img))

    pixels = np.asarray(img, dtype='float32')
    # print(pixels.shape)
    pixels = pixels / 255.
    # print(pixels.shape)
    pred = pill_model.predict(np.array([pixels, ]))
    pred = pred[0]

    class_name, prob = getClass(pill_classes, pred)
    print(class_name, prob)

    return jsonify({"class": class_name,
                    "probability": str(prob) + '%'})


@app.route('/uploadPack', methods=['POST'])
def uploadPack():
    img_string = request.form.get("data")
    # print(type(img_string))
    img = base64.b64decode(img_string)
    # print(type(img))

    img = Image.open(BytesIO(img))

    pixels = np.asarray(img, dtype='float32')
    # print(pixels.shape)
    pixels = pixels / 255.
    # print(pixels.shape)
    pred = pack_model.predict(np.array([pixels, ]))
    pred = pred[0]

    class_name, prob = getClass(pack_classes, pred)
    print(class_name, prob)

    return jsonify({"class": class_name,
                    "probability": str(prob) + '%'})

@app.route('/getInfo', methods=['POST'])
def getInfo():
    drug_brand = request.form.get("name")
    return jsonify({"info": getInfo(drug_brand)})

def getClass(class_names, pred_arr, conf_tresh=0):
    prob = max(pred_arr)
    if prob > conf_tresh:
        c = class_names[pred_arr.argmax()]
        return c, "{:.2f}".format(prob * 100)
    return "0", 0


if __name__ == '__main__':
    app.run(debug=True)
