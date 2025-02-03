from django.urls import path
from . import views 
urlpatterns = [
      path("/", views.PerfromerListCreate.as_view(), name="facedetect-view-create"),
      path("/<int:pk>/", views.PerformerRetrieveUpdateDestroy.as_view(), name="facedetect-view-retrieve"),
]