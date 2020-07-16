from django.urls import path

from .views import (
    HomePageView, 
    CartPageView,
    CheckoutView,
    ProductListView,
    ProductDetailView,
    CategoryListView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    PaymentView,
    ProfilePageView,

)


app_name = 'shop'

urlpatterns = [

    path('', HomePageView.as_view(), name='home'),
    path('cart/', CartPageView.as_view(), name='cart'),
    path('profile/<pk>/', ProfilePageView.as_view(), name='profile'),
    path('add-to-cart/<slug>', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>', remove_from_cart, name='remove-from-cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('produtc-list/', ProductListView.as_view(), name='products'),
    path('category/<slug:slug>/', CategoryListView.as_view(), name='categories'),
    path('produtc-detail/<slug:slug>/', ProductDetailView.as_view(), name='produtc-detail'), 
    path('remove-item-from-cart/<slug>', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),

]