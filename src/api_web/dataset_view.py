from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q

from datasets.models import DatasetPage  

class DatasetListAPIView(APIView):
    def get(self, request):
        datasets = DatasetPage.objects.live().values(
            'title', 'type_dataset', 'identifier', 'institution_related__title',
            'description', 'authors', 'file_format', 'version', 'use_license',
            'url_dataset', 'citation', 'partner_institutions', 'start_date',
            'end_date', 'upload_frequency', 'keywords', 'access_instructions', 'geo_type'
        )
        return Response(list(datasets))
    
class DatasetDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            dataset = DatasetPage.objects.live().values(
                'title', 'type_dataset', 'identifier', 'institution_related__title',
                'description', 'authors', 'file_format', 'version', 'use_license',
                'url_dataset', 'citation', 'partner_institutions', 'start_date',
                'end_date', 'upload_frequency', 'keywords', 'access_instructions', 'geo_type'
            ).get(pk=pk)
            return Response(dataset)
        except DatasetPage.DoesNotExist:
            return Response({"detail": "Dataset no encontrado."}, status=status.HTTP_404_NOT_FOUND)

class DatasetSearchAPIView(APIView):
    def get(self, request):
        title = request.query_params.get('title', None)
        type_dataset = request.query_params.get('type_dataset', None)
        institution = request.query_params.get('institution', None)

        filters = Q()
        if title:
            filters &= Q(title__icontains=title)
        if type_dataset:
            filters &= Q(type_dataset__iexact=type_dataset)
        if institution:
            filters &= Q(institution_related__title__icontains=institution)

        datasets = DatasetPage.objects.live().filter(filters).values(
            'title', 'type_dataset', 'identifier', 'institution_related__title',
            'description', 'authors', 'file_format', 'version', 'use_license',
            'url_dataset', 'citation', 'partner_institutions', 'start_date',
            'end_date', 'upload_frequency', 'keywords', 'access_instructions', 'geo_type'
        )
        return Response(list(datasets))
