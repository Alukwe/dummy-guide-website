from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserAnalytics, ProfileChangeLog, CustomUser, UserProfile

User = get_user_model()


@receiver(post_save, sender=CustomUser)
def assign_to_group(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff:
            group, created = Group.objects.get_or_create(name='staff')
            instance.groups.add(group)



@receiver(post_save, sender=CustomUser)
def user_created(sender, instance, created, **kwargs):
    if created:
        # Implement actions you want to perform when a new user is created
        group, create  = Group.objects.get_or_create(name='client')
        instance.groups.add(group)
        UserProfile.objects.create(
            user=instance,
        )
        print('Profile  Created')
@receiver(post_save, sender=CustomUser)
def user_profile_updated(sender, instance, created, **kwargs):
    # Implement actions you want to perform when a user's profile is updated
    if created == False:
        try:
            instance.userprofile.save()
            print('Profile updated! ')
        except:
            UserProfile.objects.create(user=instance)
            print('Profile create for existing user!')


@receiver(post_save, sender=UserAnalytics)
def user_created(sender, instance, created, **kwargs):
    if created:
        # Create a UserAnalytics  record for the new user
        UserAnalytics.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def profile_change_logged(sender, instance, **kwargs):
#     for field_name in instance.profile_changed_fields():
#         old_value = getattr(instance._original, field_name, None)
#         new_value = getattr(instance, field_name, None)
#         if old_value != new_value:
#             ProfileChangeLog.objects.create(
#                 user=instance,
#                 field_name=field_name,
#                 old_value=old_value,
#                 new_value=new_value,
#             )
