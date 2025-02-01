from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from celery import shared_task

from booking.models import Subscribe, Order


@shared_task
def subscribe_send_offers(subject, text):
    subscribers = Subscribe.objects.all()
    body = render_to_string('email/send-offers.html', context={'subject': subject, 'text': text})
    for i in subscribers:
        message = EmailMessage(subject = subject, body = body, from_email = f"Anywayanytrip.az <{settings.EMAIL_HOST_USER}>", to=[i.email, ])
        message.content_subtype = 'html'
        message.send()

@shared_task
def me_send_orders(order):
    order = Order.objects.get(id=order)
    body = render_to_string('email/send-orders.html', context={'order': order})
    message = EmailMessage(subject = f"Sifariş{order.id}", body = body, from_email = f"Anywayanytrip.az <{settings.EMAIL_HOST_USER}>", to=["gbayramov@hotmail.com", ])
    message.content_subtype = 'html'
    message.send()
