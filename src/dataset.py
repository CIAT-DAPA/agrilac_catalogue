import os
import django
from flask import Flask, jsonify

# Configurar las variables de entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings.dev')
django.setup()

# Importar los modelos de Django/Wagtail
from wagtail.models import Page


# Crear la app Flask
app = Flask(__name__)

@app.route('/paginas', methods=['GET'])
def obtener_paginas():
    # Consultar todas las páginas de Wagtail
    paginas = Page.objects.all()
    # Crear una lista de títulos de las páginas
    resultado = [{'id': pagina.id, 'titulo': pagina.title} for pagina in paginas]
    for pagina in paginas:
        print(pagina.specific_class)
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)
