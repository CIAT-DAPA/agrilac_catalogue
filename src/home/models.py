from django.db import models
from django.contrib.auth.models import User

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField

class HomePage(Page):
    pass

class InstitutionPage(Page):
    verified = models.BooleanField(default=False)
    owner_institution = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='institutions')
    #owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='institutions')

    content_panels = Page.content_panels + [
        FieldPanel('verified'),
        FieldPanel('owner_institution'),
    ]

    def __str__(self):
        return self.title
