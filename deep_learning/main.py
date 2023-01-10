import cv2
from flask import Flask, render_template, jsonify
from flask import flash, request, redirect, url_for
from keras.models import load_model
import matplotlib.pyplot as plt
from keras.utils import load_img, img_to_array
import numpy as np
import os
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

model = load_model('static/models/best_model.h5')

app = Flask(__name__)

UPLOAD_FOLDER = 'static/img/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():  # put application's code here
    return (render_template('page.html'))

@app.route('/', methods=['POST'])
def predicte(file_contents=None):
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        img = cv2.imread(f"C:/Users/tarek/Desktop/pythonProject/deep_learning/static/img/{filename}")
        plt.figure(figsize=(6,4))
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.tight_layout()
        img = cv2.resize(img, (150, 150))
        img = np.reshape(img, [-1, 150, 150, 3])
        result = model.predict(img)
        print(filename)
        print(result)
        if result == 0: return "Recyclable"
        elif result ==1: return "Organic"
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)






@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='img/' + filename), code=301)

if __name__ == '__main__':
    app.run()
