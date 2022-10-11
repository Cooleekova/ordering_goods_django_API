from celery import shared_task
from django.core.mail import send_mail

"""
Запуск на Windows:
celery -A orders  worker -l info -P eventlet
"""


@shared_task()
def new_user_registered_email(token, subject, recipient_list):
    send_mail(
        subject=subject,
        message=token,
        from_email='',
        recipient_list=[recipient_list],
    )

    return None


@shared_task()
def new_order_email(recipient_list):
    send_mail(
        subject='Обновление статуса заказа',
        message='Заказ сформирован',
        from_email='',
        recipient_list=[recipient_list],
    )

    return None

