from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import  settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

# User = get_user_model()

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    # user_identifier = models.CharField(max_length=10, unique=True, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    # def save(self, *args, **kwargs):
    #     if not self.user_identifier:
    #         #Generate a unique identifier, e.g., using UUIDor other method
    #         self.user_identifier = generate_unique_identifier()
    #     super().save(*args, **kwargs)
    #
    def __str__(self):
        return self.email

    # Custom registration logic to check phone number limits
    def custom_registration(self, username, email, password, phone_number):
        # Check if there are already two registration limit for the phone number
        registration_count = CustomUser.objects.filter(phone_number=phone_number).count()
        if registration_count >= 2:
            raise ValidationError("Phone number registration limit reached")

        # Creat a new user
        self.phone_number = phone_number
        return self

# def generate_unique_identifier():
    # Implement your logic to generate a unique user identifier
    # This cloud be a UUID, a custom algorithm, or any method that ensures uniqueness
    # Example:
    # return 'UID1234'

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    linkedin_profile = models.URLField(blank=True)
    twitter_profile = models.URLField(blank=True)
    profile_completeness_score = models.IntegerField(default=0)

    def update_profile_completeness(self):
        # Calculate the profile completeness score based on the data in the profile
        completeness_score = 0
        if self.bio:
            completeness_score += 10 # Assign points for having a bio
        if self.linkedin_profile:
            completeness_score += 5
        if self.location:
            completeness_score += 5
        if self.website:
            completeness_score += 5
        if self.twitter_profile:
            completeness_score  += 5
            
        # Update the profile completeness score
        self.profile_completeness_score = completeness_score
        self.save()
            
    def __str__(self):
        return f'{self.user.username}'

    # Create customer permissions for staff/admin to edit user profiles
    # edit_user_profile = Permission.objects.create(
    #     codename = 'can_edit_user_profile',
    #     name='Can edit user profile',
    #     content_type = ContentType.objects.get_for_model(UserProfile),
    # )

class ProfilePicture(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user_profile.user.username}'s profile picture"



class UserAnalytics(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    login_count = models.PositiveIntegerField(default=0)
    time_spent = models.DurationField(default=timezone.timedelta(seconds=0))

    def track_login(self):
        # Update login count and time spent when the user logs in
        self.login_count += 1
        self.save()

    def track_time_spent(self, duration):
        # Update time spent when the user interacts with the platform
        self.time_spent += duration
        self.save()

class ProfileChangeLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=50)
    old_value = models.TextField()
    new_value = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
