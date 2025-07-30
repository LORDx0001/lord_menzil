from django.urls import path
from .views import product_list, product_create, product_update

urlpatterns = [
    path('products/', product_list, name='products-list'),
    path('products/create/', product_create, name='products-create'),
    path('products/<int:pk>/update/', product_update, name='products-update'),
]
