import os
from flask import Flask, request, jsonify
import numpy as np
import base64
import pandas as pd
from io import BytesIO
from PIL import Image
import tensorflow as tf
import tensorflow_hub as hub
from api_call import *
from OCR import extract_text
from medical_NER import getEntities

pill_model = tf.keras.models.load_model("CV models/pills_efficientNetB0.h5")
pack_model = tf.keras.models.load_model("CV models/pack_efficientnet_model_1.h5",
                                        custom_objects={"KerasLayer": hub.KerasLayer})

pill_classes = ['Alaxan', 'Bactidol', 'Bioflu', 'Biogesic', 'DayZinc', 'Decolgen', 'Fish Oil', 'Kremil S', 'Medicol',
                'Neozep']
pack_classes = os.listdir(r"C:\Users\sarin\Documents\Science Fair Data\packaging_images")
med_cond_df = pd.read_csv("medical_condition_urls.csv")
med_conds = list(med_cond_df["medical_condition"])

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


@app.route('/extractText', methods=['POST'])
def extractText():
    img_string = request.form.get("data")
    img = base64.b64decode(img_string)

    img = Image.open(BytesIO(img))

    text = extract_text(img)
    # summary = bert_extractive(text, 5)

    med_ner = getEntities(text, "custom")
    products, quantity = getEntities(text, "roberta")
    conds = []
    cond_in_df = []
    for i, j in med_ner:
        if j == "MEDICALCONDITION":
            conds.append(i)
            if i in med_conds:
                cond_in_df.append(i)
        if j == "MEDICINE":
            products.append(i)

    cond_str = "Medical Conditions: \n"
    for i in conds:
        cond_str += i + "\n"

    final_api_summary = ''
    for p in products:
        final_api_summary = getSummary(p, 2)
        if final_api_summary != '':
            break

    if len(quantity) == 0 and final_api_summary != '':
        products_2, quantity = getEntities(text, "roberta")

    quan = ''
    if len(quantity) != 0:
        quan += "Quantity: " + quantity[0] + "\n\n"

    final_str = cond_str + quan + final_api_summary

    # get medical condition urls
    urls = []
    for i in cond_in_df:
        urls.append(med_cond_df.loc[med_cond_df["medical_condition"] == i]["url"])

    return jsonify({"sum_text": final_str,
                    "urls": urls})


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
