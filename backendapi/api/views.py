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
from .model_loader import ModelLoader
from .predictor import Predictor
from .image_processor import ImageProcessor
from .visualizer import Visualizer
from .feature_extractor import FeatureExtractor
import numpy as np
import cv2
import os
import re
def sanitize_filename(filename):
    filename = re.sub(r'[^\w-]', '_', filename)  
    filename = filename.replace(" ", "_")  
    return filename

class PerformerListCreate(generics.ListCreateAPIView):
    queryset = Performer.objects.all()
    serializer_class = PerformerSerializer
    model_loader = ModelLoader()
    feature_extractor = FeatureExtractor(model_loader.base_model,model_loader.pca_model)
    predictor = Predictor(model_loader, feature_extractor,16)
    visualizer = Visualizer(feature_extractor)
    def create(self, request, *args, **kwargs):
        original_image = request.FILES.get('original_image')
        name = request.data.get('name')
        if not original_image:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        np_image = np.frombuffer(original_image.read(), np.uint8)
        img = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
        detected_faces = ImageProcessor.detect_and_crop_face(img)

        if not detected_faces:
            return Response({'error': 'No face detected'}, status=status.HTTP_400_BAD_REQUEST)

        save_folder = os.path.join('images', name)
        os.makedirs(save_folder, exist_ok=True)
        heatmap_filenames = []

        for i, face_img in enumerate(detected_faces):
            face_crop_name = f"face_crop_{sanitize_filename(name)}_{i}.jpg"
            face_crop_path = os.path.join(save_folder, face_crop_name)
            cv2.imwrite(face_crop_path, face_img)
            input_heatmap_img, heatmaps = self.visualizer.visualize_heatmaps(face_crop_path, self.predictor)
            heatmap_input_path = os.path.join(save_folder, f"heatmap_input_{name}_{i}.jpg")
            cv2.imwrite(heatmap_input_path, input_heatmap_img)
            heatmap_filenames.append(heatmap_input_path)

            for j, heatmap in enumerate(heatmaps):
                heatmap_path =  os.path.join(save_folder, f"heatmap_{j+1}_{sanitize_filename(name)}_{i}.jpg")
                cv2.imwrite(heatmap_path, heatmap)
                heatmap_filenames.append(heatmap_path)

        performer = Performer.objects.create(
            name=name,
            original_image=original_image,
            detected_image=face_crop_name,
            heatmap_1=heatmap_filenames[0] if len(heatmap_filenames) > 0 else None,
            heatmap_2=heatmap_filenames[1] if len(heatmap_filenames) > 1 else None,
            heatmap_3=heatmap_filenames[2] if len(heatmap_filenames) > 2 else None,
        )

        serializer = self.get_serializer(performer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
class PerformerRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
        queryset = Performer.objects.all()
        serializer_class = PerformerSerializer
        lookup_field = 'pk'
  
    
