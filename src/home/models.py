from django import forms
from django.db import models
from django.contrib.auth.models import User

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, FieldRowPanel, InlinePanel
from modelcluster.fields import ParentalKey
from wagtail.fields import RichTextField
from django.utils.translation import gettext_lazy as _


class HomePage(Page):
    pass

class InstitutionPage(Page):
    verified = models.BooleanField(default=False, verbose_name=_("Verificado"))
    owner_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='owners', verbose_name=_("Representante principal"))
    description = RichTextField(blank=True, verbose_name=_("Descripción"))
    email = models.EmailField(max_length=254, blank=True, verbose_name=_("Email"))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_("Teléfono"))

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

    type_dataset = models.CharField(max_length=50, choices=TYPE_DATASET_CHOICES, verbose_name=_("Acceso"))
    institution_related = models.ForeignKey('InstitutionPage', on_delete=models.SET_NULL, null=True, blank=True, related_name='datasets', verbose_name=_("Institución"))
    description = RichTextField(verbose_name=_("Descripción"))

    # Campos adicionales
    url_dataset = models.URLField(blank=True, verbose_name=_("URL del dataset"))
    location = models.CharField(max_length=255, blank=True, verbose_name=_("Ubicación"))
    citation = RichTextField(blank=True, verbose_name=_("Citación"))
    start_date = models.DateField(blank=True, null=True, verbose_name=_("Fecha de inicio"))
    end_date = models.DateField(blank=True, null=True, verbose_name=_("Fecha de fin"))
    FREQUENCY_CHOICES = [
        ('hourly', 'Horario'),
        ('daily', 'Diaria'),
        ('monthly', 'Mensual'),
        ('quarterly', 'Trimestral'),
        ('semiannually', 'Semestral'),
    ]
    upload_frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, blank=True, verbose_name=_("Frecuencia de subida"))
    
    # Lista de palabras clave
    KEYWORDS_CHOICES = [
        ('clima', 'Clima'),
        ('cultivos', 'Cultivos'),
        ('temperatura', 'Temperatura'),
        ('precipitacion', 'Precipitación'),
        ('humedad', 'Humedad'),
        ('evapotranspiracion', 'Evapotranspiración'),
        ('radiacion_solar', 'Radiación Solar'),
        ('productividad_agricola', 'Productividad Agrícola'),
        ('fenologia', 'Fenología'),
        ('pronosticos_meteorologicos', 'Pronósticos Meteorológicos'),
        ('cambio_climatico', 'Cambio Climático'),
        ('suelos', 'Suelos'),
        ('biodiversidad', 'Biodiversidad'),
        ('modelos_climaticos', 'Modelos Climáticos'),
        ('manejo_agua', 'Manejo de Agua'),
        ('variabilidad_climatica', 'Variabilidad Climática'),
        ('resiliencia_agricola', 'Resiliencia Agrícola'),
        ('riesgos_climaticos', 'Riesgos Climáticos'),
        ('adaptacion_clima', 'Adaptación al Clima'),
        ('indices_climaticos', 'Índices Climáticos'),
        ('escenarios_climaticos', 'Escenarios Climáticos'),
        ('monitoreo_climatico', 'Monitoreo Climático'),
        ('agricultura_sostenible', 'Agricultura Sostenible'),
        ('agroecologia', 'Agroecología'),
        ('seguridad_alimentaria', 'Seguridad Alimentaria'),
        ('agroforesteria', 'Agroforestería'),
        ('tecnologia_agricola', 'Tecnología Agrícola'),
        ('datos_satelitales', 'Datos Satelitales'),
        ('gis', 'GIS'),
        ('sensores_remotos', 'Sensores Remotos'),
        ('estaciones_meteorologicas', 'Estaciones Meteorológicas'),
    ]
    
    keywords = models.CharField(max_length=255, choices=KEYWORDS_CHOICES, blank=True, verbose_name=_("Palabras clave"))

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
            FieldPanel('keywords', widget=forms.CheckboxSelectMultiple),
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
    latitude = models.FloatField(blank=True, null=True, verbose_name=_("Latitud"))
    longitude = models.FloatField(blank=True, null=True, verbose_name=_("Longitud"))

    # Campos para Nivel administrativo
    region_name = models.CharField(max_length=100, blank=True, verbose_name=_("Nombre región"))
    municipality_name = models.CharField(max_length=100, blank=True, verbose_name=_("Nombre municipalidad"))

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
    title = models.CharField(max_length=255, verbose_name=_("Título"))
    description = RichTextField(verbose_name=_("Descripción"))

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
    ]


class DataDictionary(models.Model):
    dataset = ParentalKey(DatasetPage, on_delete=models.CASCADE, related_name='data_dictionary')
    title = models.CharField(max_length=255, verbose_name=_("Título"))
    unit = models.CharField(max_length=100, verbose_name=_("Unidad"))
    description = RichTextField(verbose_name=_("Descripción"))

    panels = [
        FieldPanel('title'),
        FieldPanel('unit'),
        FieldPanel('description'),
    ]