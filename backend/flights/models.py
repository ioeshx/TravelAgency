from django.db import models
from django.contrib.auth.models import User

class Flight(models.Model):
    flight_number = models.CharField(max_length=20, unique=True)
    departure_city = models.CharField(max_length=100)
    arrival_city = models.CharField(max_length=100)  # 统一字段名
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    airline = models.CharField(max_length=100)
    aircraft_type = models.CharField(max_length=100)
    economy_seats = models.PositiveIntegerField(default=0)
    business_seats = models.PositiveIntegerField(default=0)  # 添加商务舱
    first_seats = models.PositiveIntegerField(default=0)  # 统一字段名
    economy_price = models.DecimalField(max_digits=10, decimal_places=2)
    business_price = models.DecimalField(max_digits=10, decimal_places=2)  # 添加商务舱价格
    first_price = models.DecimalField(max_digits=10, decimal_places=2)  # 统一字段名

    def __str__(self):
        return self.flight_number

class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', '已确认'),
        ('cancelled', '已取消'),
        ('pending', '待确认'),
    ]
    
    SEAT_CLASS_CHOICES = [
        ('economy', '经济舱'),
        ('business', '商务舱'),
        ('first', '头等舱'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat_class = models.CharField(max_length=20, choices=SEAT_CLASS_CHOICES)
    seat_count = models.PositiveIntegerField(default=1)
    passenger_name = models.CharField(max_length=100)  # 添加乘客姓名
    passenger_id = models.CharField(max_length=18)  # 添加身份证号
    phone = models.CharField(max_length=20)  # 添加联系电话
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    booking_time = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        """计算总价格"""
        if self.seat_class == 'economy':
            return self.flight.economy_price * self.seat_count
        elif self.seat_class == 'business':
            return self.flight.business_price * self.seat_count
        elif self.seat_class == 'first':
            return self.flight.first_price * self.seat_count
        return 0

    def __str__(self):
        return f'{self.user.username} - {self.flight.flight_number}'
