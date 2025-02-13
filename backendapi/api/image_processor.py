import numpy as np
from tensorflow.keras.preprocessing import image # type: ignore
from tensorflow.keras.applications.resnet50 import preprocess_input # type: ignore
import cv2
from PIL import Image
class ImageProcessor:
    def __init__(self, img_size=(224, 224)):
        self.IMG_SIZE = img_size
    @staticmethod
    def detect_and_crop_face(image):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        detected_faces = []
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2) 
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
   
    def preprocess_image(self, img_path):
            img = cv2.imread(img_path)
            if img is None:
                print("Error: Could not read image.")
                return None, None

            detected_faces = self.detect_and_crop_face(img)
            if not detected_faces:
                print("Error: No faces detected.")
                return None, None

            # Assuming we only want to process the first detected face
            face_img = detected_faces[0]
            face_img = cv2.resize(face_img, self.IMG_SIZE)
            img_array = image.img_to_array(face_img)
            return preprocess_input(np.expand_dims(img_array, axis=0)), face_img
