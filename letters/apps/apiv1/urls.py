from django.conf.urls import url

from .views import CommunityEnergyGroupListAPIView

urlpatterns = [
    url(
        r'^community-energy-groups/$',
        CommunityEnergyGroupListAPIView.as_view(),
        name='community-energy-groups-list-api'
    )
]
