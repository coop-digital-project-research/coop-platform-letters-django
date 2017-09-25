from django.conf.urls import url

from .views import UpdateSenderProfileView

urlpatterns = [
    url(
        r'^group/(?P<slug>.*)/$',
        UpdateSenderProfileView.as_view(),
        name='update-sender-profile'
    ),

]
