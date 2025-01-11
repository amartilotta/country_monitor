import requests

from apps.country.models import Country, Location, NativeName
from apps.country.serializer import (
    CountrySerializer,
    LocationSerializer,
    NativeNameSerializer,
)
from config import settings


class CountryService:

    @classmethod
    def fetch_countries(self):
        try:
            url = f"{settings.API_COUNTRY_URL}/all?fields=name,flags,capital,population,continents,timezones,area,latlng"

            response = requests.get(url)
            countries = response.json()

            for country_data in countries:
                location_serializer = LocationSerializer(
                    data={
                        "lat": country_data["latlng"][0],
                        "lng": country_data["latlng"][1],
                        "capital": (
                            country_data["capital"][0]
                            if country_data["capital"]
                            else ""
                        ),
                        "area": country_data["area"],
                        "timezone": country_data["timezones"][0],
                        "continent": country_data["continents"][0],
                    }
                )
                location_serializer.is_valid(raise_exception=True)
                location, _ = Location.objects.update_or_create(
                    **location_serializer.validated_data
                )

                country_serializer = CountrySerializer(
                    data={
                        "common_name": country_data["name"]["common"],
                        "official_name": country_data["name"]["official"],
                        "flag_png": country_data["flags"]["png"],
                        "flag_svg": country_data["flags"]["svg"],
                        "flag_alt": country_data["flags"]["alt"],
                        "location": location.id,
                        "population": country_data["population"],
                    }
                )
                country_serializer.is_valid(raise_exception=True)
                country, _ = Country.objects.update_or_create(
                    **country_serializer.validated_data
                )

                native_names = country_data["name"]["nativeName"]
                for lang_code, names in native_names.items():
                    native_name_data = {
                        "language_code": lang_code,
                        "official": names["official"],
                        "common": names["common"],
                    }
                    native_name_serializer = NativeNameSerializer(
                        data=native_name_data
                    )
                    native_name_serializer.is_valid(raise_exception=True)
                    native_name, _ = NativeName.objects.update_or_create(
                        language_code=lang_code,
                        defaults=native_name_serializer.validated_data,
                    )
                    country.native_names.add(native_name)
        except Exception as ex:
            print(ex)

    @classmethod
    def get_paginated_countries(self, offset: int = 0, limit: int = 100):
        queryset = Country.objects.all()
        total_items = Country.objects.count()
        countries = queryset[offset : offset + limit]
        return countries, total_items

    @classmethod
    def get_country_id(self, country_id: int) -> Country:
        return Country.objects.get(id=country_id)
