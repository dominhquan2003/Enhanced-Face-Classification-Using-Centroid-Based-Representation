import re
from django.db import models
import os


def sanitize_filename(filename):
    filename = re.sub(r'[^\w-]', '_', filename)  # Thay thế ký tự không hợp lệ
    filename = filename.replace(" ", "_")  # Thay thế khoảng trắng bằng dấu gạch dưới
    return filename

def get_upload_path(instance, filename):
    person_name = sanitize_filename(instance.name)  # Sử dụng name từ mô hình này
    extension = filename.split('.')[-1]
    return os.path.join(f'images/{person_name}/', f'{person_name}.{extension}') 

class Performer(models.Model):
    name = models.CharField(max_length=30)  
    status = models.BooleanField(default=True)  
    original_image = models.ImageField(upload_to=get_upload_path, null=True, blank=True)  
    crop_image = models.ImageField(upload_to=get_upload_path,null=True, blank=True)  
    crop_heatmap_image = models.ImageField(upload_to=get_upload_path,null=True, blank=True)  
    predictor_1 = models.ImageField(max_length=30, null=True, blank=True)
    predictor_2 = models.ImageField(max_length=30, null=True, blank=True)
    predictor_3 = models.ImageField(max_length=30, null=True, blank=True)
    heatmap_1 = models.ImageField(upload_to=get_upload_path,null=True, blank=True)  
    heatmap_2 = models.ImageField(upload_to=get_upload_path,null=True, blank=True)  
    heatmap_3 = models.ImageField(upload_to=get_upload_path,null=True, blank=True)  
    lg = models.ImageField(upload_to=get_upload_path,null=True, blank=True)  
    knn = models.ImageField(upload_to=get_upload_path,null=True, blank=True)  
    mlp = models.ImageField(upload_to=get_upload_path,null=True, blank=True)  
   
    def __str__(self):
        return self.name