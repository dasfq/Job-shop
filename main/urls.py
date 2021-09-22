from django.urls import path, include
from main import views

urlpatterns = [
    path('', views.index, name='index'),
    path('items/<str:category_slug>/<str:item_slug>/', views.ItemDetail.as_view(), name='item_detail'),
    # path('items/<str:category_slug>/', views.CategoryDetail.as_view(), name='category_detail'),
    # path('items/<str:category_slug>/', views.ItemList.as_view(), name='items_list'),
    path('items/<str:item_model_name>/', views.ItemList.as_view(), name='items_list'),
]
