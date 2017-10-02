from django.conf.urls import url

from .views import (
    UpdateWriterProfileView, WriterProfileDetailView,
    ReaderChooseWritersView, ReaderConfirmationView, WriterGuideView,
    WriterTrainingView
)

JWT_PATTERN = "[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*"

urlpatterns = [
    url(
        r'^sender/profile/update/(?P<json_web_token>' + JWT_PATTERN + ')/$',
        UpdateWriterProfileView.as_view(),
        name='update-writer-profile'
    ),

    url(
        r'^sender/profile/(?P<json_web_token>' + JWT_PATTERN + ')/$',
        WriterProfileDetailView.as_view(),
        name='writer-profile-detail'
    ),

    url(
        r'^sender/training/(?P<json_web_token>' + JWT_PATTERN + ')/$',
        WriterTrainingView.as_view(),
        name='writer-training'
    ),

    url(
        r'^reader/choose-writers/(?P<json_web_token>' + JWT_PATTERN + ')/$',
        ReaderChooseWritersView.as_view(),
        name='reader-choose-writers'
    ),

    url(
        r'^reader/confirmation/$',
        ReaderConfirmationView.as_view(),
        name='reader-confirmation'
    ),

    url(
        r'^sender/guide/$',
        WriterGuideView.as_view(),
        name='sender-guide'
    ),

]
