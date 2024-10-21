# access_requests/models.py
from django.db import models
from users.models import CustomUser
from datasets.models import DatasetPage
from django.utils.translation import gettext_lazy as _

class AccessRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Esperando revisión')),
        ('approved', _('Aprobada')),
        ('denied', _('Denegada')),
    ]
    
    dataset = models.ForeignKey(DatasetPage, on_delete=models.CASCADE, related_name='access_requests')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='access_requests')
    reason = models.TextField(verbose_name=_("Motivo de la solicitud"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    access_response = models.TextField(blank=True, null=True)
    
    # class Meta:
    #     unique_together = ('dataset', 'user')  # Un usuario solo puede solicitar una vez el acceso a un dataset

    def __str__(self):
        return f"{self.user} - {self.dataset.title} ({self.status})"
