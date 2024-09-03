from django.db import models
from django.contrib.auth.models import User

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, FieldRowPanel, InlinePanel
from modelcluster.fields import ParentalKey
from wagtail.fields import RichTextField


class HomePage(Page):
    pass

class InstitutionPage(Page):
    verified = models.BooleanField(default=False)
    owner_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='owners')
    description = RichTextField(blank=True)
    email = models.EmailField(max_length=254, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('verified'),
        FieldPanel('owner_user'),
        FieldPanel('description'),
        FieldPanel('email'),
        FieldPanel('phone'),
    ]

    def __str__(self):
        return self.title
    

class DatasetPage(Page):
    TYPE_DATASET_CHOICES = [
        ('public', 'Público'),
        ('restricted', 'Restringido'),
    ]

    type_dataset = models.CharField(max_length=50, choices=TYPE_DATASET_CHOICES)
    institution_related = models.ForeignKey('InstitutionPage', on_delete=models.SET_NULL, null=True, blank=True, related_name='datasets')
    description = RichTextField()

    # Campos adicionales
    url_dataset = models.URLField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    citation = RichTextField(blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    FREQUENCY_CHOICES = [
        ('hourly', 'Horario'),
        ('daily', 'Diaria'),
        ('monthly', 'Mensual'),
        ('quarterly', 'Trimestral'),
        ('semiannually', 'Semestral'),
    ]
    upload_frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, blank=True)
    keywords = models.TextField(blank=True, help_text="Agregar múltiples palabras clave separadas por comas")

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('type_dataset'),
            FieldPanel('institution_related'),
            FieldPanel('description'),
        ], heading="Información del Dataset"),
        MultiFieldPanel([
            FieldPanel('url_dataset'),
            FieldPanel('location'),
            FieldPanel('citation'),
            FieldRowPanel([
                FieldPanel('start_date'),
                FieldPanel('end_date'),
            ]),
            FieldPanel('upload_frequency'),
            FieldPanel('keywords'),
        ], heading="Detalles del Dataset"),
        InlinePanel('geo_data', label="Datos Geográficos"),
        InlinePanel('additional_info', label="Información Adicional"),
        InlinePanel('data_dictionary', label="Diccionario de Datos"),
    ]

    def __str__(self):
        return self.title


class GeoData(models.Model):
    dataset = ParentalKey(DatasetPage, on_delete=models.CASCADE, related_name='geo_data')
    GEO_TYPE_CHOICES = [
        ('coords', 'Coordenadas geográficas'),
        ('admin_level', 'Nivel administrativo'),
    ]
    geo_type = models.CharField(max_length=50, choices=GEO_TYPE_CHOICES)

    # Campos para Coordenadas geográficas
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    # Campos para Nivel administrativo
    region_name = models.CharField(max_length=100, blank=True)
    municipality_name = models.CharField(max_length=100, blank=True)

    panels = [
        FieldPanel('geo_type'),
        MultiFieldPanel([
            FieldPanel('latitude'),
            FieldPanel('longitude'),
        ], heading="Coordenadas geográficas", classname="geo-coords"),
        MultiFieldPanel([
            FieldPanel('region_name'),
            FieldPanel('municipality_name'),
        ], heading="Nivel administrativo", classname="geo-admin"),
    ]


class AdditionalInfo(models.Model):
    dataset = ParentalKey(DatasetPage, on_delete=models.CASCADE, related_name='additional_info')
    title = models.CharField(max_length=255)
    description = RichTextField()

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
    ]


class DataDictionary(models.Model):
    dataset = ParentalKey(DatasetPage, on_delete=models.CASCADE, related_name='data_dictionary')
    title = models.CharField(max_length=255)
    unit = models.CharField(max_length=100)
    description = RichTextField()

    panels = [
        FieldPanel('title'),
        FieldPanel('unit'),
        FieldPanel('description'),
    ]