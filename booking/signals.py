from django.dispatch import receiver
from django.urls import reverse
from django.db.models.signals import post_save
from django.conf import settings
from booking.models import Order, Subscribe, Announcement, Room
from booking.tasks import me_send_orders
from django.core.mail import send_mail

@receiver(post_save, sender=Order)
def on_order_saved(sender, instance, created, **kwargs):
    me_send_orders.delay(instance.id,)


@receiver(post_save, sender=Announcement)
def send_announcement_email_to_subscribers(sender, instance, created, **kwargs):
    if created:
        subscribers = Subscribe.objects.all()
        subject = f"Yeni Otel Əlavə olundu. Otelin adı: {instance.title}"
        message = f"Başlıq: {instance.title}\n\nAçıqlama: {instance.description}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [subscriber.email for subscriber in subscribers]
        send_mail(subject,message,from_email,recipient_list,fail_silently=False,)
   

@receiver(post_save, sender=Room)
def send_room_email_to_subscribers(sender, instance, created, **kwargs):
    if created:
        subscribers = Subscribe.objects.all()
        subject = f"Yeni otaq Əlavə olundu. Otelin adı: {instance.room_name}"
        message = f"Başlıq: {instance.room_name}\n\nAçıqlama: {instance.description}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [subscriber.email for subscriber in subscribers]
        send_mail(subject,message,from_email,recipient_list,fail_silently=False,)