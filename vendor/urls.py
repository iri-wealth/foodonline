from django.urls import path
from . import views
from .models import Vendor


urlpatterns = [
    path('', views.vendorDashboard),
    path('registerVendor/', views.registerVendor, name='registerVendor'),
    path('vendorDashboard/', views.vendorDashboard, name='vendorDashboard'),
    path('vendorProfile/', views.vendorProfile, name='vendorProfile'),
    path('menu_builder/', views.menu_builder, name='menu_builder'),
    path('menu_builder/category/<int:pk>/', views.fooditems_by_category, name='fooditems_by_category'),
    path('vendor_detail/<int:pk>/', views.vendor_detail, name='vendor_detail'),

    #Category CRUD
    path('menu-builder/category/add/', views.add_category, name='add_category'),
    path('menu-builder/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('menu-builder/category/delete/<int:pk>/', views.delete_category, name='delete_category'),

    # FoodItem CRUD
    path('menu-builder/food/add/', views.add_food, name='add_food'),
    path('menu-builder/food/edit/<int:pk>/', views.edit_food, name='edit_food'),
    path('menu-builder/food/delete/<int:pk>/', views.delete_food, name='delete_food'),

]