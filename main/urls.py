from django.urls import path, include

from main import views
from cart.views import AddToCart, CartDetail, CartDeleteItem, OrderCheckout, OrderDetail, OrderList, CartChange, OrderEdit

urlpatterns = [
    path('', views.IndexView.as_view(), name='main'),
    path('items/<str:item_model_name>/<str:item_slug>/', views.ItemDetail.as_view(), name='item_detail'),
    path('items/<str:item_model_name>/', views.ItemList.as_view(), name='items_list'),

    path('cart/change/<str:model_name>/<str:item_slug>/', CartChange.as_view(), name='cart_change_qty'),
    path('cart/delete_item/<int:id>/', CartDeleteItem.as_view(), name='cart_delete_item'),
    path('cart/<str:item_model_name>/<str:item_slug>/', AddToCart.as_view(), name='add_to_cart'),
    path('cart/', CartDetail.as_view(), name='cart'),

    path('orders/', OrderList.as_view(), name='orders_list'),
    path('order/<int:pk>/', OrderDetail.as_view(), name='order_detail'),
    path('order/edit/<int:pk>/', OrderEdit.as_view(), name='order_edit'),
    path('order/checkout/<int:pk>/', OrderCheckout.as_view(), name='order_checkout'),
]
