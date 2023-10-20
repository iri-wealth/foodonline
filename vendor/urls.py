from django.urls import path
from . import views


urlpatterns = [
    path('', views.vendorDashboard),
    path('registerVendor/', views.registerVendor, name='registerVendor'),
    path('vendorDashboard/', views.vendorDashboard, name='vendorDashboard'),
    path('vendorProfile/', views.vendorProfile, name='vendorProfile'),
]