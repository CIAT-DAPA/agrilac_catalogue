import django_filters
from .models import Dataset

class DatasetFilter(django_filters.FilterSet):
    type_dataset = django_filters.CharFilter(field_name='type_dataset', lookup_expr='iexact')
    start_date = django_filters.DateFilter(field_name='start_date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='end_date', lookup_expr='lte')
    keywords = django_filters.CharFilter(field_name='keywords', lookup_expr='icontains')
    
    class Meta:
        model = Dataset
        fields = ['type_dataset', 'start_date', 'end_date', 'keywords']