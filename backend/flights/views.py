from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Flight, Booking
from .serializers import FlightSerializer, BookingSerializer

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        queryset = Flight.objects.all()
        departure_city = request.query_params.get('departure_city')
        destination_city = request.query_params.get('destination_city')
        departure_date = request.query_params.get('departure_date')

        if departure_city:
            queryset = queryset.filter(departure_city__icontains=departure_city)
        if destination_city:
            queryset = queryset.filter(destination_city__icontains=destination_city)
        if departure_date:
            queryset = queryset.filter(departure_time__date=departure_date)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        flight_id = request.data.get('flight')
        seat_class = request.data.get('seat_class')
        seat_count = int(request.data.get('seat_count', 1))

        try:
            flight = Flight.objects.get(id=flight_id)
        except Flight.DoesNotExist:
            return Response({'error': 'Flight not found.'}, status=status.HTTP_404_NOT_FOUND)

        if seat_class == 'economy':
            if flight.economy_seats >= seat_count:
                flight.economy_seats -= seat_count
            else:
                return Response({'error': 'Not enough economy seats available.'}, status=status.HTTP_400_BAD_REQUEST)
        elif seat_class == 'first_class':
            if flight.first_class_seats >= seat_count:
                flight.first_class_seats -= seat_count
            else:
                return Response({'error': 'Not enough first class seats available.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid seat class.'}, status=status.HTTP_400_BAD_REQUEST)

        flight.save()

        user_id = request.data.get('user')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        booking = Booking.objects.create(
            user=user,
            flight=flight,
            seat_class=seat_class,
            seat_count=seat_count
        )
        serializer = self.get_serializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        try:
            booking = self.get_object()
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)

        flight = booking.flight
        seat_class = booking.seat_class
        seat_count = booking.seat_count

        if seat_class == 'economy':
            flight.economy_seats += seat_count
        elif seat_class == 'first_class':
            flight.first_class_seats += seat_count
        
        flight.save()
        booking.delete()

        return Response({'message': 'Booking canceled successfully.'}, status=status.HTTP_204_NO_CONTENT)
