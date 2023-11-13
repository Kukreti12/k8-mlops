import mlflow
import numpy as np
import gradio as gr
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import cv2

logged_model = 'runs:/d4ef959ac4994fc699a1250af655195e/best_model'

mlflow.set_tracking_uri("http://localhost:8080")
loaded_model = mlflow.pyfunc.load_model(logged_model)

def object_detection(path):
    image = load_img(path)
    image = np.array(image, dtype=np.uint8)
    image1 = load_img(path, target_size=(224, 224))
    image_arr_224 = img_to_array(image1) / 255.0
    h, w, d = image.shape
    test_arr = image_arr_224.reshape(1, 224, 224, 3)
    coords = loaded_model.predict(test_arr)
    denorm = np.array([w, w, h, h])
    coords = coords * denorm
    coords = coords.astype(np.int32)
    xmin, xmax, ymin, ymax = coords[0]
    pt1 = (xmin, ymin)
    pt2 = (xmax, ymax)
    cv2.rectangle(image, pt1, pt2, (0, 255, 0), 3)
    return image

def predict_image(img_path):
    result_image = object_detection(img_path)
    return result_image

iface = gr.Interface(
    fn=predict_image,
    inputs="image",
    outputs="image",
    live=True
)

iface.launch()
