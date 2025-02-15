import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
import os
import glob
import json
import joblib
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input

IMG_SIZE = (224, 224)
NUM_CENTROIDS_PER_PERSON = 16
NUM_PEOPLE = 488


def load_models_centroids(name_model:str = 'MobileNetV2', cluster:str = 'kmeans_k=16'):
    # =======================================  CNN models =======================================
    if name_model == 'EfficientNetB0':
        model = load_model('../models/EfficientNetb0.h5', compile=True)
        feature_layer_name = 'top_conv'
    elif name_model == 'MobileNetV2':
        model = load_model('../models/MobileNetV2.h5', compile=True)
        feature_layer_name = 'Conv_1'
    elif name_model == 'ResNet50':
        model = load_model('../models/ResNet50.h5' , compile=True)
        feature_layer_name = 'conv5_block3_out'
    feature_extractor = tf.keras.Model(inputs=model.input, outputs=model.get_layer(feature_layer_name).output)
    
    # =======================================  Cluster centroids ======================================= 
    pca_model = joblib.load(f'../models/{cluster}/pca_model.pkl')
    all_centroids = np.load(f'../models/{cluster}/all_centroids.npy')

    # =======================================  Class indices ======================================= 
    with open(f"../models/feature_maps/class_indices.json", "r") as f:
        index_to_class = {v: k for k, v in json.load(f).items()}

    return feature_extractor, feature_layer_name, pca_model, all_centroids, index_to_class


feature_extractor, feature_layer_name, pca_model, all_centroids, index_to_class = load_models_centroids(name_model='MobileNetV2', 
                                                                                                        cluster='kmeans_k=16')


def detect_and_crop_face(image_path):
    image = cv2.imread(image_path)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    if len(faces) == 0:
        print("No faces detected, using original image.")
        return image_path  
    
    x, y, w, h = faces[0] 
    face_crop = image[y:y+h, x:x+w]
    cropped_path = "cropped_face.jpg"
    cv2.imwrite(cropped_path, face_crop)
    return cropped_path

def preprocess_image(img_path):
    img_path = detect_and_crop_face(img_path) 
    img = image.load_img(img_path, target_size=IMG_SIZE)
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

def get_image_from_train(actor_name, train_dir="../models/data"):
    img_paths = glob.glob(os.path.join(train_dir, actor_name, "*.jpeg"))
    return img_paths[0] if img_paths else None

def compute_gradcam(model, img_array, layer_name='conv5_block3_out'):
    grad_model = tf.keras.Model(inputs=model.input, outputs=[model.get_layer(layer_name).output, model.output])
    with tf.GradientTape() as tape:
        conv_output, preds = grad_model(img_array)
        class_idx = np.clip(np.argmax(preds[0]), 0, preds.shape[1] - 1)
        loss = preds[:, class_idx]
    grads = tape.gradient(loss, conv_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    heatmap = np.maximum(tf.reduce_mean(tf.multiply(pooled_grads, conv_output), axis=-1)[0], 0)
    return heatmap / np.max(heatmap)

def overlay_heatmap(img, heatmap):
    heatmap = cv2.applyColorMap(cv2.resize((heatmap * 255).astype(np.uint8), (img.size[0], img.size[1])), cv2.COLORMAP_JET)
    return cv2.addWeighted(np.array(img), 0.5, heatmap, 0.5, 0)

def visualize_heatmaps(img_path):
    predicted_people = find_closest_people(img_path)
    input_array, input_img = preprocess_image(img_path)
    plt.figure(figsize=(6, 6))
    plt.imshow(overlay_heatmap(input_img, compute_gradcam(feature_extractor, input_array, layer_name=feature_layer_name)))
    plt.title("Input Image Heatmap")
    plt.axis("off")
    plt.show()
    
    for i, person in enumerate(predicted_people):
        img_path = get_image_from_train(person)
        if img_path:
            img_array, img = preprocess_image(img_path)
            plt.figure(figsize=(6, 6))
            plt.imshow(overlay_heatmap(img, compute_gradcam(feature_extractor, img_array, layer_name=feature_layer_name)))
            plt.title(f"Predicted Actor {i+1}: {person}")
            plt.axis("off")
            plt.show()

input_img_path =  ['D:/TailieuhocTDTu/ProjectInformationTechnology/reactnative_mobileapp/backendapi/models/data/Adam_Brody/Adam_Brody_355_235.jpeg']

for i in input_img_path:
    print(find_closest_people(i))