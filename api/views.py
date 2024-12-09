from rest_framework import viewsets, status, generics, permissions
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import MultiPartParser
from .inference import predict_face_shape
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from .models import FaceShape, HairStyle, Accessory, Recommendation, Feedback, History, UserProfile, UserSelection
from .serializers import (
    FaceShapeSerializer,
    HairStyleSerializer,
    AccessorySerializer,
    RecommendationsSerializer,
    FeedbackSerializer,
    HistorySerializer,
    UserSerializer,
    UserProfileSerializer,
    PasswordChangeSerializer,
    PasswordResetSerializer, 
    PasswordResetConfirmSerializer,
    UserSelectionSerializer
)
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django_ratelimit.decorators import ratelimit
import logging

logger = logging.getLogger(__name__)

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
                'user': UserSerializer(user).data
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
                'token' : token.key,
                'user' : UserSerializer(user).data
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

class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return UserProfileView.get_object(self)

class VerifyEmailView(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.email = request.query_params.get('email')
            user.save()
            return Response({'status': 'success', 'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error', 'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(generics.UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"status": "success", "message": "Password updated successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password reset e-mail has been sent."}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password has been reset with the new password."}, status=status.HTTP_200_OK)
    
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
        return History.objects.filter(user=self.request.user).prefetch_related('user__selections')

class UserSelectionViewSet(viewsets.ModelViewSet):
    queryset = UserSelection.objects.all()
    serializer_class = UserSelectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserSelection.objects.filter(user=self.request.user)

def save_image_and_predict(image):
    image_name = default_storage.save(f'uploads/{image.name}', ContentFile(image.read()))
    image_path = default_storage.path(image_name)
    predicted_face_shape = predict_face_shape(image_path)
    return image_name, predicted_face_shape

@api_view(['POST'])
@parser_classes([MultiPartParser])
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
@permission_classes([AllowAny])
def predict(request):
    if 'image' not in request.FILES:
        return Response({'status': 'error', 'message': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    if 'gender' not in request.data:
        return Response({'status': 'error', 'message': 'No gender provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    image = request.FILES['image']
    gender = request.data['gender']
    
    image_name, predicted_face_shape = save_image_and_predict(image)

    try:
        face_shape = FaceShape.objects.get(name=predicted_face_shape)
        recommendations = Recommendation.objects.filter(face_shape=face_shape, gender=gender)
        recommended_hair_styles_ids = recommendations.values_list('hair_styles', flat=True)
        recommended_accessories_ids = recommendations.values_list('accessories', flat=True)
        
        hair_styles = HairStyle.objects.filter(gender=gender)
        accessories = Accessory.objects.all()
        
        recommended_hair_styles = HairStyleSerializer(
            hair_styles.filter(id__in=recommended_hair_styles_ids), many=True
        ).data
        recommended_accessories = AccessorySerializer(
            accessories.filter(id__in=recommended_accessories_ids), many=True
        ).data
        
        other_hair_styles = HairStyleSerializer(
            hair_styles.exclude(id__in=recommended_hair_styles_ids), many=True
        ).data
        other_accessories = AccessorySerializer(
            accessories.exclude(id__in=recommended_accessories_ids), many=True
        ).data
        
        user = request.user if request.user.is_authenticated else None
        if user:
            History.objects.create(user=user, recommendation=recommendations.first(), image=image_name)
        
        return Response({
            'status': 'success',
            'data': {
                'image_url': default_storage.url(image_name),
                'face_shape': predicted_face_shape,
                'recommendations': {
                    'hair_styles': recommended_hair_styles,
                    'accessories': recommended_accessories
                },
                'other_options': {
                    'hair_styles': other_hair_styles,
                    'accessories': other_accessories
                }
            }
        }, status=status.HTTP_200_OK)
    except FaceShape.DoesNotExist:
        return Response({'status': 'error', 'message': 'Face shape not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_user_selection(request):
    user = request.user
    recommendation_id = request.data.get('recommendation_id')
    selected_hair_style_id = request.data.get('selected_hair_style_id')
    selected_accessories_ids = request.data.get('selected_accessories_ids', [])

    if isinstance(selected_accessories_ids, str):
        selected_accessories_ids = selected_accessories_ids.strip('[]').split(',')
        selected_accessories_ids = [int(id.strip()) for id in selected_accessories_ids]
    
    try:
        recommendation = Recommendation.objects.get(id=recommendation_id)
        selected_hair_style = HairStyle.objects.get(id=selected_hair_style_id)
        selected_accessories = Accessory.objects.filter(id__in=selected_accessories_ids)

        user_selection = UserSelection.objects.create(
            user=user,
            recommendation=recommendation,
            selected_hair_style=selected_hair_style
        )
        user_selection.selected_accessories.set(selected_accessories)
        user_selection.save()

        return Response({'status': 'success', 'message': 'User selection saved successfully'}, status=status.HTTP_201_CREATED)
    except Recommendation.DoesNotExist:
        logger.error(f"Recommendation with id {recommendation_id} does not exist")
        return Response({'status': 'error', 'message': 'Invalid recommendation ID provided'}, status=status.HTTP_400_BAD_REQUEST)
    except HairStyle.DoesNotExist:
        logger.error(f"HairStyle with id {selected_hair_style_id} does not exist")
        return Response({'status': 'error', 'message': 'Invalid hair style ID provided'}, status=status.HTTP_400_BAD_REQUEST)
    except Accessory.DoesNotExist:
        logger.error(f"Accessory with ids {selected_accessories_ids} do not exist")
        return Response({'status': 'error', 'message': 'Invalid accessory IDs provided'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def logout(request):
    try:
        request.user.auth_token.delete()
        return Response({'status': 'success', 'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({'status': 'error', 'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)