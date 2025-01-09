from django.db import models

# Create your models here.
class Country(models.Model):
    flag_png = models.URLField(max_length=200)
    flag_svg = models.URLField(max_length=200)
    flag_alt = models.TextField(blank=True, null=True)
    name_common = models.CharField(max_length=255)
    name_official = models.CharField(max_length=255)
    native_name_official = models.CharField(max_length=255)
    native_name_common = models.CharField(max_length=255)
    capital = models.CharField(max_length=255)
    lat = models.FloatField()
    lng = models.FloatField()
    area = models.FloatField()
    population = models.IntegerField()
    timezone = models.CharField(max_length=50)
    continent = models.CharField(max_length=100)

    def __str__(self):
        return self.name_common
