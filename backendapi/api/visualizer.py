import numpy as np
import tensorflow as tf
import cv2
from .image_processor import ImageProcessor
class Visualizer:
    def __init__(self, feature_extractor):
        self.feature_extractor = feature_extractor

 
    def compute_gradcam(self,model, img_array, layer_name='conv5_block3_out'):
        model = self.feature_extractor.feature_extractor
        grad_model = tf.keras.Model(inputs=model.input, outputs=[model.get_layer(layer_name).output, model.output])        
        with tf.GradientTape() as tape:
            conv_output, preds = grad_model(img_array)
            class_idx = np.clip(np.argmax(preds[0]), 0, preds.shape[1] - 1)
            loss = preds[:, class_idx]
        grads = tape.gradient(loss, conv_output)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        heatmap = np.maximum(tf.reduce_mean(tf.multiply(pooled_grads, conv_output), axis=-1)[0], 0)
        return heatmap / np.max(heatmap)

  
    def overlay_heatmap(self,img, heatmap):
        heatmap = cv2.applyColorMap(cv2.resize((heatmap * 255).astype(np.uint8), (img.shape[1], img.shape[0])), cv2.COLORMAP_JET)
        return cv2.addWeighted(img, 0.5, heatmap, 0.5, 0)
    
    def visualize_heatmaps(self, img_path, predictor):
        image_processor = ImageProcessor()
        predicted_people = predictor.find_closest_people(img_path)
        predicted_images = predictor.load_predicted_people_images(predicted_people)
        
        input_array, input_img = image_processor.preprocess_image(img_path)
        input_heatmap_img = self.overlay_heatmap(input_img, self.compute_gradcam(self.feature_extractor, input_array))
        # Lưu heatmap đầu vào
        heatmaps = [input_heatmap_img]

        for i, (person, img_path) in enumerate(predicted_images.items()):
            img_array, img = image_processor.preprocess_image(img_path)
            heatmap = self.compute_gradcam(self.feature_extractor, img_array)
            heatmap_img = self.overlay_heatmap(img, heatmap)
            heatmaps.append(heatmap_img)

        return input_heatmap_img, heatmaps
