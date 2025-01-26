from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
urlpatterns = [
    path('facedetect/api/', include('api.urls')),
]
urlpatterns += static(settings.IMAGES_URL, document_root=settings.IMAGES_ROOT)
