from django.db.models.signals import pre_save
from django.dispatch import receiver
from WorkStream.models.customUser import CustomUser

@receiver(pre_save, sender=CustomUser)
def set_username_based_on_email(sender, instance, **kwargs):
    if not instance.username:  # Asegurarse de no sobrescribir usernames existentes
        username = instance.email.split("@")[0]
        instance.username = username
