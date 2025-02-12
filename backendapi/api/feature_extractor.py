import numpy as np
from .image_processor import ImageProcessor


class FeatureExtractor:
    def __init__(self, model_loader):
        self.feature_extractor = model_loader.feature_extractor
        self.pca_model = model_loader.pca_model
        self.all_centroids = model_loader.all_centroids

    def extract_feature_map(self, img_path):
        img_array = ImageProcessor.preprocess_image(img_path)
        feature_maps = self.feature_extractor.predict(img_array)
        feature_vector = feature_maps.reshape(1, -1)
        feature_vector_reduced = self.pca_model.transform(feature_vector)
        return feature_vector_reduced

    def compute_distance_vector(self, img_path):
        feature_vector_reduced = self.extract_feature_map(img_path)
        distances = np.linalg.norm(self.all_centroids - feature_vector_reduced, axis=1)
        return distances.reshape(1, -1)