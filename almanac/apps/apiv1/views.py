from almanac.apps.registry.models import CommunityEnergyGroup

from rest_framework.generics import ListAPIView

from .serializers import CommunityEnergyGroupSerializer


class CommunityEnergyGroupListAPIView(ListAPIView):
    queryset = CommunityEnergyGroup.objects.all()
    serializer_class = CommunityEnergyGroupSerializer
