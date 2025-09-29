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


    @action(detail=False, methods=['post'])
    def all_bookings(self, request):
        if not self._check_admin(request):
            return Response({'error': 'Admin authentication failed'}, status=status.HTTP_403_FORBIDDEN)

        bookings = Booking.objects.all()
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(detail=False, methods=['post'])
    def search(self, request):
        if not self._check_admin(request):
            return Response({'error': 'Admin authentication failed'}, status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get('user')
        flight_id = request.data.get('flight')
        seat_class = request.data.get('seat_class')
        seat_count = request.data.get('seat_count')

        filters = {}
        if user_id:
            filters['user_id'] = user_id
        if flight_id:
            filters['flight_id'] = flight_id
        if seat_class:
            filters['seat_class'] = seat_class
        if seat_count:
            filters['seat_count'] = seat_count

        bookings = Booking.objects.filter(**filters)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @action(detail=False, methods=['get'])
    def get_empty_seats(self, request):
        flight_number = request.query_params.get('flight_number')
        departure_date = request.query_params.get('departure_date')

        if not flight_number or not departure_date:
            return Response({'error': 'Missing flight_number or departure_date.'}, status=status.HTTP_200_OK)

        flights = Flight.objects.filter(flight_number=flight_number, departure_time__date=departure_date)
        if not flights.exists():
            return Response({'error': 'No matching flight found.'}, status=status.HTTP_200_OK)

        flight = flights.first()
        bookings = Booking.objects.filter(flight=flight)

        # 假定经济舱座位号从1开始，头等舱紧接其后
        total_seats = flight.economy_seats + flight.first_class_seats
        # 计算已被预订的座位数量
        booked_seats = sum([b.seat_count for b in bookings])
        # 所有座位号 1 ~ (已预订+剩余)
        all_seat_count = total_seats
        # 假定已预订座位号为 1 ~ booked_seats，剩余座位号为 booked_seats+1 ~ all_seat_count
        empty_seat_list = list(range(booked_seats + 1, all_seat_count + 1))

        data = {
            'flight_number': flight.flight_number,
            'departure_date': departure_date,
            'seats_left': total_seats,
            'empty_seat_list': empty_seat_list
        }
        return Response(data, status=status.HTTP_200_OK)