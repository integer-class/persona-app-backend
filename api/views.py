from rest_framework import viewsets
from .models import Face_shape, Hair_styles, Accessories, Recommendations, Recommendations_hair_styles, Recommendations_accessories, Feedback, History
from .serializers import Face_shapeSerializer, Hair_stylesSerializer, AccessoriesSerializer, RecommendationsSerializer, Recommendations_hair_stylesSerializer, Recommendations_accessoriesSerializer, FeedbackSerializer, HistorySerializer

class Face_shapeViewSet(viewsets.ModelViewSet):
    queryset = Face_shape.objects.all()
    serializer_class = Face_shapeSerializer
    
class Hair_stylesViewSet(viewsets.ModelViewSet):
    queryset = Hair_styles.objects.all()
    serializer_class = Hair_stylesSerializer
    
class AccessoriesViewSet(viewsets.ModelViewSet):
    queryset = Accessories.objects.all()
    serializer_class = AccessoriesSerializer
    
class RecommendationsViewSet(viewsets.ModelViewSet):
    queryset = Recommendations.objects.select_related('face_shape', 'hair_styles', 'accessories').all()
    serializer_class = RecommendationsSerializer
    
class Recommendations_hair_stylesViewSet(viewsets.ModelViewSet):
    queryset = Recommendations_hair_styles.objects.select_related('recommendations', 'hair_styles').all()
    serializer_class = Recommendations_hair_stylesSerializer
    
class Recommendations_accessoriesViewSet(viewsets.ModelViewSet):
    queryset = Recommendations_accessories.objects.select_related('recommendations', 'accessories').all()
    serializer_class = Recommendations_accessoriesSerializer
    
class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.select_related('recommendations').all()
    serializer_class = FeedbackSerializer
    
class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    
