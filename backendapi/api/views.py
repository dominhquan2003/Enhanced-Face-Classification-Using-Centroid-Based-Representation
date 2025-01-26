from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Performer
from .serializers import PerformerSerializer

class PerfromerListCreate(generics.ListCreateAPIView):
    queryset = Performer.objects.all()
    serializer_class = PerformerSerializer

class PerformerRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Performer.objects.all()
    serializer_class = PerformerSerializer
    lookup_field = 'pk'
 
    
