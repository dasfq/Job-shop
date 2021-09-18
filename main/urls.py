from django.urls import path, include
from main import views


urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:pk>/', views.ItemList.as_view(), name='category')
]