from django.core.mail import send_mail
from django.conf import settings

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

def send_access_request_email(recipient_list, dataset_title, access_response, status):
    trans_es = {
        "approved": "Aprobada",
        "denied": "Denegada"
    }
    subject = f"Solicitud de acceso - {trans_es[status]}"
    message = f"Su solicitud de acceso al dataset '{dataset_title}' ha sido {trans_es[status]}. {access_response}"
    from_email = settings.DEFAULT_FROM_EMAIL
    
    send_mail(subject, message, from_email, recipient_list)
