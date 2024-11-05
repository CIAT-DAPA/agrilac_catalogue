from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator
from django.contrib.auth.models import Group

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
        # Agrega permiso al panel de `verified` solo para superusuarios
        FieldPanel('verified', permission='auth.change_user'),  # 'auth.change_user' es solo accesible a superusuarios
        FieldPanel('owner_user'),
        FieldPanel('description'),
        FieldPanel('email'),
        FieldPanel('phone'),
        FieldPanel('url_institution'),
    ]

    base_form_class = InstitutionPageForm  # Asignar el formulario personalizado

    def __str__(self):
        return self.name
    
    
    def save(self, *args, **kwargs):
        previous_owner = None
        if self.pk:
            # Verificar si ya existe un owner previo antes de esta edición
            previous_owner = InstitutionPage.objects.filter(pk=self.pk).first().owner_user

        super().save(*args, **kwargs)
        
        # Si hay un nuevo owner_user, se le asigna el rol 'owner'
        if self.owner_user:
            self.owner_user.role = 'owner'
            self.owner_user.save()

            # Agregar el usuario al grupo "Dueños"
            owners_group, created = Group.objects.get_or_create(name="Dueños")
            owners_group.user_set.add(self.owner_user)

            # Remover el usuario de otros grupos que no correspondan a su rol
            if Group.objects.filter(name="Socios").exists():
                self.owner_user.groups.remove(Group.objects.get(name="Socios"))
            if Group.objects.filter(name="Visitante").exists():
                self.owner_user.groups.remove(Group.objects.get(name="Visitante"))

        # Si había un owner anterior que ha sido cambiado, revierte su rol a 'visitor' o 'partner'
        if previous_owner and previous_owner != self.owner_user:
            previous_owner.role = 'visitor'  # o el rol que consideres adecuado
            previous_owner.save()

            # Agregar el usuario anterior al grupo correspondiente
            if previous_owner.role == 'visitor':
                visitor_group, created = Group.objects.get_or_create(name="Visitante")
                visitor_group.user_set.add(previous_owner)
            elif previous_owner.role == 'partner':
                partner_group, created = Group.objects.get_or_create(name="Socios")
                partner_group.user_set.add(previous_owner)

            # Remover el usuario del grupo "Dueños" si ya no es owner
            if Group.objects.filter(name="Dueños").exists():
                previous_owner.groups.remove(Group.objects.get(name="Dueños"))
        
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
    
    def get_url(self, request=None, current_site=None):
        # Aquí generas la URL en función del ID de la página
        return f'/institutions/institution/{self.id}/'

    

class InstitutionMembership(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='membership_set')
    institution = models.ForeignKey(InstitutionPage, on_delete=models.CASCADE, related_name='membership_set')
    role = models.CharField(max_length=20, choices=[('partner', 'Partner'), ('owner', 'Owner')], default='partner')
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'institution')

    def __str__(self):
        return f"{self.user} - {self.institution} ({self.role})"
