from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q
from datasets.models import DatasetPage
from .serializers import DatasetPageSerializer

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



class DatasetCreateAPIView(APIView):
    def post(self, request):
        serializer = DatasetPageSerializer(data=request.data)
        if serializer.is_valid():
            dataset = serializer.save()  # Guarda el dataset usando el método create
            return Response({
                'id': dataset.id,
                'title': dataset.title,
                'message': 'Dataset creado exitosamente.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DatasetManageAPIView(APIView):
    def post(self, request):
        serializer = DatasetPageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            dataset = DatasetPage.objects.get(pk=pk)
        except DatasetPage.DoesNotExist:
            return Response({"detail": "Dataset no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DatasetPageSerializer(dataset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            dataset = DatasetPage.objects.get(pk=pk)
            dataset.delete()
            return Response({"detail": "Dataset eliminado correctamente."}, status=status.HTTP_204_NO_CONTENT)
        except DatasetPage.DoesNotExist:
            return Response({"detail": "Dataset no encontrado."}, status=status.HTTP_404_NOT_FOUND)
