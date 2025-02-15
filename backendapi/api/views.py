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
from .predict import detect_and_crop_face, visualize_heatmaps  
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
    for i, face_img in enumerate(detected_faces):
        face_crop_name = f"face_crop_{sanitize_filename(name)}_{i}.jpg"
        face_crop_path = os.path.join(save_folder, face_crop_name)
        cv2.imwrite(face_crop_path, face_img)

        predicted_images = visualize_heatmaps(face_crop_path, kmeans_k)
        heatmap_input_path = os.path.join(save_folder, f"heatmap_input_{name}_{i}.jpg")
        input_prediction_path = os.path.join(save_folder, f"prediction_input_{name}_{i}.jpg")

        # Lưu heatmap đầu vào
        cv2.imwrite(heatmap_input_path, predicted_images[0][1])  # Heatmap từ hình ảnh đầu vào
        cv2.imwrite(input_prediction_path, predicted_images[0][0])  # Hình ảnh predictor từ đầu vào

        
        # Lưu heatmaps và predictor cho các người dự đoán
        for j, (img, heatmap) in enumerate(predicted_images[1:]):  # Bỏ qua hình ảnh đầu vào
            heatmap_path = os.path.join(save_folder, f"heatmap_{j+1}_{sanitize_filename(name)}_{i}.jpg")
            prediction_path = os.path.join(save_folder, f"prediction_{j+1}_{sanitize_filename(name)}_{i}.jpg")

            cv2.imwrite(heatmap_path, heatmap)  # Lưu heatmap
            cv2.imwrite(prediction_path, img)  # Lưu hình ảnh predictor
            heatmap_filenames.append((prediction_path, heatmap_path))

    return heatmap_filenames, heatmap_input_path,input_prediction_path
    
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
        heatmap_filenames, heatmap_input_path,input_prediction_path = save_detected_faces(detected_faces, save_folder, name, kmeans_k)
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
        )

        serializer = self.get_serializer(performer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
class PerformerRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
        queryset = Performer.objects.all()
        serializer_class = PerformerSerializer
        lookup_field = 'pk'
  
    
