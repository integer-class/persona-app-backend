from django.db import models
from django.contrib.auth.models import User
from .utils import PathAndRename

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
]

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to=PathAndRename('avatars/'), blank=True, null=True, default='avatars/default_avatar.png')

    def __str__(self):
        return self.user.username

class FaceShape(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Face Shape"
        verbose_name_plural = "Face Shapes"

class HairStyle(TimeStampedModel):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='images/hair_styles')
    description = models.TextField(blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Hair Style"
        verbose_name_plural = "Hair Styles"

class Accessory(TimeStampedModel):
    CATEGORY_CHOICES = [
        ('glasses', 'Glasses'),
        ('earrings', 'Earrings'),
    ]
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='images/accessories')
    description = models.TextField(blank=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Accessory"
        verbose_name_plural = "Accessories"

class Recommendation(TimeStampedModel):
    face_shape = models.ForeignKey(FaceShape, on_delete=models.CASCADE, related_name='recommendations')
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    hair_styles = models.ManyToManyField(HairStyle, related_name='recommendations')
    accessories = models.ManyToManyField(Accessory, related_name='recommendations')

    def __str__(self):
        return f"{self.face_shape.name} - {self.gender}"

    class Meta:
        verbose_name = "Recommendation"
        verbose_name_plural = "Recommendations"

class Feedback(TimeStampedModel):
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE, related_name='feedbacks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    comment = models.TextField(blank=True)
    rating = models.PositiveSmallIntegerField(default=0, choices=[(i, str(i)) for i in range(1, 6)])

    def __str__(self):
        return f"Feedback by {self.user.username} for {self.recommendation}"

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"

class UserSelection(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='selections')
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE, related_name='selections')
    selected_hair_style = models.ForeignKey(HairStyle, on_delete=models.CASCADE, related_name='selections')
    selected_accessories = models.ManyToManyField(Accessory, related_name='selections')
    
    def __str__(self):
        return f"{self.user.username} - {self.recommendation}"
    
    class Meta:
        verbose_name = "User Selection"
        verbose_name_plural = "User Selections"

class Prediction(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions', null=True)
    image = models.ImageField(upload_to=PathAndRename('uploads/'))
    face_shape = models.ForeignKey(FaceShape, on_delete=models.SET_NULL, null=True, blank=True, related_name='predictions')

    def __str__(self):
        return f"Prediction - {self.face_shape.name if self.face_shape else 'Unknown'}"

class History(TimeStampedModel):
    prediction = models.ForeignKey(Prediction, on_delete=models.CASCADE, related_name='history')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
    user_selection = models.ForeignKey(UserSelection, on_delete=models.CASCADE, related_name='history', null=True, blank=True)
    note = models.TextField(blank=True, null=True)
        
    def __str__(self):
        return f"History of {self.user.username} - {self.prediction.face_shape.name if self.prediction.face_shape else 'Unknown'}"

    class Meta:
        verbose_name = "History"
        verbose_name_plural = "Histories"
        
