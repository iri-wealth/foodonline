from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from .models import User, UserProfile


@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    print('created')

    if created:
        UserProfile.objects.create(user=instance)
        print('User Profile is created')
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
            print('User Profile is updated')
        except:
            #create userprofile if not exists
            UserProfile.objects.create(user=instance)
            print('User Profile is created')


#post_save_connect(post_save_create_profile_receiver, sender=User)
@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    print(instance.username, 'new user was pre-saved')

