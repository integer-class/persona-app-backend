# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include('api.urls')),
# ]

from django.urls import path
from .views import classify_face_shape

urlpatterns = [
    path('classify/', classify_face_shape, name='classify_face_shape'),
]