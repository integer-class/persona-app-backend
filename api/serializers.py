from django.contrib.auth.models import User
from rest_framework import serializers
from .models import FaceShape, HairStyle, Accessory, Recommendation, Feedback, History

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

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
        
class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'  
        
