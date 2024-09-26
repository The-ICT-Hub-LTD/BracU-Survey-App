from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import UserProfile, Complain, Profile

@receiver(pre_delete, sender=UserProfile)
def delete_related_profile(sender, instance, **kwargs):
    try:
        instance.profile.delete() 
    except Profile.DoesNotExist:
        pass

@receiver(pre_delete, sender=Complain)
def delete_related_complain_data(sender, instance, **kwargs):
    if instance.complain_image:
        instance.complain_image.delete(save=False)
    if instance.resolved_image:
        instance.resolved_image.delete(save=False)