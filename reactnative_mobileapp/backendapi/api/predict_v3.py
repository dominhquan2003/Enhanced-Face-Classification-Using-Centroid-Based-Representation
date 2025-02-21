
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
import os
import glob
import json
import joblib
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing import image # type: ignore
from tensorflow.keras.applications.resnet50 import preprocess_input # type: ignore

IMG_SIZE = (224, 224)
NUM_CENTROIDS_PER_PERSON = 16
NUM_PEOPLE = 488

def load_models_centroids(name_model: str = 'MobileNetV2', cluster: str = 'kmeans_k=16'):
    if name_model == 'EfficientNetB0':
        model = load_model('../models/EfficientNetb0.h5', compile=True)
        feature_layer_name = 'top_conv'
    elif name_model == 'MobileNetV2':
        model = load_model('../models/MobileNetV2.h5', compile=True)
        feature_layer_name = 'Conv_1'
    elif name_model == 'ResNet50':
        model = load_model('../models/ResNet50.h5', compile=True)
        feature_layer_name = 'conv5_block3_out'
    feature_extractor = tf.keras.Model(inputs=model.input, outputs=model.get_layer(feature_layer_name).output)
    
    pca_model = joblib.load(f'../models/{cluster}/pca_model.pkl')
    all_centroids = np.load(f'../models/{cluster}/all_centroids.npy')
    
    with open(f"../feature_maps/{name_model}/class_indices.json", "r") as f:
        index_to_class = {v: k for k, v in json.load(f).items()}
    
    return feature_extractor, feature_layer_name, pca_model, all_centroids, index_to_class

feature_extractor, feature_layer_name, pca_model, all_centroids, index_to_class = load_models_centroids(name_model='MobileNetV2', 
                                                                                                        cluster='gmm_k=16')

def detect_and_crop_face(image_path):
    image = cv2.imread(image_path)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    if len(faces) == 0:
        print("No faces detected, using original image.")
        return image_path  
    
    x, y, w, h = faces[0] 
    return image[y:y+h, x:x+w]

def preprocess_image(img_path):
    img = detect_and_crop_face(img_path)
    img = cv2.resize(img, IMG_SIZE)
    img_array = image.img_to_array(img)
    return preprocess_input(np.expand_dims(img_array, axis=0)), img

def extract_feature_map(img_path):
    img_array, _ = preprocess_image(img_path)
    feature_maps = feature_extractor.predict(img_array)
    feature_vector = feature_maps.reshape(1, -1)
    return pca_model.transform(feature_vector)

def find_closest_people(img_path, num_people=3):
    feature_vector_reduced = extract_feature_map(img_path)
    distances = np.linalg.norm(all_centroids - feature_vector_reduced, axis=1)
    closest_centroids = np.argsort(distances)[:num_people * NUM_CENTROIDS_PER_PERSON]
    closest_people = set(closest_centroids // NUM_CENTROIDS_PER_PERSON)
    return [index_to_class.get(person, "Unknown") for person in list(closest_people)[:num_people]]


def get_image_from_train(actor_name, train_dir="../data/train"):
    img_paths = glob.glob(os.path.join(train_dir, actor_name, "*.jpeg"))
    return img_paths[0] if img_paths else None

def load_classification_model():
    logreg_model = joblib.load('../models/logreg/logreg.pkl')
    logreg_pca = joblib.load('../models/logreg/logreg_pca.pkl')
    logreg_scaler = joblib.load('../models/logreg/logreg_scaler.pkl')
    
    knn_model = joblib.load('../models/knn/knn.pkl')
    knn_pca = joblib.load("../models/knn/knn_pca.pkl")
    knn_scaler = joblib.load("../models/knn/knn_scaler.pkl")
    
    mlp_model = load_model("../models/mlp/mlp.h5")
    mlp_scaler = joblib.load("../models/mlp/mlp_scaler.pkl")
    
    return logreg_model, logreg_pca, logreg_scaler, knn_model, knn_pca, knn_scaler, mlp_model, mlp_scaler

def compute_distance_vector(img_path):
    feature_vector_reduced = extract_feature_map(img_path)
    return np.linalg.norm(all_centroids - feature_vector_reduced, axis=1).reshape(1, -1)

def predict_label(img_path):
    
    distance_vector = compute_distance_vector(img_path)
    logreg_model, logreg_pca, logreg_scaler, knn_model, knn_pca, knn_scaler, mlp_model, mlp_scaler = load_classification_model()
    
    knn_pred = knn_model.predict(knn_pca.transform(knn_scaler.transform(distance_vector)))[0]
    mlp_pred = np.argmax(mlp_model.predict(mlp_scaler.transform(distance_vector)), axis=1)[0]
    logreg_pred = logreg_model.predict(logreg_pca.transform(logreg_scaler.transform(distance_vector)))[0]
    
    predictions = {"LogisticRegression": logreg_pred, "KNN": knn_pred, "MLP": mlp_pred}
    
    predicted_images = {method: get_image_from_train(index_to_class.get(pred, "Unknown")) for method, pred in predictions.items()}
    
    return predicted_images



