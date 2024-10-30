from django.db import models
from django.core.exceptions import ValidationError
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, FieldRowPanel, InlinePanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from modelcluster.fields import ParentalKey

import csv


from django.utils.translation import gettext_lazy as _

# Create your models here.
class DatasetPage(Page):
    TYPE_DATASET_CHOICES = [
        ('public', 'Público'),
        ('restricted', 'Restringido'),
    ]

    type_dataset = models.CharField(max_length=50, choices=TYPE_DATASET_CHOICES, verbose_name=_("Acceso"))
    identifier = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Identificador"))

    institution_related = models.ForeignKey('institutions.InstitutionPage', on_delete=models.SET_NULL, null=True, blank=True, related_name='datasets', verbose_name=_("Institución"))
    description = RichTextField(features=['h2', 'h3', 'bold', 'italic', 'link'], verbose_name=_("Descripción"))

    authors = models.CharField(max_length=255, verbose_name=_("Autores"), help_text="Agrega autores separados por comas")
    file_format = models.CharField(max_length=255, verbose_name=_("Formato de archivo"), help_text="Agrega formatos separados por comas")    
    version = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Versión"))
    use_license = models.CharField(max_length=255, verbose_name=_("Licencia de Uso"))

    url_dataset = models.URLField(blank=True, verbose_name=_("URL del dataset"))
    citation = models.CharField(max_length=255, blank=True, verbose_name=_("Citación"))
    partner_institutions = models.CharField(max_length=255, verbose_name=_("Instituciones asociadas"), help_text="Agrega instituciones separados por comas")
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
    keywords = models.CharField(max_length=255, verbose_name=_("Palabras clave"), help_text="Agrega palabras clave separadas por comas")    
    access_instructions = RichTextField(features=['h2', 'h3', 'bold', 'italic', 'link'], blank=True, null=True, verbose_name=_("Instrucciones de acceso"))
    GEO_TYPE_CHOICES = [
        ('coords', 'Coordenadas geográficas'),
        ('admin_level', 'Nivel administrativo'),
    ]
    
    geo_type = models.CharField(max_length=50, choices=GEO_TYPE_CHOICES, verbose_name=_("Tipo de dato geográfico"))
    csv_file = models.FileField(upload_to='geo_csvs/', blank=True, null=True, verbose_name=_("Archivo CSV de ubicaciones."), help_text=" Este es un archivo separado por comas y debe tener una columna 'tipo' que debe coincidir con el valor escogido en 'Tipo de dato geográfico'")


    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('type_dataset'),
            FieldPanel('identifier'),
            FieldPanel('institution_related'),
            FieldPanel('description'),
            FieldPanel('authors'),
            FieldPanel('file_format'),
            FieldPanel('version'),
            FieldPanel('use_license'),
        ], heading="Información del Dataset"),
        MultiFieldPanel([
            FieldPanel('url_dataset'),
            FieldPanel('citation'),
            FieldPanel('partner_institutions'),
            FieldRowPanel([
                FieldPanel('start_date'),
                FieldPanel('end_date'),
            ]),
            FieldPanel('upload_frequency'),
            FieldPanel('keywords'),
            FieldPanel('access_instructions'),
        ], heading="Detalles del Dataset"),
        FieldPanel('geo_type'),
        FieldPanel('csv_file'), 
        InlinePanel('geo_data', label="Datos Geográficos"),
        InlinePanel('complementary_info', label="Información Complementaria"),
        InlinePanel('data_dictionary', label="Diccionario de Datos"),
    ]

    def __str__(self):
        return self.title
    
    def get_field_as_list(self, field_name):
        field_value = getattr(self, field_name, "")
        if field_value:
            return field_value.split(",")
        return []
    
    def clean(self):
        # Llama al método clean de la clase base para realizar otras validaciones
        super().clean()

        # Validar el archivo CSV
        if self.csv_file:
            # Leer el contenido del archivo CSV y verificar la columna 'tipo'
            try:
                # Decodificar el archivo como texto y leer el CSV
                self.csv_file.seek(0)  # Asegurarse de leer desde el inicio
                csv_reader = csv.DictReader(self.csv_file.read().decode('utf-8').splitlines())
                
                # Verificar si existe la columna 'tipo'
                if 'tipo' not in csv_reader.fieldnames:
                    raise ValidationError("El archivo CSV debe contener una columna llamada 'tipo'.")

                # Verificar si los valores en la columna 'tipo' coinciden con el valor seleccionado en geo_type
                expected_type = self.geo_type
                for row in csv_reader:
                    if row['tipo'] != expected_type:
                        raise ValidationError(
                            f"El valor en la columna 'tipo' del CSV debe coincidir con '{expected_type}'."
                        )

            except Exception as e:
                raise ValidationError(f"Error al procesar el archivo CSV: {str(e)}")



    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Llama al método save original

    def get_url(self, request=None, current_site=None):
        # Aquí generas la URL en función del ID de la página
        return f'/datasets/dataset/{self.id}/'
        

class GeoData(models.Model):
    dataset = ParentalKey(DatasetPage, on_delete=models.CASCADE, related_name='geo_data')

    latitude = models.FloatField(blank=True, null=True, verbose_name=_("Latitud"))
    longitude = models.FloatField(blank=True, null=True, verbose_name=_("Longitud"))
    region_name = models.CharField(max_length=100, blank=True, verbose_name=_("Nombre región"))
    municipality_name = models.CharField(max_length=100, blank=True, verbose_name=_("Nombre municipalidad"))

    panels = [
        
        MultiFieldPanel([
            FieldPanel('latitude'),
            FieldPanel('longitude'),
        ]),
        MultiFieldPanel([
            FieldPanel('region_name'),
            FieldPanel('municipality_name'),
        ]),
    ]



class ComplementaryInfo(models.Model):
    dataset = ParentalKey(DatasetPage, on_delete=models.CASCADE, related_name='complementary_info')
    feature = models.CharField(max_length=255, verbose_name=_("Característica"))
    description = models.CharField(max_length=255, verbose_name=_("Descripción"))

    panels = [
        FieldPanel('feature'),
        FieldPanel('description'),
    ]


class DataDictionary(models.Model):
    dataset = ParentalKey(DatasetPage, on_delete=models.CASCADE, related_name='data_dictionary')
    field_name = models.CharField(max_length=255, verbose_name=_("Nombre del campo"))
    unit = models.CharField(max_length=100, verbose_name=_("Unidad"))
    description = models.CharField(max_length=255, verbose_name=_("Descripción"))

    panels = [
        FieldPanel('field_name'),
        FieldPanel('unit'),
        FieldPanel('description'),
    ]
