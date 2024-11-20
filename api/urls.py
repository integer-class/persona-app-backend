from django.urls import path, include 
from rest_framework.routers import DefaultRouter
from .views import FaceShapeViewSet, HairStyleViewSet, AccessoryViewSet, RecommendationsViewSet, CustomAuthToken, RegisterView, FeedbackViewSet, HistoryViewSet, UserProfileView, predict

router = DefaultRouter()
router.register(r'face-shapes', FaceShapeViewSet)
router.register(r'hair-styles', HairStyleViewSet)
router.register(r'accessories', AccessoryViewSet)
router.register(r'recommendations', RecommendationsViewSet)
router.register(r'feedback', FeedbackViewSet)
router.register(r'history', HistoryViewSet)

urlpatterns = [        
    path('', include(router.urls)),
    path('auth/', CustomAuthToken.as_view(), name='auth'),   
    path('register/', RegisterView.as_view(), name='register'),
    path('predict/', predict, name='predict'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]

