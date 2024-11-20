from rest_framework import viewsets, status, generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from .inference import predict_face_shape
from .models import FaceShape, HairStyle, Accessory, Recommendation, Feedback, History
from .serializers import UserSerializer, FaceShapeSerializer, HairStyleSerializer, AccessorySerializer, RecommendationsSerializer, FeedbackSerializer, HistorySerializer

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
        

class FaceShapeViewSet(viewsets.ModelViewSet):
    queryset = FaceShape.objects.all()
    serializer_class = FaceShapeSerializer

class HairStyleViewSet(viewsets.ModelViewSet):
    queryset = HairStyle.objects.all()
    serializer_class = HairStyleSerializer

class AccessoryViewSet(viewsets.ModelViewSet):
    queryset = Accessory.objects.all()
    serializer_class = AccessorySerializer
    
class RecommendationsViewSet(viewsets.ModelViewSet):
    queryset = (
        Recommendation.objects
        .select_related('face_shape')
        .prefetch_related(
            'hair_styles',
            'accessories'
        )
        .all()
    )
    serializer_class = RecommendationsSerializer

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.select_related('recommendations').all()
    serializer_class = FeedbackSerializer

class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

@api_view(['POST'])
@parser_classes([MultiPartParser])
def predict(request):
    if 'image' not in request.FILES:
        return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    if 'gender' not in request.data:
        return Response({'error': 'No gender provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    image = request.FILES['image']
    gender = request.data['gender']
    
    predicted_face_shape = predict_face_shape(image)  # Your prediction function

    try:
        face_shape = FaceShape.objects.get(name=predicted_face_shape)
        recommendations = Recommendation.objects.filter(face_shape=face_shape, gender=gender)
        serializer = RecommendationsSerializer(recommendations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except FaceShape.DoesNotExist:
        return Response({'error': 'Face shape not found'}, status=status.HTTP_404_NOT_FOUND)
    except Recommendation.DoesNotExist:
        return Response({'error': 'No recommendations found for the given face shape and gender'}, status=status.HTTP_404_NOT_FOUND)