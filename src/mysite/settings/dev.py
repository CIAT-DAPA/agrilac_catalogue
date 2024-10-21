from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-nbzdz)3brifqsi3@e=efj%abv35df4d9rvh@=x)*^7sx(i81j&"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

#EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'agrilacdatacatalogue@gmail.com'
EMAIL_HOST_PASSWORD = 'cihv wwim pkz nqjpy'
DEFAULT_FROM_EMAIL = 'noreply@agrilac_data_catalogue.com'


try:
    from .local import *
except ImportError:
    pass
