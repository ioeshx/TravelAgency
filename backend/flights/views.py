from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Flight, Booking
from .serializers import FlightSerializer, BookingSerializer
import json


def index(request):
    """首页"""
    return render(request, 'index.html')


def flight_search(request):
    """航班查询"""
    if request.method == 'GET':
        departure_city = request.GET.get('departure_city', '')
        arrival_city = request.GET.get('arrival_city', '')
        departure_date = request.GET.get('departure_date', '')
        
        flights = Flight.objects.all()
        
        if departure_city:
            flights = flights.filter(departure_city__icontains=departure_city)
        if arrival_city:
            flights = flights.filter(arrival_city__icontains=arrival_city)
        if departure_date:
            flights = flights.filter(departure_time__date=departure_date)
        
        context = {
            'flights': flights,
            'departure_city': departure_city,
            'arrival_city': arrival_city,
            'departure_date': departure_date,
        }
        return render(request, 'flight_search.html', context)
    
    return render(request, 'flight_search.html')


def flight_list(request):
    """航班列表"""
    flights = Flight.objects.all().order_by('departure_time')
    return render(request, 'flight_list.html', {'flights': flights})


def flight_detail(request, pk):
    """航班详情"""
    flight = get_object_or_404(Flight, pk=pk)
    return render(request, 'flight_detail.html', {'flight': flight})


@login_required
def booking_create(request, flight_id):
    """创建订座"""
    flight = get_object_or_404(Flight, pk=flight_id)
    
    if request.method == 'POST':
        seat_class = request.POST.get('seat_class')
        seat_count = int(request.POST.get('seat_count', 1))
        passenger_name = request.POST.get('passenger_name')
        passenger_id = request.POST.get('passenger_id')
        phone = request.POST.get('phone')
        
        # 检查座位数量
        if seat_class == 'economy':
            available_seats = flight.economy_seats
        elif seat_class == 'business':
            available_seats = flight.business_seats
        elif seat_class == 'first':
            available_seats = flight.first_seats
        else:
            available_seats = 0
        
        # 计算已订座位数
        booked_count = Booking.objects.filter(
            flight=flight, 
            seat_class=seat_class, 
            status='confirmed'
        ).count()
        
        if booked_count + seat_count > available_seats:
            seat_class_display = dict(Booking.SEAT_CLASS_CHOICES).get(seat_class, seat_class)
            messages.error(request, f'{seat_class_display}座位不足！')
            return render(request, 'booking_form.html', {'flight': flight})
        
        # 创建订座记录
        for i in range(seat_count):
            Booking.objects.create(
                user=request.user,
                flight=flight,
                seat_class=seat_class,
                passenger_name=passenger_name,
                passenger_id=passenger_id,
                phone=phone
            )
        
        messages.success(request, '订座成功！')
        return redirect('booking_list')
    
    return render(request, 'booking_form.html', {'flight': flight})


@login_required
def booking_list(request):
    """订座记录列表"""
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_time')
    return render(request, 'booking_list.html', {'bookings': bookings})


@login_required
def booking_cancel(request, pk):
    """取消订座"""
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, '订座已取消！')
        return redirect('booking_list')
    
    return render(request, 'booking_confirm_cancel.html', {'booking': booking})


def user_login(request):
    """用户登录"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, '登录成功！')
            return redirect('index')
        else:
            messages.error(request, '用户名或密码错误！')
    
    return render(request, 'login.html')


def user_register(request):
    """用户注册"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, '两次输入的密码不一致！')
            return render(request, 'register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, '用户名已存在！')
            return render(request, 'register.html')
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        messages.success(request, f'账户 {username} 创建成功！')
        return redirect('login')
    
    return render(request, 'register.html')


def user_logout(request):
    """用户登出"""
    logout(request)
    messages.success(request, '已成功登出！')
    return redirect('index')


# API视图
@csrf_exempt
@api_view(['GET'])
def api_flight_search(request):
    """API: 航班搜索"""
    departure_city = request.GET.get('departure_city', '')
    arrival_city = request.GET.get('arrival_city', '')
    departure_date = request.GET.get('departure_date', '')
    
    flights = Flight.objects.all()
    
    if departure_city:
        flights = flights.filter(departure_city__icontains=departure_city)
    if arrival_city:
        flights = flights.filter(arrival_city__icontains=arrival_city)
    if departure_date:
        flights = flights.filter(departure_time__date=departure_date)
    
    serializer = FlightSerializer(flights, many=True)
    return Response(serializer.data)


@csrf_exempt
@api_view(['GET'])
def api_flight_list(request):
    """API: 航班列表"""
    flights = Flight.objects.all().order_by('departure_time')
    serializer = FlightSerializer(flights, many=True)
    return Response(serializer.data)


@csrf_exempt
@api_view(['GET'])
def api_flight_detail(request, pk):
    """API: 航班详情"""
    flight = get_object_or_404(Flight, pk=pk)
    serializer = FlightSerializer(flight)
    return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def api_booking_create(request):
    """API: 创建订座"""
    try:
        data = request.data
        flight_id = data.get('flight_id')
        seat_class = data.get('seat_class')
        seat_count = int(data.get('seat_count', 1))
        passenger_name = data.get('passenger_name')
        passenger_id = data.get('passenger_id')
        phone = data.get('phone')
        
        flight = get_object_or_404(Flight, pk=flight_id)
        
        # 检查座位数量
        if seat_class == 'economy':
            available_seats = flight.economy_seats
        elif seat_class == 'business':
            available_seats = flight.business_seats
        elif seat_class == 'first':
            available_seats = flight.first_seats
        else:
            return Response({'error': 'Invalid seat class'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 计算已订座位数
        booked_count = Booking.objects.filter(
            flight=flight, 
            seat_class=seat_class, 
            status='confirmed'
        ).count()
        
        if booked_count + seat_count > available_seats:
            return Response({'error': 'No available seats'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 创建订座记录
        bookings = []
        for i in range(seat_count):
            booking = Booking.objects.create(
                user=request.user,
                flight=flight,
                seat_class=seat_class,
                seat_count=1,  # 每个记录代表一个座位
                passenger_name=passenger_name,
                passenger_id=passenger_id,
                phone=phone
            )
            bookings.append(booking)
        
        serializer = BookingSerializer(bookings, many=True)
        return Response({
            'success': True,
            'bookings': serializer.data,
            'total_price': sum(booking.total_price for booking in bookings)
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def api_booking_list(request):
    """API: 订座记录列表"""
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_time')
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)