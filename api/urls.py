from django.urls import path, include 
from rest_framework.routers import DefaultRouter
from .views import (
    FaceShapeViewSet,
    HairStyleViewSet,
    AccessoryViewSet,
    PredictionViewSet,
    RecommendationsViewSet,
    FeedbackViewSet,
    HistoryViewSet,
    CustomAuthToken,
    RegisterView,
    predict,
    UserProfileView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
    logout,
    UpdateProfileView,
    VerifyEmailView,
    UserSelectionViewSet,
    delete_image,
    save_user_choices,
)

router = DefaultRouter()
router.register(r'face-shapes', FaceShapeViewSet)
router.register(r'hair-styles', HairStyleViewSet)
router.register(r'accessories', AccessoryViewSet)
router.register(r'recommendations', RecommendationsViewSet)
router.register(r'feedback', FeedbackViewSet)
router.register(r'history', HistoryViewSet)
router.register(r'predictions', PredictionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomAuthToken.as_view(), name='auth'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', logout, name='logout'),
    path('predict/', predict, name='predict'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='profile-update'),
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('password-change/', PasswordChangeView.as_view(), name='password-change'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('delete-image/', delete_image, name='delete_image'),
    path('save-record/', save_user_choices, name='save_record'),
]

