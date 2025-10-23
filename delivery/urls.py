from django.urls import path
from . import views
from django.shortcuts import render
 
urlpatterns = [
    # Home and authentication paths
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.handle_login, name='handle_login'),
    path('signup/submit/', views.handle_signup, name='handle_signup'),
    path('admin/home/', views.admin_home, name='admin_home'),
    path('customer/<str:username>/home/', views.customer_home, name='customer_home'),

    # Restaurant-related paths
    path('restaurants/add', views.add_restaurant_page, name='add_restaurant_page'),
    path('restaurants/', views.show_restaurant_page, name='show_restaurant_page'),
    path('restaurants/add/', views.add_restaurant, name='add_restaurant'),
    path('restaurants/<int:restaurant_id>/menu/', views.restaurant_menu, name='restaurant_menu'),
    path('restaurants/<int:restaurant_id>/update/', views.update_restaurant, name='update_restaurant'),
    path('restaurants/<int:restaurant_id>/update/page/', views.update_restaurant_page, name='update_restaurant_page'),
    path('restaurants/<int:restaurant_id>/delete/', views.delete_restaurant, name='delete_restaurant'),

    path('menu/<int:menuItem_id>/update/', views.update_menuItem, name='update_menuItem'),
    path('menu/<int:menuItem_id>/update/page/', views.update_menuItem_page, name='update_menuItem_page'),
    path('menu/<int:menuItem_id>/delete/', views.delete_menuItem, name='delete_menuItem'),

    path('restaurants/<int:restaurant_id>/menu/customer/<str:username>/', views.customer_menu, name='customer_menu'),
    path('cart/<str:username>/', views.show_cart_page, name='show_cart_page'),
    path('cart/<int:item_id>/add/<str:username>/', views.add_to_cart, name='add_to_cart'),
    path('cart/<int:item_id>/remove/<str:username>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/<int:item_id>/update/<str:username>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/clear/<str:username>/', views.clear_cart, name='clear_cart'),

    path('checkout/<str:username>/', views.checkout, name='checkout'),

    path('orders/<str:username>/', views.orders, name='orders'),
    
    # Debug route
    path('debug-cart/', lambda request: render(request, 'delivery/debug_cart.html'), name='debug_cart'),


]
