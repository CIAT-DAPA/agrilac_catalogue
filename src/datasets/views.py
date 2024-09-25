from django.shortcuts import render
from .models import DatasetPage

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
                if geo.region_name:
                    ubicaciones.update(geo.region_name.split(','))

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
