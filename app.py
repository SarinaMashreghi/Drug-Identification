import base64

import pandas as pd
from flask import Flask, request, jsonify
import numpy as np
import base64
import pickle
import matplotlib.pyplot as plt

# model = pickle.load(open('', 'rb'))
app = Flask(__name__)


@app.route('/')
def index():
    return "Hello world"


@app.route('/upload', methods=['POST'])
def upload():
    img_string = request.files['image']
    img = base64.b64decode(img_string)
    print('image received')
    plt.imshow(img)

    # if not pic:
    #     return 'No pic uploaded!', 400
    #
    # filename = secure_filename(pic.filename)
    # mimetype = pic.mimetype
    # if not filename or not mimetype:
    #     return 'Bad upload!', 400
    #
    # img = Img(img=pic.read(), name=filename, mimetype=mimetype)
    # db.session.add(img)
    # db.session.commit()
    #
    # return 'Img Uploaded!', 200

if __name__ == '__main__':
    app.run(debug=True)