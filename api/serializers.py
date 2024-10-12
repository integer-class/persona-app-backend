from rest_framework import serializers
from .models import Face_shape, Hair_styles, Accessories, Recommendations, Recommendations_hair_styles, Recommendations_accessories, Feedback, History

class Face_shapeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Face_shape
        fields = '__all__'
        
class Hair_stylesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hair_styles
        fields = '__all__'
        
class AccessoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accessories
        fields = '__all__'
        
class RecommendationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendations
        fields = '__all__'
        
class Recommendations_hair_stylesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendations_hair_styles
        fields = '__all__'
        
class Recommendations_accessoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendations_accessories
        fields = '__all__'
        
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
        
class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'  
        
