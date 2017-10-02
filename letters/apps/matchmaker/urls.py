from django.conf.urls import url

from .views import (
    UpdateSenderProfileView, SenderProfileDetailView,
    ReceiverChooseSendersView, ReceiverConfirmationView, SenderGuideView,
    SenderTrainingView
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
        r'^sender/training/(?P<json_web_token>' + JWT_PATTERN + ')/$',
        SenderTrainingView.as_view(),
        name='sender-training'
    ),

    url(
        r'^receiver/choose-senders/(?P<json_web_token>' + JWT_PATTERN + ')/$',
        ReceiverChooseSendersView.as_view(),
        name='receiver-choose-senders'
    ),

    url(
        r'^receiver/confirmation/$',
        ReceiverConfirmationView.as_view(),
        name='receiver-confirmation'
    ),

    url(
        r'^sender/guide/$',
        SenderGuideView.as_view(),
        name='sender-guide'
    ),

]
