from rest_framework import serializers


class LocationSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()
    capital = serializers.CharField(default="", allow_blank=True)
    area = serializers.FloatField()
    timezone = serializers.CharField()
    continent = serializers.CharField()


class CountrySerializer(serializers.Serializer):
    common_name = serializers.CharField()
    official_name = serializers.CharField()
    flag_png = serializers.CharField()
    flag_svg = serializers.CharField()
    flag_alt = serializers.CharField(allow_null=True, allow_blank=True)
    location = serializers.IntegerField()
    population = serializers.IntegerField()


class NativeNameSerializer(serializers.Serializer):
    language_code = serializers.CharField()
    official = serializers.CharField()
    common = serializers.CharField()


class CountryOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    common_name = serializers.CharField()
    official_name = serializers.CharField()
    native_names = NativeNameSerializer(many=True)
    flag_png = serializers.CharField()
    flag_svg = serializers.CharField()
    flag_alt = serializers.CharField(allow_null=True, allow_blank=True)
    location = serializers.CharField()
    population = serializers.IntegerField()


class PaginationParamsSerializer(serializers.Serializer):
    offset = serializers.IntegerField(required=False, default=0)
    limit = serializers.IntegerField(required=False, default=100)
