from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

# Load the trained model
model = load_model('final_model_number_recognition_cnn.h5')

# Define a function to preprocess the image
def preprocess_image(img):
    img = img.convert('L')  # Convert image to grayscale
    img = img.resize((40, 160))  # Resize to the same size as training images
    img = np.array(img)
    img = img / 255.0  # Normalize the image
    img = np.expand_dims(img, axis=-1)  # Add the channel dimension
    img = np.expand_dims(img, axis=0)  # Add the batch dimension
    return img

@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            try:
                img = Image.open(io.BytesIO(file.read()))
                img = preprocess_image(img)

                # Make a prediction
                prediction = model.predict(img)
                predicted_class = np.argmax(prediction, axis=1)[0] + 1  # Adding 1 to match the labels

                return jsonify({'prediction': int(predicted_class)})
            except Exception as e:
                return jsonify({'error': str(e)})
        else:
            return jsonify({'error': 'No file uploaded'})

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
