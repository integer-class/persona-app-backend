from rest_framework import viewsets, status, generics, permissions
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from .inference import predict_face_shape
from .models import FaceShape, HairStyle, Accessory, Recommendation, Feedback, History, UserProfile
from .serializers import UserSerializer, FaceShapeSerializer, HairStyleSerializer, AccessorySerializer, RecommendationsSerializer, FeedbackSerializer, HistorySerializer, UserProfileSerializer
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django_ratelimit.decorators import ratelimit

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'status': 'success',
            'message': 'User authenticated successfully',
            'data': {
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
                }
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
            'status' : 'success',
            'message' : 'User registered successfully',
            'data' : {
                'user' : UserSerializer(user, context=self.get_serializer_context()).data,
                'token' : token.key
            }
        }, status=status.HTTP_201_CREATED)
        

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        profile, created = UserProfile.objects.get_or_create(user=user)
        return profile

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'status': 'success',
            'message': 'User profile retrieved successfully',
            'data': serializer.data
        })

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'status': 'success',
            'message': 'User profile updated successfully',
            'data': serializer.data
        })

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
    queryset = Feedback.objects.select_related('recommendation', 'user').all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return History.objects.filter(user=self.request.user)
    
@api_view(['POST'])
@parser_classes([MultiPartParser])
def predict(request):
    if 'image' not in request.FILES:
        return Response({'status': 'error', 'message': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    if 'gender' not in request.data:
        return Response({'status': 'error', 'message': 'No gender provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    image = request.FILES['image']
    gender = request.data['gender']
    
    # Save the uploaded image
    image_name = default_storage.save(f'uploads/{image.name}', ContentFile(image.read()))
    image_path = default_storage.path(image_name)
    
    predicted_face_shape = predict_face_shape(image_path)  # Your prediction function

    try:
        face_shape = FaceShape.objects.get(name=predicted_face_shape)
        recommendations = Recommendation.objects.filter(face_shape=face_shape, gender=gender)
        serializer = RecommendationsSerializer(recommendations, many=True)
        
        # Save the prediction to history
        user = request.user
        History.objects.create(user=user, recommendation=recommendations.first(), image=image_name)
        
        return Response({
            'status': 'success',
            'message': 'Recommendations retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    except FaceShape.DoesNotExist:
        return Response({'status': 'error', 'message': 'Face shape not found'}, status=status.HTTP_404_NOT_FOUND)
    except Recommendation.DoesNotExist:
        return Response({'status': 'error', 'message': 'No recommendations found for the given face shape and gender'}, status=status.HTTP_404_NOT_FOUND)