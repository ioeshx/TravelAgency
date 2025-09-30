from django.urls import path
from . import views

urlpatterns = [
    # 首页
    path('', views.index, name='index'),
    
    # 航班相关
    path('flights/', views.flight_list, name='flight_list'),
    path('flights/search/', views.flight_search, name='flight_search'),
    path('flights/<int:pk>/', views.flight_detail, name='flight_detail'),
    
    # 订座相关
    path('flights/<int:flight_id>/booking/', views.booking_create, name='booking_create'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:pk>/cancel/', views.booking_cancel, name='booking_cancel'),
    
    # 用户认证
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    
    # API接口
    path('api/flights/', views.api_flight_list, name='api_flight_list'),
    path('api/flights/search/', views.api_flight_search, name='api_flight_search'),
    path('api/flights/<int:pk>/', views.api_flight_detail, name='api_flight_detail'),
    path('api/bookings/', views.api_booking_list, name='api_booking_list'),
    path('api/bookings/create/', views.api_booking_create, name='api_booking_create'),
]