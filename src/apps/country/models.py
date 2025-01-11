from django.db import models

# class Flag(models.Model):
#     png = models.URLField(max_length=200, help_text="URL to the PNG flag image")
#     svg = models.URLField(max_length=200, help_text="URL to the SVG flag image")
#     alt = models.TextField(blank=True, null=True, help_text="Alternative text for the flag")

#     def __str__(self):
#         return self.alt or "Flag"


class Location(models.Model):
    capital = models.CharField(
        max_length=255, help_text="Capital city of the country"
    )
    lat = models.FloatField(help_text="Latitude of the country")
    lng = models.FloatField(help_text="Longitude of the country")
    area = models.FloatField(
        help_text="Area of the country in square kilometers"
    )
    timezone = models.CharField(
        max_length=50, help_text="Timezone of the country"
    )
    continent = models.CharField(
        max_length=100, help_text="Continent where the country is located"
    )

    class Meta:
        unique_together = (("lat", "lng"),)

    def __str__(self):
        return self.capital


class NativeName(models.Model):
    language_code = models.CharField(
        max_length=3, primary_key=True, help_text="ISO 639-1 language code"
    )
    official = models.CharField(
        max_length=255, help_text="Official native name of the country"
    )
    common = models.CharField(
        max_length=255, help_text="Common native name of the country"
    )

    def __str__(self):
        return f"{self.language_code}: {self.common}"


# class Name(models.Model):
#     common = models.CharField(max_length=255, unique=True, help_text="Common name of the country")
#     official = models.CharField(max_length=255, unique=True, help_text="Official name of the country")
#     native_names = models.ManyToManyField(NativeName, help_text="Native names of the country in different languages")

#     def __str__(self):
#         return self.common


class Country(models.Model):
    common_name = models.CharField(
        max_length=255, unique=True, help_text="Common name of the country"
    )
    official_name = models.CharField(
        max_length=255, unique=True, help_text="Official name of the country"
    )
    native_names = models.ManyToManyField(
        NativeName,
        help_text="Native names of the country in different languages",
    )
    flag_png = models.URLField(
        max_length=200, help_text="URL to the PNG flag image"
    )
    flag_svg = models.URLField(
        max_length=200, help_text="URL to the SVG flag image"
    )
    flag_alt = models.TextField(
        blank=True, null=True, help_text="Alternative text for the flag"
    )
    location = models.OneToOneField(
        Location, on_delete=models.CASCADE, related_name="country"
    )
    population = models.IntegerField(help_text="Population of the country")

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.common_name
