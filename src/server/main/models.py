from django.db import models
from django.urls import reverse


class Reservation(models.Model):
    auto = models.ForeignKey('auto.Auto', on_delete=models.CASCADE)
    tenant = models.ForeignKey('tenant.Tenant', on_delete=models.CASCADE)
    additional = models.TextField(null=True, blank=True)
    rent_start_date = models.DateField()
    rent_end_date = models.DateField()

    def get_absolute_url(self):
        return reverse('reservation_detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.auto.auto_number} | с {self.rent_start_date} до {self.rent_end_date}"
