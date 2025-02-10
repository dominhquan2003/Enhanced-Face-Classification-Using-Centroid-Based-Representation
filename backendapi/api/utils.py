import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from sklearn.decomposition import PCA
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
import joblib
import glob
import cv2
model = load_model('models/resnet50.h5')

feature_extractor = tf.keras.Model(inputs=model.input, outputs=model.get_layer('conv5_block3_out').output)

pca_model = joblib.load('models/kmeans_k=16/pca_model.pkl') 

kmeans_models_paths = glob.glob('models/kmeans_k=16/kmeans_label_*.pkl') 
all_centroids = []

for path in kmeans_models_paths:
    kmeans = joblib.load(path)
    all_centroids.append(kmeans.cluster_centers_)

all_centroids = np.concatenate(all_centroids, axis=0)

def detect_faces(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    detected_faces = []
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2) 
        side_length = max(w, h)  
        half_side = side_length // 2
        center_x = x + w // 2
        center_y = y + h // 2
    
        x1 = max(center_x - half_side, 0)
        y1 = max(center_y - half_side, 0)
        x2 = min(center_x + half_side, image.shape[1])
        y2 = min(center_y + half_side, image.shape[0])
        
        face_img = image[y1:y2, x1:x2]
        detected_faces.append(face_img)  

    return detected_faces  

def preprocess_image(img_array):
    img_array = cv2.resize(img_array, (224, 224))
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array

def get_distance_vector(img_path):
    img_array = preprocess_image(img_path)

    feature_maps = feature_extractor.predict(img_array)
    
    feature_vector = feature_maps.reshape(1, -1)

    feature_vector_reduced = pca_model.transform(feature_vector)

    distances = np.linalg.norm(all_centroids - feature_vector_reduced, axis=1)

    return distances.reshape(1, -1)
