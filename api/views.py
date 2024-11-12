from rest_framework import viewsets, status, generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import Face_shape, Hair_styles, Accessories, Recommendations, Recommendations_hair_styles, Recommendations_accessories, Feedback, History
from .serializers import Face_shapeSerializer, Hair_stylesSerializer, AccessoriesSerializer, RecommendationsSerializer, Recommendations_hair_stylesSerializer, Recommendations_accessoriesSerializer, FeedbackSerializer, HistorySerializer, UserSerializer

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key, 'user_id': user.pk, 'email': user.email
            }, status=status.HTTP_200_OK)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)
        
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
    
