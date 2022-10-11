import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from rest_framework.authtoken.admin import User
from django.urls import reverse
from rest_framework.status import HTTP_201_CREATED
from rest_framework.authtoken.models import Token


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def contact_factory():
    def factory(**kwargs):
        return baker.make('Contact', **kwargs)
    return factory


@pytest.fixture
def category_factory():
    def factory(**kwargs):
        return baker.make('Category', **kwargs)
    return factory


@pytest.fixture
def product_factory():
    def factory(**kwargs):
        return baker.make('Product', **kwargs)
    return factory


@pytest.fixture
def order_factory():
    def factory(**kwargs):
        return baker.make('Order', **kwargs)
    return factory


@pytest.fixture
def order_items_factory():
    def factory(**kwargs):
        return baker.make('OrderItem', **kwargs)
    return factory


@pytest.fixture
def product_info_factory():
    def factory(**kwargs):
        category = baker.make('Category', **kwargs)
        product = baker.make('Product', category_id=category.id, **kwargs)
        shop = baker.make('Shop', **kwargs)
        return baker.make('ProductInfo', product_id=product.id, shop_id=shop.id, **kwargs)
    return factory


@pytest.fixture
def user(db, client, django_user_model):
    data = {
        "email": "egg@mail.com",
        "password": "egg1988Y"
    }
    user = django_user_model.objects.create_user(email=data['email'], password=data['password'])
    client.force_login(user)
    return user


@pytest.fixture
def token(db, client, user):
    Token.objects.create(user=user)
    token = Token.objects.get(user=user)
    return token


@pytest.fixture
def auth_client(db, client, user, token):

    client.force_authenticate(user=user, token=token)
    return client


@pytest.fixture
def user_partner(db, client, django_user_model):
    data = {
        "email": "partner_test@mail.com",
        "password": "egg1988Y",
        "type": "shop",
    }
    user_partner = django_user_model.objects.create_user(
        email=data['email'],
        password=data['password'],
        type=data['type']
    )
    client.force_login(user_partner)
    return user_partner


@pytest.fixture
def partner_token(db, client, user_partner):
    Token.objects.create(user=user_partner)
    partner_token = Token.objects.get(user=user_partner)
    return partner_token


@pytest.fixture
def auth_partner(db, client, user_partner, partner_token):
    client.force_authenticate(user=user_partner, token=partner_token)
    return client


@pytest.fixture
def shop_factory(user_partner):
    def factory(**kwargs):
        return baker.make('Shop', user=user_partner, **kwargs)
    return factory














