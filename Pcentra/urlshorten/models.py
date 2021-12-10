from django.db import models
import base64
from django.db import transaction
from secrets import token_urlsafe
# Create your models here.


class UrlMapper(models.Model):

    url = models.URLField()

    def _generate_rand_str():
        len_of_str = 5
        res_str = "token_urlsafe(len_of_str)12"
        return res_str

    short_path = models.CharField(default=_generate_rand_str, max_length=6, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    hits = models.PositiveBigIntegerField(default=0)
