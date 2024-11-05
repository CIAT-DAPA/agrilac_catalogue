from rest_framework import serializers
from datasets.models import DatasetPage

class DatasetPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetPage
        fields = [
            'title', 'type_dataset', 'identifier', 'institution_related',
            'description', 'authors', 'file_format', 'version', 'use_license',
            'url_dataset', 'citation', 'partner_institutions', 'start_date',
            'end_date', 'upload_frequency', 'keywords', 'access_instructions', 'geo_type'
        ]

    def create(self, validated_data):
        # Aquí puedes manejar la creación y evitar campos no deseados
        dataset_page = DatasetPage(**validated_data)
        dataset_page.save()  # Esto permitirá que Wagtail maneje `path` y `depth`
        return dataset_page
