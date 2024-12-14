from django.contrib import admin
from django.utils.html import format_html
from .models import (
    FaceShape, HairStyle, Accessory, Prediction, 
    Recommendation, Feedback, History, UserProfile, 
    UserSelection
)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_email', 'get_avatar_preview')
    search_fields = ('user__username', 'user__email')
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    
    def get_avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="50" height="50" />', obj.avatar.url)
        return '-'
    get_avatar_preview.short_description = 'Avatar'

@admin.register(HairStyle)
class HairStyleAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'get_image_preview', 'created_at')
    list_filter = ('gender', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return '-'
    get_image_preview.short_description = 'Preview'

@admin.register(Accessory)
class AccessoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'get_image_preview', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return '-'
    get_image_preview.short_description = 'Preview'

class HairStyleInline(admin.TabularInline):
    model = Recommendation.hair_styles.through
    extra = 1

class AccessoryInline(admin.TabularInline):
    model = Recommendation.accessories.through
    extra = 1

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('face_shape', 'gender', 'get_hair_styles_count', 'get_accessories_count')
    list_filter = ('face_shape', 'gender')
    search_fields = ('face_shape__name',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [HairStyleInline, AccessoryInline]
    exclude = ('hair_styles', 'accessories')

    def get_hair_styles_count(self, obj):
        return obj.hair_styles.count()
    get_hair_styles_count.short_description = 'Hair Styles'

    def get_accessories_count(self, obj):
        return obj.accessories.count()
    get_accessories_count.short_description = 'Accessories'

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'recommendation', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'comment')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_face_shape', 'created_at')
    list_filter = ('created_at', 'prediction__face_shape')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')
    
    def get_face_shape(self, obj):
        return obj.prediction.face_shape if obj.prediction else '-'
    get_face_shape.short_description = 'Face Shape'

@admin.register(UserSelection)
class UserSelectionAdmin(admin.ModelAdmin):
    list_display = ('user', 'recommendation', 'selected_hair_style', 'get_accessories_count')
    list_filter = ('created_at',)
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('selected_accessories',)

    def get_accessories_count(self, obj):
        return obj.selected_accessories.count()
    get_accessories_count.short_description = 'Accessories'

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('id', 'face_shape', 'get_image_preview', 'created_at')
    list_filter = ('face_shape', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return '-'
    get_image_preview.short_description = 'Preview'

@admin.register(FaceShape) 
class FaceShapeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')