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
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='images/hair_styles')
    description = models.TextField(blank=True)

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

class History(TimeStampedModel):
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE, related_name='history')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
    image = models.ImageField(upload_to=PathAndRename('uploads/'), blank=True, null=True)

    def __str__(self):
        return f"History of {self.user.username} - {self.recommendation}"

    class Meta:
        verbose_name = "History"
        verbose_name_plural = "Histories"
