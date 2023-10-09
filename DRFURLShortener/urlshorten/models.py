from django.db import models
import base64
from django.db import transaction
from secrets import token_urlsafe

# Create your models here.


class UrlMapper(models.Model):
    url = models.URLField()
    short_path = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hits = models.PositiveBigIntegerField(default=0)
