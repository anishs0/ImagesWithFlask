#!/usr/bin/env python
# coding: utf-8

# ### Image Classification With Flask

# In[1]:


from flask import Flask, request, jsonify, url_for, render_template
import uuid
import os
from tensorflow.keras.models import load_model
import numpy as np
from werkzeug.utils import secure_filename
from tensorflow.keras.applications import MobileNet
from PIL import Image, ImageFile
from io import BytesIO
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet import preprocess_input
from tensorflow.keras.applications.mobilenet import decode_predictions




ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
IMAGE_HEIGHT = 224
IMAGE_WIDTH = 224
IMAGE_CHANNELS = 3




def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS





app = Flask(__name__)
model = MobileNet(weights = 'imagenet', include_top = True)

@app.route('/')
def index():
    return render_template('imageML.html')

@app.route('/api/image', methods = ['POST'])

def upload_image():
    if 'image' not in request.files:
        return render_template('imageML.html', prediction = "You did not select an image")
    file = request.files['image']
    
    if file.filename =='':
        return render_template('imageML.html', prediction = 'You did not select an image')
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print("***"+filename)
        x = []
        ImageFile.LOAD_TRUNCATED_IMAGES = False
        img = Image.open(BytesIO(file.read()))
        img.load()
        img  = img.resize((IMAGE_WIDTH, IMAGE_HEIGHT), Image.ANTIALIAS)
        x  = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x  = preprocess_input(x)
        pred = model.predict(x)
        lst =  decode_predictions(pred, top=1)
        
        items = []
        for item in lst[0]:
            items.append({'name': item[1], 'prob': float(item[2])})
        
        response = {'pred': items}
        return render_template('imageML.html', prediction = 'This is most likely an image of {}'.format(response))
    else:
        return render_template('imageML.html', prediction = 'Invalid File extension')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
    





