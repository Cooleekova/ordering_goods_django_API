import requests
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import JsonResponse
from django.shortcuts import render
from yaml import load as load_yaml, Loader

from distutils.util import strtobool
from django.db.models import Sum, F
from rest_framework.response import Response

from rest_framework import permissions
from api.models import Order
from api.permissions import IsShop
from api.serializers import ShopSerializer, OrderSerializer
from api.models import Shop, ProductInfo, Product, Parameter, ProductParameter, Category


class PartnerUpdate(GenericAPIView):
    """ Класс для обновления прайса от поставщика """

    permission_classes = (permissions.IsAuthenticated, IsShop, )
    serializer_class = ShopSerializer

    def post(self, request, *args, **kwargs):

        url = request.data.get('url')
        print(url)
        if url:
            validate_url = URLValidator()
            try:
                validate_url(url)
            except ValidationError as e:
                return JsonResponse({'Status': False, 'Error': str(e)})
            else:
                stream = requests.get(url).text

                data = load_yaml(stream, Loader=Loader)

                shop, _ = Shop.objects.get_or_create(name=data['shop'], user_id=request.user.id)
                for category in data['categories']:
                    category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
                    category_object.shops.add(shop.id)
                    category_object.save()
                ProductInfo.objects.filter(shop_id=shop.id).delete()
                for item in data['goods']:
                    product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])

                    product_info = ProductInfo.objects.create(product_id=product.id,
                                                              external_id=item['id'],
                                                              model=item['model'],
                                                              price=item['price'],
                                                              price_rrc=item['price_rrc'],
                                                              quantity=item['quantity'],
                                                              shop_id=shop.id)
                    for name, value in item['parameters'].items():
                        parameter_object, _ = Parameter.objects.get_or_create(name=name)
                        ProductParameter.objects.create(product_info_id=product_info.id,
                                                        parameter_id=parameter_object.id,
                                                        value=value)

                return JsonResponse({'Status': True})

        return JsonResponse({'Status': False, 'Error': 'Не указаны все необходимые аргументы'})


class PartnerState(GenericAPIView):
    """
    Класс для работы со статусом поставщика
    """

    permission_classes = (permissions.IsAuthenticated, IsShop,)
    serializer_class = ShopSerializer

    def get(self, request, *args, **kwargs):
        """ Метод для получения текущего статуса поставщика """

        shop = request.user.shop
        serializer = ShopSerializer(shop)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """ Метод для изменения статуса поставщика """

        state = request.data.get('state')
        if state:
            try:
                Shop.objects.filter(user_id=request.user.id).update(state=strtobool(state))
                return JsonResponse({'Status': True})
            except ValueError as error:
                return JsonResponse({'Status': False, 'Errors': str(error)})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class PartnerOrders(GenericAPIView):
    """
    Класс для получения заказов поставщиками
    """
    permission_classes = (permissions.IsAuthenticated, IsShop,)
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):

        order = Order.objects.filter(
            ordered_items__product_info__shop_id=request.user.shop.id).exclude(
            status='basket'
        ).prefetch_related(
            'ordered_items__product_info__product__category',
            'ordered_items__product_info__product_parameters__parameter').select_related('contact').annotate(
            total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))).distinct()

        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)
