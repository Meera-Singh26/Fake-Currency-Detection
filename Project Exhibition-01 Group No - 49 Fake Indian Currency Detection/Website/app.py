from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import os
import tensorflow as tf
from PIL import Image, ImageFile
import numpy as np
# from arduino import Arduino
import requests

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Initialize Arduino object
# arduino = Arduino(port='COM14', baudrate=115200, timeout=1)

ESP32_IP = '192.168.170.40'

# Folder to save uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = tf.keras.models.load_model('model.h5')

# Ensure the uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Define route for the index page (redirect to login)
@app.route('/')
def index():
    return render_template('fakeCurrency.html')

# Define the login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.get_json()['username']
        password = request.get_json()['password']
        if username == 'admin' and password == 'password':
            return redirect(url_for('upload'))
        else:
            return "Invalid credentials. Please try again."
    return render_template("Login.html")

# Define route for the home page
@app.route('/home')
def home():
    return "Welcome to the Home Page!"

# Route to display the file upload form and handle the file upload
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' in request.files:
            # Handle file upload
            file = request.files['file']
            if file.filename == '':
                return 'No selected file', 400

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
        else:
            # Send request to ESP32 to capture image
            response = requests.get(f"http://{ESP32_IP}/capture")
            if response.status_code == 200:
                # Save the image
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_image.jpg')
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                return 'Failed to capture image from ESP32', 500

        # Ensure the image file is valid
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        try:
            img = Image.open(file_path)
            img.verify()  # Verify that it is, in fact, an image
            img = Image.open(file_path)  # Reopen the image file
            img = img.resize((224, 224))  # Resize to the input size expected by the model
            img = np.array(img) / 255.0  # Normalize the image
            img = np.expand_dims(img, axis=0)  # Add batch dimension
            
            # Make prediction
            prediction = model.predict(img)
            predicted_class = np.argmax(prediction, axis=1)[0]
            prediction_value = prediction[0][0].numpy() if hasattr(prediction[0][0], 'numpy') else prediction[0][0]
            
            return jsonify({
                'prediction': int(predicted_class),
                'chances': float(prediction_value),
                'image_url': url_for('uploaded_file', filename=os.path.basename(file_path))
            })
        except (IOError, SyntaxError) as e:
            return f"Invalid image file: {e}", 400
    elif request.method == 'GET':
        return render_template('Upload.html')
    else:
        return 'Method not allowed'

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Handle favicon.ico request
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')