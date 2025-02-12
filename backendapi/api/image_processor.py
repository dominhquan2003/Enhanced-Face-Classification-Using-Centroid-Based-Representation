import numpy as np
from tensorflow.keras.preprocessing import image # type: ignore
from tensorflow.keras.applications.resnet50 import preprocess_input # type: ignore
import cv2
class ImageProcessor:
    @staticmethod
    def detect_faces(image):
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

    @staticmethod
    def preprocess_image(img_path):
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        return img_array
