import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

""" Корзина """


# получение корзины пользователем
@pytest.mark.django_db
def test_get_basket(user, auth_client, order_factory):
    # создаём корзину
    order_factory(make_m2m=True, user=user)
    # совершаем запрос GET к API по URL
    url = reverse("api:basket")
    resp = auth_client.get(url)
    # проверяем код ответа
    assert resp.status_code == HTTP_200_OK


# не получение корзины не авторизованным пользователем
@pytest.mark.django_db
def test_not_auth_user_has_no_access_to_basket(user, client, order_factory):
    # создаём корзину
    order_factory(make_m2m=True, user=user)
    # совершаем запрос GET к API по URL
    url = reverse("api:basket")
    resp = client.get(url)
    # проверяем код ответа
    assert resp.status_code == HTTP_403_FORBIDDEN


# добавление товара в корзину
@pytest.mark.django_db
def test_add_items_to_basket(user, auth_client, order_factory, product_info_factory):
    # создаём тестовый товар
    test_item = product_info_factory(make_m2m=True)
    # создаём корзину
    order_factory(make_m2m=True, user=user)

    # совершаем запрос POST к API по URL,
    # добавляем тестовый товар в корзину
    url = reverse("api:basket")
    resp1 = auth_client.post(
        url,
        {'items': f'[{{"product_info": {test_item.id}, "quantity": "1"}}]'}
    )
    # проверяем код ответа
    assert resp1.status_code == HTTP_200_OK
    resp1_json = resp1.json()
    # проверяем JSON ответ
    assert resp1_json['Status'] is True

    # теперь нужно проверить, что товар появился в корзине
    # совершаем запрос GET к API по URL
    resp2 = auth_client.get(url)
    resp2_json = resp2.json()
    # проверяем код ответа и JSON ответ
    assert resp2.status_code == HTTP_200_OK
    assert resp2_json[0]['id']
    assert resp2_json[0]['total_sum']
    assert resp2_json[0]['status'] == 'basket'
    assert resp2_json[0]['ordered_items'][0]['product_info']['product']['name'] == test_item.product.name


# неудачное размещение заказа,если не указан контакт
@pytest.mark.django_db
def test_order_not_confirmed_without_contact(user, auth_client, order_factory, product_info_factory):
    # создаём тестовый товар
    test_item = product_info_factory(make_m2m=True)
    # создаём корзину
    test_order = order_factory(make_m2m=True, user=user)

    # совершаем запрос POST к API по URL,
    # добавляем тестовый товар в корзину
    url_basket = reverse("api:basket")
    resp1 = auth_client.post(
        url_basket,
        {'items': f'[{{"product_info": {test_item.id}, "quantity": "1"}}]'}
    )
    # проверяем код ответа
    assert resp1.status_code == HTTP_200_OK
    resp1_json = resp1.json()
    # проверяем JSON ответ
    assert resp1_json['Status'] is True

    # теперь нужно разместить заказ
    # совершаем запрос POST к API по URL
    url_to_post_order = reverse("api:order")
    resp2 = auth_client.post(url_to_post_order, id=test_order.id)
    resp2_json = resp2.json()
    # проверяем код ответа и JSON ответ
    assert resp2.status_code == HTTP_200_OK
    assert resp2_json['Status'] is False


""" Заказ """


# получение заказа пользователем
@pytest.mark.django_db
def test_get_orders(user, auth_client, order_factory, product_info_factory, contact_factory):
    # создаём тестовый контакт
    test_contact = contact_factory(make_m2m=True, user=user)
    # создаём тестовый заказ
    order_factory(make_m2m=True, user=user, status='new', contact=test_contact)
    # чтобы получить размещённый заказ
    # совершаем запрос GET к API по URL
    url_to_get_order = reverse("api:order")
    resp = auth_client.get(url_to_get_order)
    resp_json = resp.json()
    # проверяем код ответа и JSON ответ
    assert resp.status_code == HTTP_200_OK
    assert resp_json[0]['id']
    assert resp_json[0]['dt']
    assert resp_json[0]['status']


# не получение заказа не авторизованным пользователем
@pytest.mark.django_db
def test_not_auth_client_fail_to_get_orders(client):
    # чтобы получить размещённый заказ
    # совершаем запрос GET к API по URL
    url_to_get_order = reverse("api:order")
    resp = client.get(url_to_get_order)
    # проверяем код ответа
    assert resp.status_code == HTTP_403_FORBIDDEN
