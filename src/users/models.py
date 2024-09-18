from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    VISITOR = 'visitor'
    PARTNER = 'partner'
    OWNER = 'owner'

    ROLE_CHOICES = [
        (VISITOR, 'Visitante'),
        (PARTNER, 'Socio'),
        (OWNER, 'Dueño'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=VISITOR,
        verbose_name="Rol"
    )

    # Nombre, Apellido y Correo
    first_name = models.CharField(max_length=30, verbose_name="Nombre")
    last_name = models.CharField(max_length=30, verbose_name="Apellido")
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")

    institution_memberships = models.ManyToManyField(
        'institutions.InstitutionPage',
        through='institutions.InstitutionMembership',
        related_name='members',
        verbose_name="Instituciones donde es miembro"
    )

    # Especificamos related_name diferente para evitar conflictos con AbstractUser
    # groups = models.ManyToManyField(
    #     'auth.Group',
    #     related_name='customuser_groups',  # Cambia el nombre de la relación inversa
    #     blank=True,
    #     help_text="Los grupos a los que pertenece el usuario.",
    #     verbose_name="groups",
    # )
    # user_permissions = models.ManyToManyField(
    #     'auth.Permission',
    #     related_name='customuser_permissions',  # Cambia el nombre de la relación inversa
    #     blank=True,
    #     help_text="Permisos específicos del usuario.",
    #     verbose_name="user permissions",
    # )


