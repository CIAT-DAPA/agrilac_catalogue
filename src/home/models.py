from django.db import models
from django.contrib.auth.models import AbstractUser
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, FieldRowPanel, InlinePanel
from modelcluster.fields import ParentalKey
from wagtail.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from django import forms
from wagtail.admin.forms import WagtailAdminPageForm
from django.contrib.auth import get_user_model  # Importa get_user_model
from taggit.models import TaggedItemBase
from modelcluster.tags import ClusterTaggableManager
from django.core.paginator import Paginator


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

        # Paginador - Mostramos 5 datasets por página
        paginator = Paginator(datasets, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Estadísticas adicionales sobre datasets
        total_datasets = datasets.count()
        public_datasets = datasets.filter(type_dataset='public').count()
        restricted_datasets = datasets.filter(type_dataset='restricted').count()

        context['total_datasets'] = total_datasets
        context['public_datasets'] = public_datasets
        context['restricted_datasets'] = restricted_datasets
        context['page_obj'] = page_obj

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


#Estas clases son para usar el formato tags/keywords en los campos del form
# class DatasetPageTag(TaggedItemBase):
#     content_object = ParentalKey('DatasetPage', related_name='datasetpage_keywords_tags', on_delete=models.CASCADE)

# class DatasetAuthorsTag(TaggedItemBase):
#     content_object = ParentalKey('DatasetPage', related_name='datasetpage_authors_tags', on_delete=models.CASCADE)

# class DatasetPartnerInstitutionsTag(TaggedItemBase):
#     content_object = ParentalKey('DatasetPage', related_name='datasetpage_partner_institution_tags', on_delete=models.CASCADE)

# class DatasetFileFormatsTag(TaggedItemBase):
#     content_object = ParentalKey('DatasetPage', related_name='datasetpage_file_format_tags', on_delete=models.CASCADE)

class DatasetPage(Page):
    TYPE_DATASET_CHOICES = [
        ('public', 'Público'),
        ('restricted', 'Restringido'),
    ]

    type_dataset = models.CharField(max_length=50, choices=TYPE_DATASET_CHOICES, verbose_name=_("Acceso"))
    identifier = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Identificador"))

    institution_related = models.ForeignKey('InstitutionPage', on_delete=models.SET_NULL, null=True, blank=True, related_name='datasets', verbose_name=_("Institución"))
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
        ], heading="Detalles del Dataset"),
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
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Llama al método save original
        

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
