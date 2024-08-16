# Number_Recognition
# Number Recognition Flask App

This is a Flask web application that uses a Convolutional Neural Network (CNN) model to predict numbers written in words from images. The model is trained to recognize numbers from 'one' to 'hundred'.

## Features

- Upload an image of a number written in words (e.g., "forty-two").
- The app preprocesses the image and uses a trained CNN model to predict the corresponding number (e.g., 42).
- Displays the prediction result as a JSON response.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```

2. **Set Up Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Add Your Trained Model**:
    - Place your trained model file `final_model_number_recognition_cnn.h5` in the root directory of the project.

## Usage

1. **Run the Flask App**:
    ```bash
    python app.py
    ```

2. **Access the Web Interface**:
    - Open your browser and go to `http://127.0.0.1:5000/`.
    - You can upload an image of a number written in words to get a prediction.

## API Endpoint

### POST `/`

**Description**: Upload an image to get the predicted number.

**Request**:
- Content-Type: `multipart/form-data`
- Body: A file input with the name `file` containing the image.

**Response**:
- Success: 
    ```json
    {
        "prediction": 42
    }
    ```
- Error:
    ```json
    {
        "error": "error message"
    }
    ```

## File Structure

