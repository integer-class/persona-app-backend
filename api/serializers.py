from django.contrib.auth.models import User
from rest_framework import serializers
from .models import FaceShape, HairStyle, Accessory, Recommendation, Feedback, History, UserProfile
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'confirm_password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}
        
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    new_email = serializers.EmailField(write_only=True, required=False)

    class Meta:
        model = UserProfile
        fields = ('user', 'avatar', 'new_email')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        new_email = validated_data.pop('new_email', None)
        avatar = validated_data.get('avatar')

        # Update User fields
        user = instance.user
        user.username = user_data.get('username', user.username)
        user.email = user_data.get('email', user.email)
        if 'password' in user_data:
            user.set_password(user_data['password'])
        user.save()

        # Update UserProfile fields
        if avatar:
            instance.avatar = avatar
        instance.save()

        # Handle email change
        if new_email:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_url = f"{settings.FRONTEND_URL}/verify-email/{uid}/{token}/"
            send_mail(
                subject="Verify your new email address",
                message=f"Click the link to verify your new email address: {verification_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[new_email],
            )

        return instance

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self):
        email = self.validated_data['email']
        users = User.objects.filter(email=email)
        for user in users:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
            send_mail(
                subject="Password Reset Request",
                message=f"Click the link to reset your password: {reset_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )

class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            uid = force_str(urlsafe_base64_decode(data['uid']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid UID")

        if not default_token_generator.check_token(user, data['token']):
            raise serializers.ValidationError("Invalid token")

        return data

    def save(self):
        uid = force_str(urlsafe_base64_decode(self.validated_data['uid']))
        user = User.objects.get(pk=uid)
        user.set_password(self.validated_data['new_password'])
        user.save()

class FaceShapeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceShape
        fields = '__all__'

class HairStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = HairStyle
        fields = '__all__'

class AccessorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Accessory
        fields = '__all__'
        
class RecommendationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = '__all__'
        
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
        read_only_fields = ['user']
        
class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'  
        
