import numpy as np
from .feature_extractor import FeatureExtractor
import glob
import os
class Predictor:
    def __init__(self, model_loader, feature_extractor,NUM_CENTROIDS_PER_PERSON):
        self.all_centroids = model_loader.all_centroids
        self.index_to_class = model_loader.index_to_class
        self.feature_extractor = feature_extractor
        self.NUM_CENTROIDS_PER_PERSON = NUM_CENTROIDS_PER_PERSON

    def find_closest_people(self, img_path, num_people=3):
        feature_vector_reduced = self.feature_extractor.extract_feature_map(img_path)
        distances = np.linalg.norm(self.all_centroids - feature_vector_reduced, axis=1)
        closest_centroids = np.argsort(distances)[:num_people * self.NUM_CENTROIDS_PER_PERSON]
        closest_people = set(closest_centroids // self.NUM_CENTROIDS_PER_PERSON)
        return [self.index_to_class.get(person, "Unknown") for person in list(closest_people)[:num_people]]

    @staticmethod
    def load_predicted_people_images(predicted_people, train_dir="models/data"):
        images = {}
        for person in predicted_people:
            img_paths = glob.glob(os.path.join(train_dir, person, "*.jpeg"))
            if img_paths:
                images[person] = img_paths[0]
        return images