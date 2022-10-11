from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import user_views, orders_views, partner_views, products_views


app_name = 'api'

router = DefaultRouter()

router.register('contacts', user_views.ContactViewSet)
router.register('user', user_views.AccountDetailsViewSet)

urlpatterns = [
    path('partner/update', partner_views.PartnerUpdate.as_view(), name='partner-update'),
    path('partner/state', partner_views.PartnerState.as_view(), name='partner-state'),
    path('partner/orders', partner_views.PartnerOrders.as_view(), name='partner-orders'),

    path('products/', products_views.ProductInfoView.as_view(), name='products'),
    path('product/<int:id>', products_views.ProductView.as_view(), name='product'),


    path('basket/', orders_views.BasketView.as_view(), name='basket'),
    path('order', orders_views.OrderView.as_view(), name='order'),

    path('user/register', user_views.RegisterAccount.as_view(), name='signup'),
    path('user/register/confirm', user_views.ConfirmAccount.as_view(), name='confirm-account'),

    # path('user/details', user_views.AccountDetails.as_view(), name='user-details'),

    path('categories', products_views.CategoryView.as_view(), name='categories'),
    path('shops', products_views.ShopView.as_view(), name='shops'),



]
