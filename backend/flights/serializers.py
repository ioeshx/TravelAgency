from rest_framework import serializers
from .models import Flight, Booking

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    flight_number = serializers.CharField(source='flight.flight_number', read_only=True)
    departure_city = serializers.CharField(source='flight.departure_city', read_only=True)
    arrival_city = serializers.CharField(source='flight.arrival_city', read_only=True)
    departure_time = serializers.DateTimeField(source='flight.departure_time', read_only=True)
    arrival_time = serializers.DateTimeField(source='flight.arrival_time', read_only=True)
    airline = serializers.CharField(source='flight.airline', read_only=True)
    total_price = serializers.ReadOnlyField()
    
    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'flight', 'seat_class', 'seat_count', 
            'passenger_name', 'passenger_id', 'phone', 'status', 
            'booking_time', 'flight_number', 'departure_city', 
            'arrival_city', 'departure_time', 'arrival_time', 
            'airline', 'total_price'
        ]
