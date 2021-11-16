from django.db import models
import base64

# Create your models here.


class UrlMapper(models.Model):

    url = models.URLField()

    @property
    def short_path_creation(self):
        """
        Create a short Base64 String using the id, hence it will be unique.
        To save processing resources, after one call, it will store the value,
        in the "short_path" field.
        """
        i_short_path = self.short_path

        if i_short_path == "":
            i_id = int(self.pk)
            id_bytes = i_id.to_bytes((i_id.bit_length() + 7) // 8, byteorder="big")
            base64_str = base64.b64encode(id_bytes)
            i_short_path = base64_str.decode()

            self.short_path = i_short_path
            self.save()

        return i_short_path

    short_path = models.CharField(default="", max_length=6)

    created_at = models.DateTimeField(auto_now_add=True)

    hits = models.PositiveBigIntegerField(default=0)

    def increase_hits(self):
        self.hits += 1
        self.save()
