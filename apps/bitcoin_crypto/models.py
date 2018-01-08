from apps.authentication.models import User
from django.db import models

class Transaction(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    from_currency = models.CharField(blank=False, max_length=10)
    to_currency = models.CharField(blank=False, max_length=10)
    amount = models.CharField(blank=False, max_length=200)
    transaction_id = models.CharField(blank=True, max_length=200)
    transaction_from = models.CharField(blank=True, max_length=200)
    transaction_to = models.CharField(blank=True, max_length=200)

    def __str__(self):
        return self.user.username