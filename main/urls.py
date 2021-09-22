from django.urls import path, include

from main import views
from cart.views import OrderCreate, AddToCart, CartDetail

urlpatterns = [
    path('', views.IndexView.as_view(), name='main'),
    path('items/<str:item_model_name>/<str:item_slug>/', views.ItemDetail.as_view(), name='item_detail'),
    path('items/<str:item_model_name>/', views.ItemList.as_view(), name='items_list'),

    path('cart/<str:item_model_name>/<str:item_slug>/', AddToCart.as_view(), name='add_to_cart'),
    path('cart/', CartDetail.as_view(), name='cart'),
    path('order/create/', OrderCreate.as_view(), name='order_create'),
]
