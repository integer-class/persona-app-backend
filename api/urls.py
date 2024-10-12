from django.urls import path, include 
from rest_framework.routers import DefaultRouter
from .views import Face_shapeViewSet, Hair_stylesViewSet, AccessoriesViewSet, RecommendationsViewSet, Recommendations_hair_stylesViewSet, Recommendations_accessoriesViewSet, FeedbackViewSet, HistoryViewSet

router = DefaultRouter()
router.register(r'face_shape', Face_shapeViewSet)
router.register(r'hair_styles', Hair_stylesViewSet)
router.register(r'accessories', AccessoriesViewSet)
router.register(r'recommendations', RecommendationsViewSet)
router.register(r'recommendations_hair_styles', Recommendations_hair_stylesViewSet)
router.register(r'recommendations_accessories', Recommendations_accessoriesViewSet)
router.register(r'feedback', FeedbackViewSet)
router.register(r'history', HistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

