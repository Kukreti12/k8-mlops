import streamlit as st
import mlflow
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import cv2

# Set up MLflow tracking URI
mlflow.set_tracking_uri("http://localhost:8080")

# Define a function to load the MLflow model
@st.cache(allow_output_mutation=True)
def load_mlflow_model(logged_model):
    return mlflow.pyfunc.load_model(logged_model)

# Load the MLflow model (using the cached function)
logged_model = 'runs:/4338809bfeec443c9b6c248c2300c27c/best_model'
loaded_model = load_mlflow_model(logged_model)

# Define the object detection function
def object_detection(image):
    # Data preprocessing
    image_arr_224 = img_to_array(image) / 255.0
    h, w, d = image.shape
    test_arr = image_arr_224.reshape(1, 224, 224, 3)

    # Make predictions
    coords = loaded_model.predict(test_arr)

    # Denormalize the values
    denorm = np.array([w, w, h, h])
    coords = coords * denorm
    coords = coords.astype(np.int32)

    # Draw bounding box on the image
    xmin, xmax, ymin, ymax = coords[0]
    pt1 = (xmin, ymin)
    pt2 = (xmax, ymax)
    cv2.rectangle(image, pt1, pt2, (0, 255, 0), 3)

    return image, f"Bbox Coordinates: {pt1}, {pt2}"

# Streamlit app
st.title("Object Detection with Streamlit")

uploaded_file = st.file_uploader("Choose an image...", type="jpg")

if uploaded_file is not None:
    # Read and display the uploaded image
    image = load_img(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Perform object detection on the uploaded image
    result_image, bbox_coordinates = object_detection(img_to_array(image))
    
    # Display the result image
    st.image(result_image, caption="Result Image", use_column_width=True)

    # Display the bounding box coordinates
    st.write(bbox_coordinates)
