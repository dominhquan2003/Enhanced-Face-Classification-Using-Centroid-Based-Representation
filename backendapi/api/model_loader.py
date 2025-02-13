import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model # type: ignore
import joblib
import glob
import json
class ModelLoader:
    def __init__(self):
        self.base_model = load_model('models/resnet50.h5')
        self.pca_model = joblib.load('models/kmeans_k=16/pca_model.pkl')
        self.kmeans_models = [joblib.load(path) for path in glob.glob('models/kmeans_k=16/kmeans_label_*.pkl')]
        self.all_centroids = np.concatenate([model.cluster_centers_ for model in self.kmeans_models], axis=0)
        with open('models/feature_maps/class_indices.json', "r") as f:
            self.index_to_class = {v: k for k, v in json.load(f).items()}
