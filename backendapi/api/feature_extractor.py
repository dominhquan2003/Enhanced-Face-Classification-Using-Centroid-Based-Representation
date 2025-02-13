import tensorflow as tf
from .image_processor import ImageProcessor
class FeatureExtractor:
    def __init__(self, base_model, pca_model,img_size=(224, 224)):
        self.feature_extractor = tf.keras.Model(inputs=base_model.input, outputs=base_model.get_layer('conv5_block3_out').output)
        self.pca_model = pca_model
        self.image_processor = ImageProcessor(img_size)
    def extract_feature_map(self, img_path):
        img_array, _ = self.image_processor.preprocess_image(img_path)
        feature_maps = self.feature_extractor.predict(img_array)
        feature_vector = feature_maps.reshape(1, -1)
        return self.pca_model.transform(feature_vector)
    
