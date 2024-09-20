from django.shortcuts import render
from .models import DatasetPage

def search(request):
    search_query = request.GET.get('query', None)
    datasets = DatasetPage.objects.live()

    # Filtros por ubicación, tamaño, frecuencia, etc.
    if 'location' in request.GET:
        datasets = datasets.filter(location__icontains=request.GET['location'])
    # Agrega más filtros según sea necesario

    return render(request, 'datasets/search_results.html', {
        'search_query': search_query,
        'datasets': datasets,
    })
