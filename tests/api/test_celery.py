import pytest
from django.core.mail import send_mail
from django.urls import reverse

from api.tasks import new_user_registered_email




#
# def test_create_task(celery_app, celery_worker):
#     @celery_app.task
#     def mul(x, y):
#         return x * y
#
#     celery_worker.reload()
#     assert mul.apply_async()

    # assert mul.delay(4, 4).get(timeout=10) == 16

#
# @pytest.mark.celery(result_backend='redis://')
# @pytest.mark.django_db
# def test_new_user_registered_email(celery_app, celery_worker, token, user):
#
#     @celery_app.task
#     def new_user_registered_email(token, subject, recipient_list):
#         send_mail(
#             subject=subject,
#             message=token,
#             from_email='',
#             recipient_list=[recipient_list],
#         )
#
#         return None
#
#     token = token(user=user)
#     assert new_user_registered_email.delay(
#                 token=token.key,
#                 subject=f"Password Token for {token.user.email}",
#                 recipient_list=token.user.email,
#             )
#
#

"""
Запуск на Windows:
celery -A orders  worker -l info -P eventlet
"""


# @shared_task()
# def new_user_registered_email(token, subject, recipient_list):
#     send_mail(
#         subject=subject,
#         message=token,
#         from_email='',
#         recipient_list=[recipient_list],
#     )
#
#     return None
#
#
# @shared_task()
# def new_order_email(recipient_list):
#     send_mail(
#         subject='Обновление статуса заказа',
#         message='Заказ сформирован',
#         from_email='',
#         recipient_list=[recipient_list],
#     )
#
#     return None










# # удачное размещение заказа из корзины
# @pytest.mark.django_db
# def test_confirm_order_from_basket(user, auth_client, order_factory, product_info_factory, contact_factory):
#     test_contact = contact_factory(user=user)
#     # создаём тестовый товар
#     test_item = product_info_factory(make_m2m=True)
#     # создаём корзину
#     test_order = order_factory(make_m2m=True, user=user)
#
#     # совершаем запрос POST к API по URL,
#     # добавляем тестовый товар в корзину
#     url_basket = reverse("api:basket")
#
#     resp1 = auth_client.post(
#         url_basket,
#         {'items': f'[{{"product_info": {test_item.id}, "quantity": "1"}}]'}
#     )
#     # проверяем код ответа
#     assert resp1.status_code == HTTP_200_OK
#     resp1_json = resp1.json()
#     # проверяем JSON ответ
#     # assert resp1_json['Status'] is True
#
#     # теперь нужно разместить заказ
#     # совершаем запрос GET к API по URL
#     url_to_post_order = reverse("api:order")
#
#     resp2 = auth_client.post(
#         url_to_post_order,
#         {"id": f'{test_order.id}', "contact": f'{test_contact.id}'}
#     )
#     resp2_json = resp2.json()
#     # проверяем код ответа и JSON ответ
#     assert resp2.status_code == HTTP_200_OK
#     assert resp2_json['Status'] is True