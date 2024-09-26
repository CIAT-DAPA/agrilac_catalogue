# access_requests/forms.py
from django import forms
from .models import AccessRequest

class AccessRequestForm(forms.ModelForm):
    class Meta:
        model = AccessRequest
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Escribe el motivo de la solicitud'}),
        }
