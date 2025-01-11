from rest_framework import status
from rest_framework.viewsets import ViewSet
from utils.custom_response import get_success_response, get_error_response

from .serializer import CountryOutputSerializer, PaginationParamsSerializer
from .services import CountryService
from rest_framework.serializers import ValidationError
import logging
from .models import Country

logger = logging.getLogger(__name__)

class CountryViewSet(ViewSet):

    def get_countries(self, request):
        try:
            params_serializer = PaginationParamsSerializer(
                data=request.query_params
            )
            params_serializer.is_valid(raise_exception=True)
            countries, total_items = CountryService.get_paginated_countries(
                **params_serializer.validated_data
            )
            countries_output = CountryOutputSerializer(countries, many=True)
            return get_success_response(
                status=status.HTTP_200_OK,
                countries=countries_output.data,
                total=total_items,
            )
        except ValidationError as ex:
            logger.error(ex)
            return get_error_response(status=status.HTTP_400_BAD_REQUEST, message="Invalid search data", errors=params_serializer.errors)
        except Exception as ex:
            logger.error(ex)
            return get_error_response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_country_by_id(self, request, country_id=None):
        try:
            country = CountryService.get_country_id(country_id)
            country_output = CountryOutputSerializer(country)
            return get_success_response(
                status=status.HTTP_200_OK, country=country_output.data
            )
        except Country.DoesNotExist as ex:
            logger.error(ex)
            return get_error_response(status=status.HTTP_404_NOT_FOUND, message=f"Country with id {country_id} not found")
        except Exception as ex:
            logger.exception(ex)
            return get_error_response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

