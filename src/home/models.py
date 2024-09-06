from django.db import models
from django.contrib.auth.models import AbstractUser
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, FieldRowPanel, InlinePanel
from modelcluster.fields import ParentalKey
from wagtail.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from django import forms
from wagtail.admin.forms import WagtailAdminPageForm
from django.contrib.auth import get_user_model  # Importa get_user_model


class HomePage(Page):
    pass

#Para traer los usuario al crear una institución. Esto porque el user se define mas abajo en este archivo
class InstitutionPageForm(WagtailAdminPageForm):
    owner_user = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),        
        required=False,
        label=_("Representante principal"),
        widget=forms.Select
    )

class InstitutionPage(Page):
    verified = models.BooleanField(default=False, verbose_name=_("Verificado"))
    name = models.CharField(max_length=255, verbose_name="Nombre")
    owner_user = models.OneToOneField(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name="owned_institution", verbose_name="Representante principal")
    description = RichTextField(blank=True, verbose_name=_("Descripción"))
    email = models.EmailField(max_length=254, blank=True, verbose_name=_("Email"))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_("Teléfono"))

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('verified'),
        FieldPanel('owner_user'),
        FieldPanel('description'),
        FieldPanel('email'),
        FieldPanel('phone'),
    ]

    base_form_class = InstitutionPageForm  # Asignar el formulario personalizado
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        datasets = self.datasets.all()
        total_datasets = datasets.count()
        public_datasets = datasets.filter(type_dataset='public').count()
        restricted_datasets = datasets.filter(type_dataset='restricted').count()

        context['total_datasets'] = total_datasets
        context['public_datasets'] = public_datasets
        context['restricted_datasets'] = restricted_datasets

        return context

    def __str__(self):
        return self.name
    
    
class CustomUser(AbstractUser):
    VISITOR = 'visitor'
    PARTNER = 'partner'
    OWNER = 'owner'

    ROLE_CHOICES = [
        (VISITOR, 'Visitante'),
        (PARTNER, 'Socio'),
        (OWNER, 'Dueño'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=VISITOR,
        verbose_name="Rol"
    )
    institution = models.ForeignKey('InstitutionPage', on_delete=models.SET_NULL, null=True, blank=True)

    # Especificamos related_name para evitar conflictos
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Cambia el nombre de la relación inversa
        blank=True,
        help_text="Los grupos a los que pertenece el usuario.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Cambia el nombre de la relación inversa
        blank=True,
        help_text="Permisos específicos del usuario.",
        verbose_name="user permissions",
    )

    def save(self, *args, **kwargs):
        # Determina el rol basado en la asociación con una institución
        if self.institution:
            if self.is_institution_owner():
                self.role = self.OWNER
            else:
                self.role = self.PARTNER
        else:
            self.role = self.VISITOR
        super().save(*args, **kwargs)

    def is_institution_owner(self):
        # Si es dueño de la institución
        return self.institution and self.institution.owner_user == self

class Invitation(models.Model):
    invited_user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    institution = models.ForeignKey('InstitutionPage', on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)

    def accept_invitation(self):
        self.invited_user.institution = self.institution
        self.invited_user.role = CustomUser.PARTNER
        self.invited_user.save()
        self.is_accepted = True
        self.save()


class DatasetPage(Page):
    TYPE_DATASET_CHOICES = [
        ('public', 'Público'),
        ('restricted', 'Restringido'),
    ]

    type_dataset = models.CharField(max_length=50, choices=TYPE_DATASET_CHOICES, verbose_name=_("Acceso"))
    institution_related = models.ForeignKey('InstitutionPage', on_delete=models.SET_NULL, null=True, blank=True, related_name='datasets', verbose_name=_("Institución"))
    description = RichTextField(verbose_name=_("Descripción"))

    authors = models.CharField(max_length=255, verbose_name=_("Autores"))
    distributor = models.CharField(max_length=255, verbose_name=_("Distribuidor"))
    data_collection_date = models.DateField(blank=True, null=True, verbose_name=_("Fecha de la colección de datos"))
    data_type = models.CharField(max_length=100, verbose_name=_("Tipo de datos"))
    file_format = models.CharField(max_length=100, verbose_name=_("Formato de archivo"))
    version = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Versión"))
    data_size = models.CharField(max_length=100, verbose_name=_("Tamaño de los datos"))
    intended_use = RichTextField(blank=True, verbose_name=_("Uso previsto"))
    use_limitations = RichTextField(verbose_name=_("Limitaciones de Uso"))

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
    keywords = TaggableManager(verbose_name=_("Palabras clave"), help_text="Agregar múltiples palabras clave separadas por comas")

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('type_dataset'),
            FieldPanel('institution_related'),
            FieldPanel('description'),
            FieldPanel('authors'),
            FieldPanel('distributor'),
            FieldPanel('data_collection_date'),
            FieldPanel('data_type'),
            FieldPanel('file_format'),
            FieldPanel('version'),
            FieldPanel('data_size'),
            FieldPanel('intended_use'),
            FieldPanel('use_limitations'),
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
    
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Llama al método save original
        
        # Guarda los keywords después de guardar el dataset
        if 'keywords' in kwargs:
            self.keywords.set(*kwargs['keywords'], clear=True)
        
        # Imprimir todos los campos, incluyendo keywords
        print("Dataset guardado con los siguientes campos:")
        for field in self._meta.fields:
            field_name = field.name
            field_value = getattr(self, field_name)
            print(f"{field_name}: {field_value}")
        
        # Para los keywords (taggit) debes iterar sobre los tags
        keywords_list = self.keywords.all()
        keywords_str = ', '.join([keyword.name for keyword in keywords_list])
        print(f"Palabras clave: {keywords_str}")

class GeoData(models.Model):
    dataset = ParentalKey(DatasetPage, on_delete=models.CASCADE, related_name='geo_data')

    GEO_TYPE_CHOICES = [
        ('coords', 'Coordenadas geográficas'),
        ('admin_level', 'Nivel administrativo'),
    ]
    
    geo_type = models.CharField(max_length=50, choices=GEO_TYPE_CHOICES, verbose_name=_("Tipo de dato geográfico"))
    latitude = models.FloatField(blank=True, null=True, verbose_name=_("Latitud"))
    longitude = models.FloatField(blank=True, null=True, verbose_name=_("Longitud"))
    csv_file = models.FileField(upload_to='geo_csvs/', blank=True, null=True, verbose_name=_("Archivo CSV de ubicaciones"))
    region_name = models.CharField(max_length=100, blank=True, verbose_name=_("Nombre región"))
    municipality_name = models.CharField(max_length=100, blank=True, verbose_name=_("Nombre municipalidad"))

    panels = [
        FieldPanel('geo_type'),
        MultiFieldPanel([
            FieldPanel('latitude'),
            FieldPanel('longitude'),
        ]),
        MultiFieldPanel([
            FieldPanel('region_name'),
            FieldPanel('municipality_name'),
        ]),
        FieldPanel('csv_file'),
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
