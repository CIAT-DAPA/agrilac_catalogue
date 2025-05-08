from django.shortcuts import render, redirect, get_object_or_404
from .models import DatasetPage
from activity_logs.utils import log_user_activity
import json

def catalogue(request):
    datasets = DatasetPage.objects.live()

    # Obtener las instituciones sin duplicados
    instituciones = set(dataset.institution_related for dataset in datasets if dataset.institution_related)

    # Obtener las palabras clave sin duplicados
    keywords = set()
    for dataset in datasets:
        if dataset.keywords:
            keywords.update(dataset.keywords.split(','))

    # Obtener las ubicaciones sin duplicados
    ubicaciones = set()
    for dataset in datasets:
        if dataset.geo_data.exists():
            for geo in dataset.geo_data.all():
                if geo.region_name and geo.municipality_name:
                    ubicaciones.add(f"{geo.region_name}, {geo.municipality_name}")

    # Obtener las variables sin duplicados
    variables = set()
    for dataset in datasets:
        if dataset.data_dictionary.exists():
            for field in dataset.data_dictionary.all():
                if field.field_name:
                    variables.update(field.field_name.split(','))

    # Obtener las frecuencias de actualización sin duplicados
    frecuencias = set()
    for dataset in datasets:
        if dataset.upload_frequency:
            frecuencias.update(dataset.upload_frequency.split(','))

    return render(request, 'datasets/catalogue.html', {
        'title': 'Catálogo de datos',
        'datasets': datasets,
        'instituciones': instituciones,
        'keywords': keywords,
        'ubicaciones': ubicaciones,
        'variables': variables,
        'frecuencias': frecuencias,
    })


def dataset_detail(request, pk):
    dataset = get_object_or_404(DatasetPage, pk=pk)
    if request.user.is_authenticated:
        log_user_activity(
            user=request.user,
            action="Dataset visto",
            request=request,
            extra_data={
                'Título del dataset': dataset.title,
                'Institución del dataset': dataset.institution_related.name if dataset.institution_related else ''
            }
        )

    # Construir y serializar JSON de geo_data usando el tipo definido en DatasetPage
    geo_list = []
    for geo in dataset.geo_data.all():
        if dataset.geo_type == 'coords':
            geo_list.append({
                "type": "coords",
                "type_temp": dataset.geo_type,
                "latitude": geo.latitude,
                "longitude": geo.longitude,
            })
        else:
            geo_list.append({
                "type": "region",
                "type_temp": dataset.geo_type,
                "region_name": geo.region_name,
                "municipality_name": geo.municipality_name,
            })
    geo_json = json.dumps(geo_list)

    return render(request, 'datasets/dataset_page.html', {
        'page': dataset,
        'geo_json': geo_json,
    })