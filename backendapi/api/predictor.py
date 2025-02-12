import numpy as np
from .feature_extractor import FeatureExtractor

class Predictor:
    def __init__(self, model_loader):
        self.rf_model = model_loader.rf_model
        self.knn_model = model_loader.knn_model
        self.mlp_model = model_loader.mlp_model
        self.knn_scaler = model_loader.knn_scaler
        self.knn_pca = model_loader.knn_pca
        self.mlp_scaler = model_loader.mlp_scaler
        self.feature_extractor = FeatureExtractor(model_loader)

    def predict_label(self, img_path):
        distance_vector = self.feature_extractor.compute_distance_vector(img_path)
        distance_vector_scaled_knn = self.knn_scaler.transform(distance_vector)
        distance_vector_pca_knn = self.knn_pca.transform(distance_vector_scaled_knn)
        knn_pred = self.knn_model.predict(distance_vector_pca_knn)
        distance_vector_scaled_mlp = self.mlp_scaler.transform(distance_vector)
        mlp_pred = np.argmax(self.mlp_model.predict(distance_vector_scaled_mlp), axis=1)
        rf_pred = self.rf_model.predict(distance_vector)
        return {
            "RandomForest": rf_pred[0],
            "KNN": knn_pred[0],
            "MLP": mlp_pred[0]
        }