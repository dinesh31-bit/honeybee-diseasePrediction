from flask import Flask, request, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)

# Path to the model
MODEL_PATH = 'honeybees.h5'

# Load the model
model = load_model(MODEL_PATH)

# Define the upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        pred, advice = predict_honeybee(file_path)
        return render_template('result2.html', prediction=pred, advice=advice)

def predict_honeybee(img_path):
    img = image.load_img(img_path, target_size=(128, 128))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x / 255.0
    preds = model.predict(x)
    # Check the shape of the predictions
    if preds.shape[1] != 3:
        return 'Error', 'Model output shape mismatch. Expected 3 classes.'
    # Extract the class with the highest probability
    pred_class = np.argmax(preds[0])
    if pred_class == 0:
        return 'healthy', 'No action needed.'
    elif pred_class == 1:
        return 'infected by DWV', 'To control DWV, implement varroa mite control strategies, use resistant bee stocks, and maintain strong, healthy colonies.'
    else:
        return 'infected', 'Further analysis required to identify the specific infection and provide appropriate treatment.'

if __name__ == '__main__':
    app.run(debug=True)
