from django.contrib import admin

# Register your models here.

from .models import UrlMapper, UrlMapper2

admin.site.register(UrlMapper)
admin.site.register(UrlMapper2)
