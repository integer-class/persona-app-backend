from django.contrib import admin
from .models import FaceShape, HairStyle, Accessory, Recommendation, Feedback, History

admin.site.register(FaceShape)
admin.site.register(HairStyle)
admin.site.register(Accessory)
admin.site.register(Recommendation)
admin.site.register(Feedback)
admin.site.register(History)