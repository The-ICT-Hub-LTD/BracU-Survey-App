from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
import re

class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save a superuser"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Define the related_name for is_staff field
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='app_auth_users_is_staff'
    )

    # Define the related_name for is_active field
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='app_auth_users_is_active'
    )

    objects = UserProfileManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name of the user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of the user"""
        return self.name

    def __str__(self):
        """Return string representation of our user"""
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=100, blank=True)
    address1 = models.TextField(max_length=400, blank=True)
    city = models.CharField(max_length=40, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.email + "'s Profile"

    # Check if all fields in the profile are filled
    def is_fully_filled(self):
        fields_name = [f.name for f in self._meta.get_fields()]

        for field_name in fields_name:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False
        return True

# Signal to create or update profile when user is created
@receiver(post_save, sender=UserProfile)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    print(instance)
    if created:
        Profile.objects.create(user=instance)
        
    else:
        instance.profile.save()
    

# Custom validator for student ID
def validate_student_id(value):
    if not re.match(r'^\d{8}$', value):  
        raise ValidationError("Student ID must be exactly 8 digits.")
    if value == "12345678":
        raise ValidationError("Student ID cannot be a serial number like 12345678.")

class Complain(models.Model):
    class FeedbackStatus(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        SOLVED = 'Solved', 'Solved'
        ON_PROCESS = 'On Process', 'On Process'

    student_name = models.CharField(max_length=100, blank=True, null=True)
    student_id = models.CharField(max_length=8, validators=[validate_student_id])
    problem_details = models.TextField()
    complain_image = models.ImageField(upload_to='complain_images/', blank=True, null=True)
    is_resolved = models.BooleanField(default=False)
    resolved_image = models.ImageField(upload_to='resolved_images/', blank=True, null=True)
    solution_details = models.TextField(blank=True, null=True, default="Pending")
    feedback_status = models.CharField(max_length=10, choices=FeedbackStatus.choices, default=FeedbackStatus.PENDING)
    submitted_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.student_name} - {self.student_id}"
    
    def save(self, *args, **kwargs):
        if self.feedback_status == self.FeedbackStatus.SOLVED:
            self.is_resolved = True
        else:
            self.is_resolved = False
        super().save(*args, **kwargs)

