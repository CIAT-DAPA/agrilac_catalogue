
Si se baja el proyecto sin las migraciones y la bd se deben correr los siguientes comandos:

python manage.py makemigrations

python manage.py migrate

python manage.py runserver

python manage.py createsuperuser

De salir errores de dependencias circulares a la hora de correr makemigrations se debe hacer las migraciones modelo por modelo (comentar y descomentar los modelos en los archivos models.py) de aquellos que no dependan de otros primero.

Si se baja el proyecto con las migraciones y la bd *(recomendado)* solo se debe correr:

python manage.py runserver
