import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN


""" Партнёр """


# проверка URL при размещении прайс-листа
@pytest.mark.parametrize(
    ["url", "expected_status"],
    (
        ("https://raw.githubusercontent.com/Cooleekova/python-final-diplom/master/data/shop1.yaml", True),
        ("fvhgghghkgjgcxkhfkvgs", False),
    )
)
@pytest.mark.django_db
def test_partner_valid_url(auth_partner, url, expected_status):
    partner_url_for_update = reverse("api:partner-update")
    resp = auth_partner.post(
        partner_url_for_update,
        {'url': f'{url}'}
    )
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert resp_json['Status'] == expected_status


# успешное получение статуса партнёра
@pytest.mark.django_db
def test_partner_get_status(auth_partner, shop_factory):
    # создаём тестовый магазин
    test_shop = shop_factory(make_m2m=True)
    # совершаем запрос GET к API по URL
    url_to_get_state = reverse("api:partner-state")
    resp = auth_partner.get(url_to_get_state)
    resp_json = resp.json()
    # проверяем код ответа и JSON ответ
    assert resp.status_code == HTTP_200_OK
    assert resp_json['id'] == test_shop.id
    assert resp_json['state'] == test_shop.state


# успешное изменение статуса партнёра
@pytest.mark.django_db
def test_partner_update_status(auth_partner, shop_factory):
    # создаём тестовый магазин
    shop_factory(make_m2m=True)
    # совершаем запрос POST к API по URL
    state_url = reverse("api:partner-state")
    new_test_state = 'False'
    resp = auth_partner.post(
        state_url,
        {'state': f'{new_test_state}'}
    )
    resp_json = resp.json()
    # проверяем код ответа и JSON ответ
    assert resp.status_code == HTTP_200_OK
    assert resp_json['Status'] is True


# успешное получение заказов партнёром
@pytest.mark.django_db
def test_partner_get_orders(user, user_partner, auth_partner, order_factory, product_info_factory, order_items_factory):
    # создаём тестовый товар
    test_item = product_info_factory(make_m2m=True)
    # присваиваем тестовый товар тестируемому магазину (user_partner)
    shop = test_item.shop
    shop.user = user_partner
    # создаём тестовый заказ
    test_order = order_factory(make_m2m=True, user=user, status='new')
    # создаём тестовую позицию
    order_items_factory(make_m2m=True, order=test_order, product_info=test_item, quantity=1)
    # чтобы получить размещённый заказ
    # совершаем запрос GET к API по URL
    url_to_get_orders = reverse("api:partner-orders")
    resp = auth_partner.get(url_to_get_orders)
    resp_json = resp.json()
    # проверяем код ответа и JSON ответ
    assert resp.status_code == HTTP_200_OK
    assert resp_json[0]['id'] == test_order.id


# неуспешное получение заказов при отсутствии user.type == SHOP
@pytest.mark.django_db
def test_not_partner_cannot_get_orders(user, auth_client, order_factory, product_info_factory, order_items_factory):
    # создаём тестовый товар
    test_item = product_info_factory(make_m2m=True)
    # создаём тестовый заказ
    test_order = order_factory(make_m2m=True, user=user, status='new')
    # создаём тестовую позицию
    order_items_factory(make_m2m=True, order=test_order, product_info=test_item, quantity=1)
    # чтобы получить размещённый заказ
    # совершаем запрос GET к API по URL
    # у клиента при этом user.type != SHOP
    url_to_get_orders = reverse("api:partner-orders")
    resp = auth_client.get(url_to_get_orders)
    # проверяем код ответа
    assert resp.status_code == HTTP_403_FORBIDDEN
