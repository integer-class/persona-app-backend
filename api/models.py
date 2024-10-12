from django.db import models
from django.contrib.auth.models import User
    
class Face_shape(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class Hair_styles(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/hair_styles')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
class Accessories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/accessories')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
class Recommendations(models.Model):
    id = models.AutoField(primary_key=True)
    Face_shape = models.ForeignKey(Face_shape, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    
class Recommendations_hair_styles(models.Model):
    id = models.AutoField(primary_key=True)
    Recommendations = models.ForeignKey(Recommendations, on_delete=models.CASCADE)
    Hair_styles = models.ForeignKey(Hair_styles, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    
class Recommendations_accessories(models.Model):
    id = models.AutoField(primary_key=True)
    Recommendations = models.ForeignKey(Recommendations, on_delete=models.CASCADE)
    Accessories = models.ForeignKey(Accessories, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    Recommendations = models.ForeignKey(Recommendations, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    rating = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    

class History(models.Model):
    id = models.AutoField(primary_key=True)
    Recommendations = models.ForeignKey(Recommendations, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
