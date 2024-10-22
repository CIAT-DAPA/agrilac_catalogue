from rest_framework.response import Response
from rest_framework.views import APIView
from datasets.models import DatasetPage  # Asegúrate de que esta es la ruta correcta
from wagtail.models import Page

class DatasetListAPIView(APIView):
    def get(self, request):
        datasets = DatasetPage.objects.live().values(
            'title', 'type_dataset', 'identifier', 'institution_related__title',
            'description', 'authors', 'file_format', 'version', 'use_license',
            'url_dataset', 'citation', 'partner_institutions', 'start_date',
            'end_date', 'upload_frequency', 'keywords', 'access_instructions', 'geo_type'
        )
        return Response(list(datasets))