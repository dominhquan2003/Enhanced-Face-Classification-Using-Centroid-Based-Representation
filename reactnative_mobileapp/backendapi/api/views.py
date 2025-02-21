from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import PerformerSerializer
import os
import numpy as np
import cv2
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Performer
from .serializers import PerformerSerializer
from .predict import detect_and_crop_face, visualize_and_predict  
import numpy as np
import cv2
import os
import re
def sanitize_filename(filename):
    filename = re.sub(r'[^\w-]', '_', filename)  
    filename = filename.replace(" ", "_")  
    return filename
def save_detected_faces(detected_faces, save_folder, name, kmeans_k):
    heatmap_filenames = [] 
    face_img = detected_faces[0]
    face_crop_name = f"face_crop_{sanitize_filename(name)}.jpg"
    face_crop_path = os.path.join(save_folder, face_crop_name)
    cv2.imwrite(face_crop_path, face_img)

    predicted_images, predicted_labels_images = visualize_and_predict(face_crop_path, kmeans_k)
    heatmap_input_path = os.path.join(save_folder, f"heatmap_input_{name}.jpg")
    input_prediction_path = os.path.join(save_folder, f"prediction_input_{name}.jpg")
    cv2.imwrite(heatmap_input_path, predicted_images[0][1])  
    cv2.imwrite(input_prediction_path, predicted_images[0][0])  
    for j, (img, heatmap) in enumerate(predicted_images[1:]): 
        heatmap_path = os.path.join(save_folder, f"heatmap_{j+1}_{sanitize_filename(name)}.jpg")
        prediction_path = os.path.join(save_folder, f"prediction_{j+1}_{sanitize_filename(name)}.jpg")

        cv2.imwrite(heatmap_path, heatmap) 
        cv2.imwrite(prediction_path, img)  
        heatmap_filenames.append((prediction_path, heatmap_path))
    predicted_label_paths = []
    model_names = ['lg', 'knn', 'mlp']  
    for idx, img in enumerate(predicted_labels_images):
        if idx < len(model_names): 
            label_img_name = f"{model_names[idx]}_image_{sanitize_filename(name)}.jpg"
            label_img_path = os.path.join(save_folder, label_img_name)
            cv2.imwrite(label_img_path, img)  
            predicted_label_paths.append(label_img_path)  
    return heatmap_filenames, heatmap_input_path,input_prediction_path,predicted_label_paths
    
class PerformerListCreate(generics.ListCreateAPIView):
    queryset = Performer.objects.all()
    serializer_class = PerformerSerializer
    def create(self, request, *args, **kwargs):
        original_image = request.FILES.get('original_image')
        name = request.data.get('name')
        kmeans_k = request.data.get('kmeans_k')  
        if not original_image:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        np_image = np.frombuffer(original_image.read(), np.uint8)
        img = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
        if img is None:
            return Response({'error': 'Invalid image format'}, status=status.HTTP_400_BAD_REQUEST)
        detected_faces = detect_and_crop_face(img)

        if not detected_faces:
            return Response({'error': 'No face detected'}, status=status.HTTP_400_BAD_REQUEST)

        save_folder = os.path.join('images', name)
        os.makedirs(save_folder, exist_ok=True)
        heatmap_filenames, heatmap_input_path,input_prediction_path, predicted_label_paths = save_detected_faces(detected_faces, save_folder, name, kmeans_k)
        performer = Performer.objects.create(
            name=name,
            original_image=original_image,
            crop_image = input_prediction_path,
            crop_heatmap_image= heatmap_input_path,
            heatmap_1=heatmap_filenames[0][1] if len(heatmap_filenames) > 0 else None,
            heatmap_2=heatmap_filenames[1][1] if len(heatmap_filenames) > 1 else None,
            heatmap_3=heatmap_filenames[2][1] if len(heatmap_filenames) > 2 else None,
            predictor_1=heatmap_filenames[0][0] if len(heatmap_filenames) > 0 else None,
            predictor_2=heatmap_filenames[1][0] if len(heatmap_filenames) > 1 else None,
            predictor_3=heatmap_filenames[2][0] if len(heatmap_filenames) > 2 else None,
            lg = predicted_label_paths[0] ,
            knn = predicted_label_paths[1] ,
            mlp = predicted_label_paths[2] ,
        )

        serializer = self.get_serializer(performer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
class PerformerRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
        queryset = Performer.objects.all()
        serializer_class = PerformerSerializer
        lookup_field = 'pk'
  
    
