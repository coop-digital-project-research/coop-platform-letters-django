from django.shortcuts import render
from django.views.generic.detail import DetailView

from .models import CommunityEnergyGroup


class CommunityEnergyGroupDetail(DetailView):
    template_name = 'registry/community_energy_group_detail.html'
    model = CommunityEnergyGroup
    context_object_name = 'group'
