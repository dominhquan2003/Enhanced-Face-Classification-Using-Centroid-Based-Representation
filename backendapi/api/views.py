from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Performer
from .serializers import PerformerSerializer
from .utils import detect_faces, get_distance_vector
import numpy as np
import cv2
import os
class PerfromerListCreate(generics.ListCreateAPIView):
    queryset = Performer.objects.all()
    serializer_class = PerformerSerializer
    
    def create(self, request, *args, **kwargs):
        original_image = request.FILES.get('original_image')
        name=request.data.get('name')
        if not original_image:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        np_image = np.frombuffer(original_image.read(), np.uint8)
        img = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
        detected_faces = detect_faces(img)
        save_folder = os.path.join('images', name)  # Tạo đường dẫn thư mục
        if not detected_faces:
            return Response({'error': 'No face detected'}, status=status.HTTP_400_BAD_REQUEST)

        for i, face_img in enumerate(detected_faces):
            distances = get_distance_vector(face_img)
            performer = Performer.objects.create(
                name=name,
                original_image=original_image,
            )
            face_crop_name = f"face_crop_{performer.pk}.jpg"  # Tên file lưu
            face_crop_path = os.path.join(save_folder, face_crop_name)  # Đường dẫn lưu
            cv2.imwrite(face_crop_path, face_img)  # Lưu hình ảnh khuôn mặt
        serializer = self.get_serializer(performer)
        print(distances, serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
class PerformerRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Performer.objects.all()
    serializer_class = PerformerSerializer
    lookup_field = 'pk'
 
    
