# App_Survey/pipeline.py

from django.core.exceptions import PermissionDenied
from .models import Profile


def require_staff(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        if not user.is_staff:
            raise PermissionDenied("You do not have permission to access this site.")
    else:
        email = details.get('email')
        allowed_domains = ['gmail.com']  # Replace with your domains
        if not email.endswith(tuple(allowed_domains)):
            raise PermissionDenied("You are not authorized to access this site.")


def create_user_profile(strategy, details, backend, user=None, *args, **kwargs):
    if user is None:
        email = details.get('email')
        first_name = details.get('first_name', '')
        last_name = details.get('last_name', '')
        name = f"{first_name} {last_name}".strip()
        user = strategy.create_user(email=email, name=name)
        user.is_staff = True  # Grant staff status
        user.save()

        # Optionally, populate the Profile model
        Profile.objects.create(
            user=user,
            username=f"{first_name.lower()}.{last_name.lower()}",
            # Populate other fields as needed
        )
    return {'user': user}


def verify_email(strategy, details, backend, user=None, *args, **kwargs):
    if details.get('email_verified'):
        return
    else:
        raise PermissionDenied("Email address not verified.")