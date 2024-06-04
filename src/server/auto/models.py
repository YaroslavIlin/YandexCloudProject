from django.db import models
from django.utils import timezone
from datetime import datetime, time


class Auto(models.Model):
    auto_number = models.CharField(max_length=10, unique=True)
    auto_type = models.CharField(max_length=50)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)

    def is_booked_now(self):
        now = timezone.now()
        reservations = self.reservation_set.all()
        return any(
            timezone.make_aware(timezone.datetime.combine(reservation.rent_start_date, time(12, 0, 0)), timezone.get_current_timezone()) <= now <=
            timezone.make_aware(timezone.datetime.combine(reservation.rent_end_date, time(12, 0, 0)), timezone.get_current_timezone())
            for reservation in reservations
        )

    def __str__(self):
        return self.auto_number
