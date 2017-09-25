"""letters URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:

Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
"""
from django.conf.urls import url

from .views import CommunityEnergyGroupDetail, CommunityEnergyGroupMap

urlpatterns = [
    url(
        r'^group/(?P<slug>.*)/$',
        CommunityEnergyGroupDetail.as_view(),
        name='community-energy-group-detail'
    ),
    url(
        r'^$',
        CommunityEnergyGroupMap.as_view(),
        name='community-energy-group-map'
    )
]
