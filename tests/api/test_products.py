import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN




# товар
# успешное получение списка товаров








#
# # успешное получение карточки товара
# @pytest.mark.django_db
# def test_get_one_product(client, category_factory, product_factory):
#     category = category_factory()
#     # создаём один продукт
#     product = product_factory(category_id=category.id)
#     product_id = product.id
#     # url = reverse("api:product")
#     # совершаем запрос GET к API по URL
#     product_url = reverse('api:product', kwargs={'id': product_id})
#     resp = client.get(product_url)
#     # resp_json = resp.json()
#     resp_text = resp.context
#     assert resp.status_code == HTTP_200_OK
#     # assert resp_json
#     # test_product = resp_json[0]
#     # # проверяем, что вернулся именно тот товар, который запрашивали
#     # assert test_product['name'] == product.title


""" Категория """


# получение списка категорий
@pytest.mark.django_db
def test_get_categories(client, category_factory):
    # создаём категории
    category_factory(make_m2m=True, _quantity=5)
    # совершаем запрос GET к API по URL
    url = reverse("api:categories")
    resp = client.get(url)
    resp_json = resp.json()
    # проверяем код ответа
    assert resp.status_code == HTTP_200_OK
    # проверяем, что вернулось нужное количество категорий
    assert len(resp_json) == 5
