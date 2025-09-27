from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlightViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'flights', FlightViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
