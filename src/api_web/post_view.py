from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def handle_post_data(request):
    # Obtiene los datos del cuerpo de la solicitud
    data = request.data

    # Valida que se haya enviado la clave 'name' en los datos
    if 'name' not in data:
        return Response({"error": "Falta el campo 'name'"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Procesa los datos (ejemplo simple: retorna el nombre en mayúsculas)
    name = data['name'].upper()

    # Devuelve una respuesta con el dato manipulado
    return Response({"message": f"Hola, {name}"}, status=status.HTTP_200_OK)
