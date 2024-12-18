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
from .models import FaceShape, HairStyle, Accessory, Prediction, Recommendation, Feedback, History, UserProfile, UserSelection
from .serializers import (
    FaceShapeSerializer,
    HairStyleSerializer,
    AccessorySerializer,
    PredictionSerializer,
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
from django.db import transaction
import logging
from PIL import Image
from io import BytesIO
import pyheif # type: ignore
from PIL import UnidentifiedImageError

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

class PredictionViewSet(viewsets.ModelViewSet):
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Prediction.objects.filter(user=self.request.user)

def save_image_and_predict(image):
    try:
        # Open the image using Pillow
        img = Image.open(image)
    except UnidentifiedImageError:
        if image.name.lower().endswith(('.heic', '.avif')):
            try:
                heif_file = pyheif.read(image)
                img = Image.frombytes(
                    heif_file.mode, 
                    heif_file.size, 
                    heif_file.data,
                    "raw",
                    heif_file.mode,
                    heif_file.stride,
                )
            except pyheif.error.HeifError as e:
                logger.error(f"Error reading HEIF/AVIF file: {str(e)}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error reading HEIF/AVIF file: {str(e)}")
                raise
        else:
            logger.error(f"Unidentified image format for file: {image.name}")
            raise

    # Calculate new dimensions while maintaining aspect ratio
    max_size = 800
    ratio = min(max_size/float(img.size[0]), max_size/float(img.size[1]))
    new_size = tuple([int(dim * ratio) for dim in img.size])
    
    # Resize image maintaining aspect ratio
    img = img.resize(new_size, Image.LANCZOS)

    # Save with reduced quality to decrease file size
    img_io = BytesIO()
    # Convert to RGB if image is in RGBA mode
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    img.save(img_io, format='JPEG', quality=85, optimize=True)
    img_io.seek(0)

    # Save the image to the default storage
    image_name = default_storage.save(f'uploads/{image.name}', ContentFile(img_io.read()))
    image_path = default_storage.path(image_name)

    # Predict the face shape
    predicted_face_shape = predict_face_shape(image_path)
    return image_name, predicted_face_shape

@api_view(['POST'])
@parser_classes([MultiPartParser])
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
@permission_classes([AllowAny])
def predict(request):
    if 'image' not in request.FILES:
        logger.error("No image provided in the request")
        return Response({'status': 'error', 'message': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    if 'gender' not in request.data:
        logger.error("No gender provided in the request")
        return Response({'status': 'error', 'message': 'No gender provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    image = request.FILES['image']
    gender = request.data['gender']
    
    try:
        image_name, predicted_face_shape = save_image_and_predict(image)
    except Exception as e:
        logger.error(f"Error in save_image_and_predict: {str(e)}")
        return Response({'status': 'error', 'message': 'Error processing image'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        
        prediction = Prediction.objects.create(
            image=image,
            face_shape=face_shape,
            user=request.user if request.user.is_authenticated else None  # Add user if authenticated
        )
        
        return Response({
            'status': 'success',
            'data': {
                'prediction_id': prediction.id,
                'image_url': default_storage.url(image_name),
                'face_shape': predicted_face_shape,
                'recommendations_id': recommendations.values_list('id', flat=True),
                
                'recommendations': {
                    'hair_styles': [{
                        **hair_style,
                        'image': request.build_absolute_uri(hair_style['image']) 
                    } for hair_style in recommended_hair_styles],
                    'accessories': [{
                        **accessory,
                        'image': request.build_absolute_uri(accessory['image'])
                    } for accessory in recommended_accessories]
                },
                'other_options': {
                    'hair_styles': [{
                        **hair_style,
                        'image': request.build_absolute_uri(hair_style['image'])
                    } for hair_style in other_hair_styles],
                    'accessories': [{
                        **accessory,
                        'image': request.build_absolute_uri(accessory['image'])
                    } for accessory in other_accessories]
                }
            }
        }, status=status.HTTP_200_OK)
        
    except FaceShape.DoesNotExist:
        logger.error(f"Face shape '{predicted_face_shape}' not found in the database")
        return Response({'status': 'error', 'message': 'Face shape not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return Response({'status': 'error', 'message': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['POST'])
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def logout(request):
    try:
        request.user.auth_token.delete()
        return Response({'status': 'success', 'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({'status': 'error', 'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def delete_image(request):
    image_id = request.data.get('image_id')
    if image_id:
        logger.info(f"Attempting to delete image with ID: {image_id}")
        
        # Delete from database
        try:
            prediction = Prediction.objects.get(id=image_id)
            prediction.delete()  # This will also delete the file from storage
            logger.info(f"Prediction and image deleted successfully: {image_id}")
            return Response({'status': 'success', 'message': 'Image and prediction deleted successfully'})
        except Prediction.DoesNotExist:
            logger.error(f"Prediction not found for ID: {image_id}")
            return Response({'status': 'error', 'message': 'Image not found'}, status=404)
    logger.error("Image ID not provided in the request")
    return Response({'status': 'error', 'message': 'Image ID not provided'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_user_choices(request):
    try:
        # Get required data
        user = request.user
        prediction_id = request.data.get('prediction_id')
        recommendation_id = request.data.get('recommendation_id')
        selected_hair_style_id = request.data.get('selected_hair_style_id')
        selected_accessories_ids = request.data.get('selected_accessories_ids', [])

        # Process accessories ids if string
        if isinstance(selected_accessories_ids, str):
            selected_accessories_ids = selected_accessories_ids.strip('[]').split(',')
            selected_accessories_ids = [int(id.strip()) for id in selected_accessories_ids]

        # Get required objects and validate
        try:
            prediction = Prediction.objects.get(id=prediction_id)
            recommendation = Recommendation.objects.get(id=recommendation_id)
            selected_hair_style = HairStyle.objects.get(id=selected_hair_style_id)
            selected_accessories = Accessory.objects.filter(id__in=selected_accessories_ids)
        except (Prediction.DoesNotExist, Recommendation.DoesNotExist, 
                HairStyle.DoesNotExist, Accessory.DoesNotExist) as e:
            logger.error(f"Object lookup error: {str(e)}")
            return Response({
                'status': 'error',
                'message': 'Invalid ID provided'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Use transaction to ensure data consistency
        with transaction.atomic():
            # Create user selection
            user_selection = UserSelection.objects.create(
                user=user,
                recommendation=recommendation,
                selected_hair_style=selected_hair_style
            )
            user_selection.selected_accessories.set(selected_accessories)

            # Create history entry
            history = History.objects.create(
                prediction=prediction,
                user=user,
                user_selection=user_selection
            )

        return Response({
            'status': 'success',
            'message': 'Choices saved successfully',
            'data': {
                'history': HistorySerializer(history).data,
                'user_selection': UserSelectionSerializer(user_selection).data
            }
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        logger.error(f"Error saving user choices: {str(e)}")
        return Response({
            'status': 'error', 
            'message': 'Error saving choices'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_history_note(request, history_id):
    try:
        history = History.objects.get(id=history_id, user=request.user)
        note = request.data.get('note')
        
        if note is not None:
            history.note = note
            history.save()
            
            return Response({
                'status': 'success',
                'message': 'Note updated successfully',
                'data': HistorySerializer(history).data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error',
                'message': 'Note content is required'
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except History.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'History not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)