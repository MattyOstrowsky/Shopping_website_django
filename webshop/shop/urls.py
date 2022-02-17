from django import views
from django.urls import path
from shop import views

urlpatterns = [
    path('', views.getProducts, name="Products"),
    path('<str:pk>/', views.getProduct, name="Product"),
]
