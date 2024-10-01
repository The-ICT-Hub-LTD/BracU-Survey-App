from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.conf import settings

@receiver(user_signed_up)
def set_staff_on_signup(request, user, sociallogin=None, **kwargs):
    allowed_domains = ['gmail.com','bscse.uiu.ac.bd','bracu.ac.bd']
    email_domain = user.email.split('@')[-1]
    if email_domain in allowed_domains:
        user.is_staff = True
        user.save()
    else:
        user.is_staff = False
        user.save()



# from django.db.models.signals import pre_delete
# from django.dispatch import receiver
# from .models import UserProfile, Complain, Profile

# @receiver(pre_delete, sender=UserProfile)
# def delete_related_profile(sender, instance, **kwargs):
#     try:
#         instance.profile.delete() 
#     except Profile.DoesNotExist:
#         pass

# @receiver(pre_delete, sender=Complain)
# def delete_related_complain_data(sender, instance, **kwargs):
#     if instance.complain_image:
#         instance.complain_image.delete(save=False)
#     if instance.resolved_image:
#         instance.resolved_image.delete(save=False)