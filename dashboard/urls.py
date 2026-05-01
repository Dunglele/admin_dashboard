from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard_view, name='dashboard'),
    path('categories/', views.categories_view, name='categories'),
    path('products/', views.products_view, name='products'),
    path('orders/', views.orders_view, name='orders'),
    path('users/', views.users_view, name='users'),
]
