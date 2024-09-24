from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator

from .forms import InstitutionPageForm 
# Create your models here.

class InstitutionPage(Page):
    verified = models.BooleanField(default=False, verbose_name=_("Verificado"))
    name = models.CharField(max_length=255, verbose_name="Nombre")
    owner_user = models.OneToOneField(
        'users.CustomUser',
        on_delete=models.SET_NULL, 
        null=True, blank=True, 
        related_name="owned_institution", 
        verbose_name="Representante principal"
    )
    description = RichTextField(blank=True, verbose_name=_("Descripción"))
    email = models.EmailField(max_length=254, blank=True, verbose_name=_("Email"))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_("Teléfono"))
    url_institution = models.URLField(blank=True, verbose_name=_("URL de la institución"))
    
    institution_memberships = models.ManyToManyField(
        'users.CustomUser',
        through='institutions.InstitutionMembership',
        related_name='institutions',
        verbose_name="Socios",
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('verified'),
        FieldPanel('owner_user'),
        FieldPanel('description'),
        FieldPanel('email'),
        FieldPanel('phone'),
        FieldPanel('url_institution'),
    ]

    base_form_class = InstitutionPageForm  # Asignar el formulario personalizado

    def __str__(self):
        return self.name
    
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
    
    # def can_edit(self, user):
    #     # Los dueños pueden editar la página de su institución
    #     if self.owner_user == user:
    #         return True

    #     # Los socios pueden editar los datasets pero no la página principal de la institución
    #     if self.institution_memberships.filter(user=user).exists():
    #         return False  # No permitir la edición de la página, solo datasets

    #     return False  # Si no es dueño ni socio, no puede editar
    

class InstitutionMembership(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='membership_set')
    institution = models.ForeignKey(InstitutionPage, on_delete=models.CASCADE, related_name='membership_set')
    role = models.CharField(max_length=20, choices=[('partner', 'Partner'), ('owner', 'Owner')], default='partner')
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'institution')

    def __str__(self):
        return f"{self.user} - {self.institution} ({self.role})"
