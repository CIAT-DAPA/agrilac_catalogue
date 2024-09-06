from django.db import models
from django.contrib.auth.models import User

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, FieldRowPanel, InlinePanel
from modelcluster.fields import ParentalKey
from wagtail.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager


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

    def get_context(self, request, *args, **kwargs):
        # Llama al contexto original para obtener todo lo que ya tiene
        context = super().get_context(request, *args, **kwargs)
        
        # Calcula los totales
        datasets = self.datasets.all()  # Accede a los datasets relacionados
        total_datasets = datasets.count()
        public_datasets = datasets.filter(type_dataset='public').count()
        restricted_datasets = datasets.filter(type_dataset='restricted').count()
        
        # Añade las variables al contexto
        context['total_datasets'] = total_datasets
        context['public_datasets'] = public_datasets
        context['restricted_datasets'] = restricted_datasets

        return context

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

    # Nuevos campos solicitados
    authors = models.CharField(max_length=255, verbose_name=_("Autores"))  # Obligatorio
    distributor = models.CharField(max_length=255, verbose_name=_("Distribuidor"))  # Obligatorio
    data_collection_date = models.DateField(blank=True, null=True, verbose_name=_("Fecha de la colección de datos"))  # Opcional
    data_type = models.CharField(max_length=100, verbose_name=_("Tipo de datos"))  # Obligatorio
    file_format = models.CharField(max_length=100, verbose_name=_("Formato de archivo"))  # Obligatorio
    version = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Versión"))  # Opcional
    data_size = models.CharField(max_length=100, verbose_name=_("Tamaño de los datos"))  # Obligatorio
    intended_use = RichTextField(blank=True, verbose_name=_("Uso previsto"))  # Opcional
    use_limitations = RichTextField(verbose_name=_("Limitaciones de Uso"))  # Obligatorio

    # Campos adicionales existentes
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

    # Añadir palabras clave usando TaggableManager
    keywords = TaggableManager(verbose_name=_("Palabras clave"), help_text="Agregar múltiples palabras clave separadas por comas")

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('type_dataset'),
            FieldPanel('institution_related'),
            FieldPanel('description'),
            FieldPanel('authors'),  # Nuevo campo
            FieldPanel('distributor'),  # Nuevo campo
            FieldPanel('data_collection_date'),  # Nuevo campo
            FieldPanel('data_type'),  # Nuevo campo
            FieldPanel('file_format'),  # Nuevo campo
            FieldPanel('version'),  # Nuevo campo
            FieldPanel('data_size'),  # Nuevo campo
            FieldPanel('intended_use'),  # Nuevo campo
            FieldPanel('use_limitations'),  # Nuevo campo
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
            FieldPanel('keywords'),  # Aquí ya no necesitas definir el widget
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
    
    geo_type = models.CharField(max_length=50, choices=GEO_TYPE_CHOICES, verbose_name=_("Tipo de dato geográfico"))

    # Campos para Coordenadas geográficas
    latitude = models.FloatField(blank=True, null=True, verbose_name=_("Latitud"))
    longitude = models.FloatField(blank=True, null=True, verbose_name=_("Longitud"))
    
    # Campo de archivo CSV (independiente de la selección de geo_type)
    csv_file = models.FileField(upload_to='geo_csvs/', blank=True, null=True, verbose_name=_("Archivo CSV de ubicaciones"))

    # Campos para Nivel administrativo
    region_name = models.CharField(max_length=100, blank=True, verbose_name=_("Nombre región"))
    municipality_name = models.CharField(max_length=100, blank=True, verbose_name=_("Nombre municipalidad"))

    panels = [
        FieldPanel('geo_type'),
        MultiFieldPanel([
            FieldPanel('latitude'),
            FieldPanel('longitude'),
        ],),
        MultiFieldPanel([
            FieldPanel('region_name'),
            FieldPanel('municipality_name'),
        ],),
        FieldPanel('csv_file'),  # Campo de archivo CSV (visible siempre)
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