# Generated by Django 4.2.3 on 2023-10-10 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UrlMapper",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("url", models.URLField()),
                ("short_path", models.CharField(max_length=6, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("hits", models.PositiveBigIntegerField(default=0)),
            ],
        ),
    ]