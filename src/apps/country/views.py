from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Country
from .serializer import CountrySerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    # Método personalizado para obtener países por continente
    @action(detail=False, methods=["get"])
    def by_continent(self, request):
        continent = request.query_params.get("continent", None)
        if continent:
            countries = Country.objects.filter(continent=continent)
            serializer = CountrySerializer(countries, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "Continent parameter is required"}, status=400
            )
