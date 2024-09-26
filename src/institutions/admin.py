# institutions/admin.py
from django.contrib import admin
from .models import InstitutionPage, InstitutionMembership

admin.site.register(InstitutionPage)
admin.site.register(InstitutionMembership)


