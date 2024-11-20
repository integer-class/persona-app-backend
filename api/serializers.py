from django.contrib.auth.models import User
from rest_framework import serializers
from .models import FaceShape, HairStyle, Accessory, Recommendation, Feedback, History, UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ('user', 'avatar')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
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

        return instance

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
        
