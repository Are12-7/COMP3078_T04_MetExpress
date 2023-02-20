from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Village
from .serializers import VillageSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api/villages',
        'GET /api/villages/:id',
        'GET /api/villages/:id'
    ]
    return Response(routes)

# GET ALL VILLAGES


@api_view(['GET'])
def getVillages(request):
    villages = Village.objects.all()
    serializer = VillageSerializer(villages, many=True)
    return Response(serializer.data)


# GET VILLAGE BY ID
@api_view(['GET'])
def getVillage(request, id):
    village = Village.objects.get(id=id)
    serializer = VillageSerializer(village, many=False)
    return Response(serializer.data)
