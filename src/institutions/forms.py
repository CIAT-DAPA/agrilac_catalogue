# forms.py en la aplicación home
from django import forms
from wagtail.admin.forms import WagtailAdminPageForm
from django.contrib.auth import get_user_model

class InstitutionPageForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aquí se llama a get_user_model() para definir el queryset del campo owner_user
        self.fields['owner_user'].queryset = get_user_model().objects.all()
