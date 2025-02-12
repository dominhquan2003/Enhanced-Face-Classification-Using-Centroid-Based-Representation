import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image # type: ignore
from tensorflow.keras.applications.resnet50 import preprocess_input # type: ignore
import glob
import cv2
import os
import json

class GradCAMVisualizer:
    def __init__(self, model_loader):
        self.feature_extractor = model_loader.feature_extractor
        self.img_height, self.img_width = 224, 224
        with open("models/feature_maps/class_indices.json", "r") as f:
            class_indices = json.load(f)
            self.index_to_class = {v: k for k, v in class_indices.items()}

    def get_image_from_train(self, index, train_dir="models/data"):
        actor_name = self.index_to_class.get(index, None)
        if actor_name is None:
            return None
        actor_folder = os.path.join(train_dir, actor_name)
        img_paths = glob.glob(os.path.join(actor_folder, "*.jpeg"))
        return img_paths[0] if img_paths else None

    def load_and_preprocess_image(self, img_path):
        img = image.load_img(img_path, target_size=(self.img_height, self.img_width))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        return preprocess_input(img_array), img

    def compute_gradcam(self, model, img_array, layer_name='conv5_block3_out'):
        grad_model = tf.keras.Model([model.inputs], [model.get_layer(layer_name).output, model.output])
        with tf.GradientTape() as tape:
            conv_output, preds = grad_model(img_array)
            class_idx = np.clip(np.argmax(preds[0]), 0, preds.shape[1] - 1)
            loss = preds[:, class_idx]
        grads = tape.gradient(loss, conv_output)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        heatmap = tf.reduce_mean(tf.multiply(pooled_grads, conv_output), axis=-1)
        heatmap = np.maximum(heatmap[0], 0)
        heatmap /= np.max(heatmap)
        heatmap = np.power(heatmap, 2)
        return heatmap

    def overlay_heatmap(self, img, heatmap):
        heatmap = cv2.resize(heatmap, (img.size[0], img.size[1]))
        heatmap = np.uint8(255 * heatmap)
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
        superimposed_img = cv2.addWeighted(np.array(img), 0.5, heatmap, 0.5, 0)
        return superimposed_img

    def visualize_heatmaps(self, predictions, input_img_path):
        selected_images = [self.get_image_from_train(predictions[model]) for model in ['RandomForest', 'KNN', 'MLP']]
        selected_images = [img for img in selected_images if img is not None]
        input_array, input_img = self.load_and_preprocess_image(input_img_path)
        input_heatmap = self.compute_gradcam(self.feature_extractor, input_array)
        input_heatmap_img = self.overlay_heatmap(input_img, input_heatmap)
        heatmaps = [input_heatmap_img]
        for img_path in selected_images:
            img_array, img = self.load_and_preprocess_image(img_path)
            heatmap = self.compute_gradcam(self.feature_extractor, img_array)
            heatmap_img = self.overlay_heatmap(img, heatmap)
            heatmaps.append(heatmap_img)
        return input_heatmap_img, heatmaps