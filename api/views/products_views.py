from django.db.models import Q
from django.http import Http404
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Shop, Category, ProductInfo, Product
from api.permissions import IsAdminOrReadOnly
from api.serializers import CategorySerializer, ShopSerializer, ProductInfoSerializer, ProductSerializer


class CategoryView(ListAPIView):
    """
    Класс для просмотра категорий
    """
    permission_classes = (IsAdminOrReadOnly, )
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ShopView(ListAPIView):
    """
    Класс для просмотра списка магазинов
    """
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Shop.objects.filter(state=True)
    serializer_class = ShopSerializer


class ProductInfoView(GenericAPIView):
    """
        Класс для поиска товаров
    """
    permission_classes = (IsAdminOrReadOnly,)
    template_name = 'api/product_list.html'
    renderer_classes = (TemplateHTMLRenderer,)
    serializer_class = ProductInfoSerializer

    def get(self, request, *args, **kwargs):

        query = Q(shop__state=True)
        shop_id = request.query_params.get('shop_id')
        category_id = request.query_params.get('category_id')

        if shop_id:
            query = query & Q(shop_id=shop_id)

        if category_id:
            query = query & Q(product__category_id=category_id)

        # фильтруем и отбрасываем дуликаты
        queryset = ProductInfo.objects.filter(
            query).select_related(
            'shop', 'product__category').prefetch_related(
            'product_parameters__parameter').distinct()

        return Response({'context': queryset}, template_name=self.template_name)


class ProductView(GenericAPIView):
    """
        Карточка товара
    """
    permission_classes = (IsAdminOrReadOnly,)
    template_name = 'api/product.html'
    renderer_classes = (TemplateHTMLRenderer, )
    serializer_class = ProductSerializer

    def get(self, request, id, *args, **kwargs):
        query = Q(category__shops__state=True)
        product_id = id
        query = query & Q(id=product_id)

        # фильтруем и отбрасываем дубликаты
        queryset = Product.objects.filter(query).prefetch_related('category__shops').distinct()

        # queryset = ProductInfo.objects.filter(query).\
        #     select_related('shop', 'product', 'product__category').\
        #     prefetch_related('product_parameters__parameter').distinct()

        if queryset:
            return Response({'context': queryset}, template_name=self.template_name)
        else:
            raise Http404


