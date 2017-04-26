from rest_framework import serializers
from almanac.apps.registry.models import CommunityEnergyGroup


class CommunityEnergyGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityEnergyGroup
        exclude = (
            'id',
            'postcode_source_url',
            'group_source_url',
        )
