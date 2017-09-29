from django.conf.urls import url

from .views import (
    UpdateSenderProfileView, SenderProfileDetailView, ReceiverChooseSendersView
)

JWT_PATTERN = "[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*"

urlpatterns = [
    url(
        r'^sender/profile/update/(?P<json_web_token>' + JWT_PATTERN + ')/$',
        UpdateSenderProfileView.as_view(),
        name='update-sender-profile'
    ),

    url(
        r'^sender/profile/(?P<json_web_token>' + JWT_PATTERN + ')/$',
        SenderProfileDetailView.as_view(),
        name='sender-profile-detail'
    ),

    url(
        r'^receiver/choose-senders/(?P<json_web_token>' + JWT_PATTERN + ')/$',
        ReceiverChooseSendersView.as_view(),
        name='receiver-choose-senders'
    ),

]
