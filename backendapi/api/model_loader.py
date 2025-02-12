import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model # type: ignore
import joblib
import glob
class ModelLoader:
    def __init__(self):
        self.base_model = load_model('models/resnet50.h5')
        self.feature_extractor = tf.keras.Model(inputs=self.base_model.input, outputs=self.base_model.get_layer('conv5_block3_out').output)
        self.pca_model = joblib.load('models/kmeans_k=16/pca_model.pkl')
        self.kmeans_models_paths = glob.glob('models/kmeans_k=16/kmeans_label_*.pkl')
        self.all_centroids = np.concatenate([joblib.load(path).cluster_centers_ for path in self.kmeans_models_paths], axis=0)
        self.rf_model = joblib.load('models/random_forest/random_forest.pkl')
        self.knn_model = joblib.load('models/knn/knn.pkl')
        self.mlp_model = tf.keras.models.load_model("models/mlp/mlp.h5")
        self.knn_scaler = joblib.load("models/knn/knn_scaler.pkl")
        self.knn_pca = joblib.load("models/knn/knn_pca.pkl")
        self.mlp_scaler = joblib.load("models/mlp/mlp_scaler.pkl")