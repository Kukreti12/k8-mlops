from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import pandas as pd
import cv2
import os
import xml.etree.ElementTree as xet
from tensorflow.keras.applications import MobileNetV2, InceptionV3, InceptionResNetV2
from tensorflow.keras.layers import Dense, Dropout, Flatten, Input
from tensorflow.keras.models import Model
import tensorflow as tf
from tensorflow.keras.callbacks import TensorBoard
import numpy as np
import mlflow

df = pd.read_csv('labels.csv')
labels = df.iloc[:,1:].values

def getFilename(filename):
    filename_image = xet.parse(filename).getroot().find('filename').text
    filepath_image = os.path.join(r'C:\Users\adi3m\Downloads\Project_Files\1_Labeling\images',filename_image)
    return filepath_image


image_path = list(df['filepath'].apply(getFilename))

data = []
output = []
## Iterate  all the images
for ind in range(len(image_path)):
    image = image_path[ind]
    # Reads the image using open cv
    img_arr = cv2.imread(image)
    # Get the height width and number of channels
    h,w,d = img_arr.shape
    # prepprocesing
    # load image using keras function
    load_image = load_img(image,target_size=(224,224))
    # Convert the image to numpy array
    load_image_arr = img_to_array(load_image)
    ## Array is normalized by dividing each scale by 255 to scale them between 0 and 1
    norm_load_image_arr = load_image_arr/255.0 # normalization
    # normalization to labels
    xmin,xmax,ymin,ymax = labels[ind]
    nxmin,nxmax = xmin/w,xmax/w
    nymin,nymax = ymin/h,ymax/h
    label_norm = (nxmin,nxmax,nymin,nymax) # normalized output
    # -------------- append
    data.append(norm_load_image_arr)
    output.append(label_norm)
    
    
X = np.array(data,dtype=np.float32)
y = np.array(output,dtype=np.float32)

# Assuming X and y are defined and loaded with your data

x_train, x_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=0)

# Creating an InceptionResNetV2 model using pre-trained weights from ImageNet.
inception_resnet = InceptionResNetV2(weights="imagenet", include_top=False, input_tensor=Input(shape=(224, 224, 3)))
inception_resnet.trainable = False

# Head model
headmodel = inception_resnet.output
headmodel = Flatten()(headmodel)
headmodel = Dense(500, activation="relu")(headmodel)
headmodel = Dense(250, activation="relu")(headmodel)
headmodel = Dense(4, activation='sigmoid')(headmodel)

# Final model
model = Model(inputs=inception_resnet.input, outputs=headmodel)

# Compile model
model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4))

mlflow.set_tracking_uri("http://localhost:8080")
# Log hyperparameters
mlflow.log_param("batch_size", 10)
mlflow.log_param("epochs", 10)
mlflow.log_param("learning_rate", 1e-4)
mlflow.end_run()
# Log model architecture
with mlflow.start_run() as run:
    # Log custom hyperparameters or parameters
    mlflow.log_param("dense_units_1", 500)
    mlflow.log_param("dense_units_2", 250)
    mlflow.log_param("output_activation", "sigmoid")

    # Model training
    tfb = TensorBoard('object_detection')
    history = model.fit(x=x_train, y=y_train, batch_size=10, epochs=10,
                        validation_data=(x_test, y_test), callbacks=[tfb])

    # Log metrics
    mlflow.log_metric("train_loss", history.history['loss'][-1])
    mlflow.log_metric("val_loss", history.history['val_loss'][-1])

    # Save model
    # model.save('./models/object_detection.h5')
    mlflow.tensorflow.log_model(model, "best_model")
    