from celery import shared_task
from .utils import send_push_notification

@shared_task
def push_notification(token, title, body):
    send_push_notification(token, title, body)
