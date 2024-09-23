from django.shortcuts import render
from .models import DatasetPage

def catalogue(request):
    datasets = DatasetPage.objects.live()

    return render(request, 'datasets/catalogue.html', {
        'datasets': datasets,
    })
