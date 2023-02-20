from rest_framework.serializers import ModelSerializer
from base.models import Village

# Python object to JSON


class VillageSerializer(ModelSerializer):
    class Meta:
        model = Village
        fields = '__all__'
