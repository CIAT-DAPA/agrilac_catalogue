# forms.py en la aplicación home
from django import forms
from wagtail.admin.forms import WagtailAdminPageForm
from django.contrib.auth import get_user_model
from users.models import CustomUser

class InstitutionPageForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aquí se llama a get_user_model() para definir el queryset del campo owner_user
        self.fields['owner_user'].queryset = get_user_model().objects.all()

class AddPartnerForm(forms.Form):
    # Cambiar el campo para aceptar múltiples selecciones de usuarios
    partners = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(), 
        widget=forms.CheckboxSelectMultiple,
        label="Seleccionar socios"
    )

    def __init__(self, *args, **kwargs):
        self.institution = kwargs.pop('institution', None)
        super().__init__(*args, **kwargs)

    def save(self):
        from .models import InstitutionMembership
        partners = self.cleaned_data['partners']  # Obtener los socios seleccionados
        memberships = []
        for partner in partners:
            membership, created = InstitutionMembership.objects.get_or_create(
                user=partner,
                institution=self.institution,
                defaults={'role': 'partner'}
            )
            # Asegurarse de que el rol del usuario se actualice a 'partner'
            if partner.role != 'partner':
                partner.role = 'partner'
                partner.save()
            memberships.append(membership)
        return memberships