# Generated by Django 5.0.8 on 2024-09-05 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_remove_datasetpage_keywords_datasetpage_keywords'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geodata',
            name='geo_type',
            field=models.CharField(choices=[('coords', 'Coordenadas geográficas'), ('admin_level', 'Nivel administrativo')], max_length=50, verbose_name='Tipo de dato geográfico'),
        ),
    ]