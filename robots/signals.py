from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .logic import send_notification_email
from .models import Robot


@receiver(post_save, sender=Robot)
def notify_customer(sender, instance, **kwargs):
    robot = Robot.objects.filter(serial=instance.serial)
    if len(robot)==1:
        send_notification_email(instance)