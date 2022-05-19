from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model

from users.models import Skills

user=get_user_model()

admin.site.register(user)
admin.site.register(Skills)