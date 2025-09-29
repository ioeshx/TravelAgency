from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone
from .models import Flight, Booking
from .serializers import (
    FlightSerializer, BookingSerializer, 
    UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
)
from rest_framework.authtoken.models import Token
from django.contrib.auth import login

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [AllowAny]  # 航班信息可公开查看

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

        queryset = queryset.filter(departure_time__gt=timezone.now())

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]  # 新增：需要认证

    def get_permissions(self):
        """根据不同action设置权限"""
        if self.action in ['all_bookings', 'search', 'get_empty_seats']:
            # 管理功能需要admin验证
            permission_classes = [AllowAny]  # 但通过_check_admin验证
        else:
            # 普通用户功能需要登录
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """新增：数据隔离 - 用户只能看到自己的预订"""
        if self.request.user.is_authenticated:
            return Booking.objects.filter(user=self.request.user)
        return Booking.objects.none()
    
    @transaction.atomic  # 新增：事务保护
    def create(self, request, *args, **kwargs):
        flight_id = request.data.get('flight')
        seat_class = request.data.get('seat_class')
        seat_count = int(request.data.get('seat_count', 1))

        # 新增：预订数量验证
        if seat_count <= 0 or seat_count > 10:
            return Response(
                {'error': 'Invalid seat count. Must be between 1 and 10.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
           # 改进：并发控制
            flight = Flight.objects.select_for_update().get(id=flight_id)
        except Flight.DoesNotExist:
            return Response({'error': 'Flight not found.'}, status=status.HTTP_404_NOT_FOUND)

        # 新增：航班过期检查
        if flight.departure_time <= timezone.now():
            return Response(
                {'error': 'Cannot book expired flights.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
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

        # 改进：使用当前登录用户，不允许指定用户ID
        booking = Booking.objects.create(
            user=request.user,  # 使用request.user而不是request.data.get('user')
            flight=flight,
            seat_class=seat_class,
            seat_count=seat_count
        )

        serializer = self.get_serializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @transaction.atomic  # 新增：事务保护
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        try:
            booking = self.get_object()
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)

         # 新增：24小时内不能取消的限制
        if booking.flight.departure_time <= timezone.now() + timezone.timedelta(hours=24):
            return Response(
                {'error': 'Cannot cancel booking within 24 hours of departure.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 改进：并发控制
        flight = Flight.objects.select_for_update().get(id=booking.flight.id)
        seat_class = booking.seat_class
        seat_count = booking.seat_count

        if seat_class == 'economy':
            flight.economy_seats += seat_count
        elif seat_class == 'first_class':
            flight.first_class_seats += seat_count
        
        flight.save()
        booking.delete()

        return Response({'message': 'Booking canceled successfully.'}, status=status.HTTP_200_OK)

    def _check_admin(self, request):
        """你需要提供这个方法的实现"""
        # 这里需要你提供原有的admin验证逻辑
        # 临时实现（你需要替换为真正的逻辑）：
        from django.conf import settings
        username = request.data.get('username')
        password = request.data.get('password')
        return (username == getattr(settings, 'ADMIN_USERNAME', 'admin') and 
                password == getattr(settings, 'ADMIN_PASSWORD', '123456'))

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

class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    
    def get_permissions(self):
        if self.action in ['register', 'login']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserProfileSerializer(user).data,
                'token': token.key,
                'message': 'User registered successfully.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserProfileSerializer(user).data,
                'token': token.key,
                'message': 'Login successful.'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        if request.user.is_authenticated:
            try:
                request.user.auth_token.delete()
            except:
                pass
        return Response({'message': 'Logout successful.'})

    @action(detail=False, methods=['get'])
    def profile(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)