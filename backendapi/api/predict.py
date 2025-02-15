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


def load_models_centroids(name_model:str = 'MobileNetV2', cluster:str = 'kmeans_k=16'):
    # =======================================  CNN models =======================================
    if name_model == 'EfficientNetB0':
        model = load_model('models/EfficientNetb0.h5', compile=True)
        feature_layer_name = 'top_conv'
    elif name_model == 'MobileNetV2':
        model = load_model('models/MobileNetV2.h5', compile=True)
        feature_layer_name = 'Conv_1'
    elif name_model == 'ResNet50':
        model = load_model('models/ResNet50.h5' , compile=True)
        feature_layer_name = 'conv5_block3_out'
    feature_extractor = tf.keras.Model(inputs=model.input, outputs=model.get_layer(feature_layer_name).output)
    
    # =======================================  Cluster centroids ======================================= 
    pca_model = joblib.load(f'models/{cluster}/pca_model.pkl')
    all_centroids = np.load(f'models/{cluster}/all_centroids.npy')

    # =======================================  Class indices ======================================= 
    with open(f"models/feature_maps/class_indices.json", "r") as f:
        index_to_class = {v: k for k, v in json.load(f).items()}

    return feature_extractor, feature_layer_name, pca_model, all_centroids, index_to_class


# feature_extractor, feature_layer_name, pca_model, all_centroids, index_to_class = load_models_centroids(name_model='MobileNetV2', 
#                                                                                                         cluster='kmeans_k=16')


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
            raise ValueError(f"Error: Could not read image {img_path}.")
      detected_faces = detect_and_crop_face(img)
      if not detected_faces:
            print("Error: No faces detected.")
            return None, None
      img = detected_faces[0]
      img = cv2.resize(img, IMG_SIZE)
      img_array = image.img_to_array(img)
      return preprocess_input(np.expand_dims(img_array, axis=0)), img

def extract_feature_map(img_path, feature_extractor, pca_model):
    img_array, _ = preprocess_image(img_path)
    feature_maps = feature_extractor.predict(img_array)
    feature_vector = feature_maps.reshape(1, -1)
    return pca_model.transform(feature_vector)

def find_closest_people(img_path, num_people=3, feature_extractor=None, pca_model=None, all_centroids=None, index_to_class=None):
    feature_vector_reduced = extract_feature_map(img_path, feature_extractor, pca_model)
    distances = np.linalg.norm(all_centroids - feature_vector_reduced, axis=1)
    closest_centroids = np.argsort(distances)[:num_people * NUM_CENTROIDS_PER_PERSON]
    closest_people = set(closest_centroids // NUM_CENTROIDS_PER_PERSON)
    return [index_to_class.get(person, "Unknown") for person in list(closest_people)[:num_people]]

def get_image_from_train(actor_name, train_dir="models/data"):
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
    # Kiểm tra xem img có phải là mảng NumPy không
    if isinstance(img, np.ndarray):
        height, width = img.shape[:2]  # Lấy chiều cao và chiều rộng từ hình ảnh
    else:
        raise ValueError("img must be a numpy array")

    # Tạo heatmap với kích thước phù hợp
    heatmap_resized = cv2.resize((heatmap * 255).astype(np.uint8), (width, height))
    heatmap_colored = cv2.applyColorMap(heatmap_resized, cv2.COLORMAP_JET)
    
    return cv2.addWeighted(np.array(img), 0.5, heatmap_colored, 0.5, 0)

def visualize_heatmaps(img_path, cluster='kmeans_k=16'):
    
    feature_extractor, feature_layer_name, pca_model, all_centroids, index_to_class = load_models_centroids(
        name_model='MobileNetV2', cluster=cluster
    )
    predicted_people = find_closest_people(img_path, num_people=3, 
                                            feature_extractor=feature_extractor, 
                                            pca_model=pca_model, 
                                            all_centroids=all_centroids, 
                                            index_to_class=index_to_class)
    
    
    input_array, input_img = preprocess_image(img_path)
    input_heatmap = overlay_heatmap(input_img, compute_gradcam(feature_extractor, input_array, layer_name=feature_layer_name))
    
    predicted_images = [input_heatmap] 
    for person in predicted_people:
        img_path = get_image_from_train(person)
        if img_path:
            img_array, img = preprocess_image(img_path)
            person_heatmap = overlay_heatmap(img, compute_gradcam(feature_extractor, img_array, layer_name=feature_layer_name))
            predicted_images.append(person_heatmap)  
    
    return predicted_images
