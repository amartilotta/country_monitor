import requests

from apps.country.models import Country, Location, NativeName
from apps.country.serializer import (
    CountrySerializer,
    LocationSerializer,
    NativeNameSerializer,
)
from config import settings
from utils.custom_response import get_error_response

class CountryService:

    @classmethod
    def fetch_countries(self) -> dict:
        """
        Fetches all countries from the external API and processes them.

        :return: A dictionary containing the status code, a success message, and a list of errors if any.
        :raises RuntimeError: If the country API URL is disabled (Service Unavailable).
        :raises Exception: If there is an error fetching or processing the countries.
        """
        url = f"{settings.API_COUNTRY_URL}/all?fields=name,flags,capital,population,continents,timezones,area,latlng"
        errors = []
        processed_count = 0

        try:
            response = requests.get(url)
            if response.status_code == 503:
                raise RuntimeError("The country API URL is disabled (Service Unavailable).")
            response.raise_for_status()
            countries = response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"An error occurred while accessing the country API: {e}")

        for country_data in countries:
            try:
                location_data = {
                    "lat": country_data.get("latlng", [None, None])[0],
                    "lng": country_data.get("latlng", [None, None])[1],
                    "capital": country_data.get("capital", [""])[0],
                    "area": country_data.get("area"),
                    "timezone": country_data.get("timezones", [""])[0],
                    "continent": country_data.get("continents", [""])[0],
                }
                location_serializer = LocationSerializer(data=location_data)
                location_serializer.is_valid(raise_exception=True)
                location, _ = Location.objects.update_or_create(
                    **location_serializer.validated_data
                )

                country_data = {
                    "common_name": country_data["name"]["common"],
                    "official_name": country_data["name"]["official"],
                    "flag_png": country_data["flags"]["png"],
                    "flag_svg": country_data["flags"]["svg"],
                    "flag_alt": country_data["flags"]["alt"],
                    "location": location.id,
                    "population": country_data["population"],
                }
                country_serializer = CountrySerializer(data=country_data)
                country_serializer.is_valid(raise_exception=True)
                Country.objects.update_or_create(**country_serializer.validated_data)

                native_names = country_data["name"].get("nativeName", {})
                for lang_code, names in native_names.items():
                    native_name_data = {
                        "language_code": lang_code,
                        "official": names.get("official", ""),
                        "common": names.get("common", ""),
                    }
                    native_name_serializer = NativeNameSerializer(data=native_name_data)
                    native_name_serializer.is_valid(raise_exception=True)
                    NativeName.objects.update_or_create(
                        **native_name_serializer.validated_data
                    )

                processed_count += 1

            except Exception as e:
                country_name = country_data.get("name", {}).get("common", "Unknown")
                errors.append(f"Error processing country {country_name}: {e}")

        return {
            "status": 207 if errors else 200,
            "message": f"Processed {processed_count} countries successfully.",
            "errors": errors,
        }

    @classmethod
    def get_paginated_countries(self, offset: int = 0, limit: int = 100) -> tuple[list[Country], int]:
        """
        Fetches a paginated list of countries.

        :param offset: The starting index of the pagination.
        :param limit: The maximum number of countries to return.
        :return: A tuple containing the list of countries and the total number of countries.
        :raises Exception: If there is an error fetching the paginated countries.
        """
        try:
            queryset = Country.objects.all()
            total_items = Country.objects.count()
            countries = queryset[offset : offset + limit]
            return countries, total_items
        except Exception as e:
            raise Exception(f"Error fetching paginated countries: {e}")

    @classmethod
    def get_country_id(self, country_id: int) -> Country:
        """
        Fetches a country by its ID.

        :param country_id: The ID of the country to fetch.
        :return: The country object.
        :raises Exception: If the country does not exist or if there is an error fetching the country.
        """
        try:
            return Country.objects.get(id=country_id)
        except Country.DoesNotExist:
            raise Exception(f"Country with id {country_id} does not exist.")
        except Exception as e:
            raise Exception(f"Error fetching country with id {country_id}: {e}")