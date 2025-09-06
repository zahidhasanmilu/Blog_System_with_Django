from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, CustomUser

@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # যদি নতুন ইউজার তৈরি হয়, তবে Profile তৈরি করুন
    if created:
        Profile.objects.create(user=instance)
    else:
        # existing profile update করার সময়
        if hasattr(instance, 'user_profile'):
            instance.user_profile.save()
