# Generated by Django 5.0.8 on 2024-09-03 15:57

import django.db.models.deletion
import modelcluster.fields
import wagtail.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_datasetpage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='institutionpage',
            name='owner_institution',
        ),
        migrations.AddField(
            model_name='datasetpage',
            name='citation',
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='datasetpage',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='datasetpage',
            name='keywords',
            field=models.TextField(blank=True, help_text='Agregar múltiples palabras clave separadas por comas'),
        ),
        migrations.AddField(
            model_name='datasetpage',
            name='location',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='datasetpage',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='datasetpage',
            name='upload_frequency',
            field=models.CharField(blank=True, choices=[('hourly', 'Horario'), ('daily', 'Diaria'), ('monthly', 'Mensual'), ('quarterly', 'Trimestral'), ('semiannually', 'Semestral')], max_length=20),
        ),
        migrations.AddField(
            model_name='datasetpage',
            name='url_dataset',
            field=models.URLField(blank=True, help_text='Solo aparece si el tipo de dataset es Público'),
        ),
        migrations.AddField(
            model_name='institutionpage',
            name='description',
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='institutionpage',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='institutionpage',
            name='owner_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owners', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='institutionpage',
            name='phone',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.CreateModel(
            name='AdditionalInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', wagtail.fields.RichTextField()),
                ('dataset', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='additional_info', to='home.datasetpage')),
            ],
        ),
        migrations.CreateModel(
            name='DataDictionary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('unit', models.CharField(max_length=100)),
                ('description', wagtail.fields.RichTextField()),
                ('dataset', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='data_dictionary', to='home.datasetpage')),
            ],
        ),
        migrations.CreateModel(
            name='GeoData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geo_type', models.CharField(choices=[('coords', 'Coordenadas geográficas'), ('admin_level', 'Nivel administrativo')], max_length=50)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('region_name', models.CharField(blank=True, max_length=100)),
                ('municipality_name', models.CharField(blank=True, max_length=100)),
                ('dataset', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='geo_data', to='home.datasetpage')),
            ],
        ),
    ]