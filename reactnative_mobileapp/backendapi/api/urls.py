from django.urls import path
from . import views 
urlpatterns = [
      path("", views.PerformerListCreate.as_view(), name="facedetect-view-create"),
      path("<int:pk>/", views.PerformerRetrieveUpdateDestroy.as_view(), name="facedetect-view-retrieve"),
]