from flask import Flask, request, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)

MODEL_PATH = 'keras_model.h5'
model = load_model(MODEL_PATH)

@app.route('/')
def home():
    return render_template('honey.html')

@app.route('/classify', methods=['POST'])
def classify_image():
    if 'image' not in request.files:
        return 'No file part'
    file = request.files['image']
    if file.filename == '':
        return 'No selected file'
    if file:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        pred = predict_honeybee(file_path)
        return render_template('result.html', prediction=pred)

def predict_honeybee(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x / 255.0
    preds = model.predict(x)
    if preds[0][0] > 0.5:
        return 'Infected'
    else:
        return 'Healthy'

if __name__ == '__main__':
    app.run(debug=True)
