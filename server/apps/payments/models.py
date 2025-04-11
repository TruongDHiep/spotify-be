from django.db import models
from apps.users.models import User

# Create your models here.
class Payment(models.Model):
    STATUS_CHOICES = [('success', 'Success'), ('pending', 'Pending'), ('failed', 'Failed')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    pay_date = models.DateField()
    expr_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)