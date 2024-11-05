from rest_framework.response import Response
from rest_framework.views import APIView
from institutions.models import InstitutionPage  # Asegúrate de que esta es la ruta correcta

class InstitutionListAPIView(APIView):
    def get(self, request):
        institutions = InstitutionPage.objects.live().values(
            'name', 'verified', 'description', 'email', 'phone', 'url_institution', 'owner_user__username'
        )
        return Response(list(institutions))
