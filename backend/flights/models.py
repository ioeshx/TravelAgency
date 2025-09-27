from django.db import models

class Flight(models.Model):
    flight_number = models.CharField(max_length=20, unique=True)
    departure_city = models.CharField(max_length=100)
    destination_city = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    airline = models.CharField(max_length=100)
    aircraft_type = models.CharField(max_length=100)
    economy_seats = models.PositiveIntegerField(default=0)
    economy_price = models.DecimalField(max_digits=10, decimal_places=2)
    first_class_seats = models.PositiveIntegerField(default=0)
    first_class_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.flight_number

class Booking(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat_class = models.CharField(max_length=20, choices=[('economy', 'Economy'), ('first_class', 'First Class')])
    seat_count = models.PositiveIntegerField(default=1)
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.flight.flight_number}'
