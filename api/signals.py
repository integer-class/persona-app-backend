from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, History

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
@receiver(post_save, sender=History)
@receiver(post_delete, sender=History)
def clear_history_cache(sender, instance, **kwargs):
    cache.delete_pattern('views.decorators.cache.cache_page.*')