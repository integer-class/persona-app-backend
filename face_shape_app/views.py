from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .inference import predict_face_shape

@api_view(['POST'])
def classify_face_shape(request):
    if 'image' not in request.FILES:
        return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    image = request.FILES['image']
    prediction = predict_face_shape(image)
    
    return Response({'prediction': prediction}, status=status.HTTP_200_OK)