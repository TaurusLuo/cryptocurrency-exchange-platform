from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.crypto import get_random_string


class Wallet(models.Model):
    name = models.CharField(max_length=20, blank=True, default="")
    address = models.CharField(max_length=500, blank=True, default="")
    private = models.CharField(max_length=500, blank=True, default="")
    public = models.CharField(max_length=500, blank=True, default="")
    words = models.CharField(max_length=500, blank=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Admin Wallet"

class User(AbstractUser):
    first_name = models.CharField(max_length=200, blank=True, default="")
    last_name = models.CharField(max_length=200, blank=True, default="")
    phone_number  = models.CharField(max_length=20, blank=True, default="")
    wallets = models.ManyToManyField(Wallet) 


class AccessLog(models.Model):
    user = models.ForeignKey(User)
    ip = models.CharField(max_length=500, blank=True, default="")
    device = models.CharField(max_length=500, blank=True, default="")
    time = models.DateTimeField(editable=False)

    def __str__(self):
        return self.user.username+"-"+self.device

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        self.time = timezone.now()
        return super(User, self).save(*args, **kwargs)
