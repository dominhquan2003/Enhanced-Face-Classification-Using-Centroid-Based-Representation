from django.urls import path
from . import views 
urlpatterns = [
      path("v1/", views.PerfromerListCreate.as_view(), name="facedetect-view-create"),
      path("v1/<int:pk>/", views.PerformerRetrieveUpdateDestroy.as_view(), name="facedetect-view-retrieve"),
]