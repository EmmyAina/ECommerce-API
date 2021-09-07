from django.contrib import admin
from .models import User, UserBio
# Register your models here.
admin.site.register((User, UserBio))
