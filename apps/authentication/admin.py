from django.contrib import admin
from apps.authentication.models import User, AccessLog

admin.site.register(User)
admin.site.register(AccessLog)
# Register your models here.
