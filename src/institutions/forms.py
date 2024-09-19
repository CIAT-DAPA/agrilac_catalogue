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
    partner = forms.ModelChoiceField(queryset=CustomUser.objects.all(), label="Seleccionar socio")

    def __init__(self, *args, **kwargs):
        self.institution = kwargs.pop('institution', None)
        super().__init__(*args, **kwargs)

    def save(self):
        from .models import InstitutionMembership  # Importar aquí para evitar importación circular
        partner = self.cleaned_data['partner']
        membership, created = InstitutionMembership.objects.get_or_create(
            user=partner,
            institution=self.institution,
            defaults={'role': 'partner'}
        )
        return membership
