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

# Configuration
IMG_SIZE = (224, 224)
NUM_CENTROIDS_PER_PERSON = 16
NUM_PEOPLE = 488

# Load model and data
base_model = load_model('models/resnet50.h5')
feature_extractor = tf.keras.Model(inputs=base_model.input, outputs=base_model.get_layer('conv5_block3_out').output)

with open("models/feature_maps/class_indices.json", "r") as f:
    index_to_class = {v: k for k, v in json.load(f).items()}

def load_models(kmeans_version):
    pca_model = joblib.load(f'models/kmeans_k={kmeans_version}/pca_model.pkl')
    kmeans_models = [
        joblib.load(path) for path in glob.glob(f'models/kmeans_k={kmeans_version}/kmeans_label_*.pkl')
    ]
    all_centroids = np.concatenate([model.cluster_centers_ for model in kmeans_models], axis=0)
    
    return pca_model, kmeans_models, all_centroids

def detect_and_crop_face(image):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 3)
        detected_faces = []
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 1) 
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
   
def preprocess_image(img_path):
        img = cv2.imread(img_path)
        if img is None:
            print("Error: Could not read image.")
            return None, None

        detected_faces = detect_and_crop_face(img)
        if not detected_faces:
            print("Error: No faces detected.")
            return None, None

        # Assuming we only want to process the first detected face
        face_img = detected_faces[0]
        face_img = cv2.resize(face_img, IMG_SIZE)
        img_array = image.img_to_array(face_img)
        return preprocess_input(np.expand_dims(img_array, axis=0)), face_img

def extract_feature_map(img_path, pca_model):
    img_array, _ = preprocess_image(img_path)
    feature_maps = feature_extractor.predict(img_array)
    feature_vector = feature_maps.reshape(1, -1)
    return pca_model.transform(feature_vector)

def find_closest_people(img_path, num_people=3, kmeans_version=16, pca_model=None, all_centroids=None):
    feature_vector_reduced = extract_feature_map(img_path, pca_model)
    distances = np.linalg.norm(all_centroids - feature_vector_reduced, axis=1)
    closest_centroids = np.argsort(distances)[:num_people * kmeans_version]
    closest_people = set(closest_centroids // kmeans_version)
    return [index_to_class.get(person, "Unknown") for person in list(closest_people)[:num_people]]

def visualize_heatmaps(img_path, kmeans_version):
    # Tải mô hình tương ứng với kmeans_version
    pca_model, kmeans_models, all_centroids = load_models(kmeans_version)

    predicted_people = find_closest_people(img_path, num_people=3, kmeans_version=kmeans_version, pca_model=pca_model, all_centroids=all_centroids)
    predicted_images = load_predicted_people_images(predicted_people)
    
    input_array, input_img = preprocess_image(img_path)
    input_heatmap_img = overlay_heatmap(input_img, compute_gradcam(feature_extractor, input_array))
    
    # Lưu heatmap đầu vào
    heatmaps = [input_heatmap_img]
    for i, (person, img_path) in enumerate(predicted_images.items()):
        img_array, img = preprocess_image(img_path)
        heatmap = compute_gradcam(feature_extractor, img_array)
        heatmap_img = overlay_heatmap(img, heatmap)
        heatmaps.append(heatmap_img)

    return input_heatmap_img, heatmaps

def load_predicted_people_images(predicted_people, train_dir="models/data"):
    images = {}
    for person in predicted_people:
        img_paths = glob.glob(os.path.join(train_dir, person, "*.jpeg"))
        if img_paths:
            images[person] = img_paths[0]
    return images

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
    heatmap = cv2.applyColorMap(cv2.resize((heatmap * 255).astype(np.uint8), (img.shape[1], img.shape[0])), cv2.COLORMAP_JET)
    return cv2.addWeighted(img, 0.5, heatmap, 0.5, 0)


def visualize_heatmaps(img_path, kmeans_version):
    # Tải mô hình tương ứng với kmeans_version
    pca_model, kmeans_models, all_centroids = load_models(kmeans_version)

    predicted_people = find_closest_people(img_path, num_people=3, kmeans_version=kmeans_version, pca_model=pca_model, all_centroids=all_centroids)
    predicted_images = load_predicted_people_images(predicted_people)
    
    input_array, input_img = preprocess_image(img_path)
    input_heatmap_img = overlay_heatmap(input_img, compute_gradcam(feature_extractor, input_array))
    
    # Lưu heatmap đầu vào
    heatmaps = [input_heatmap_img]
    for i, (person, img_path) in enumerate(predicted_images.items()):
        img_array, img = preprocess_image(img_path)
        heatmap = compute_gradcam(feature_extractor, img_array)
        heatmap_img = overlay_heatmap(img, heatmap)
        heatmaps.append(heatmap_img)

    return input_heatmap_img, heatmaps