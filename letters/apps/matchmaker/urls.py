from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required

from .views import (
    AdminAllocateWriters, AdminTaskListView, AdminTaskListWriterEmailView,
    AdminTaskListReaderEmailView, AdminTaskListAllocationEmailView,
    UpdateWriterProfileView, WriterProfileDetailView, ReaderChooseWritersView,
    ReaderConfirmationView, WriterGuideView, WriterTrainingView,
    ReaderPreLetterSurveyView, WriterTrainingDemoView
)

JWT_PATTERN = "[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*"
UUID_PATTERN = (
    '[0-9a-fA-F]{8}-'
    '[0-9a-fA-F]{4}-'
    '[0-9a-fA-F]{4}-'
    '[0-9a-fA-F]{4}-'
    '[0-9a-fA-F]{12}'
)

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
        r'^sender/training-demo/$',
        WriterTrainingDemoView.as_view(),
        name='writer-training-demo'
    ),

    url(
        r'^sender/guide/$',
        WriterGuideView.as_view(),
        name='writer-guide'
    ),

    url(
        r'^reader/choose-writers/(?P<json_web_token>' + JWT_PATTERN + ')/$',
        ReaderChooseWritersView.as_view(),
        name='reader-choose-writers'
    ),

    url(
        r'^reader/confirmation/(?P<json_web_token>' + JWT_PATTERN + ')/$',
        ReaderConfirmationView.as_view(),
        name='reader-confirmation'
    ),

    url(
        r'^reader/pre-letter-survey/(?P<json_web_token>' + JWT_PATTERN + ')/$',
        ReaderPreLetterSurveyView.as_view(),
        name='reader-pre-letter-survey'
    ),

    url(
        r'^admin/tasks/$',
        staff_member_required(AdminTaskListView.as_view()),
        name='admin-task-list'
    ),

    url(
        r'^admin/tasks/emails/writer/(?P<email_slug>.+)'
        '/(?P<pk>{uuid})/$'.format(uuid=UUID_PATTERN),
        staff_member_required(AdminTaskListWriterEmailView.as_view()),
        name='admin-task-list-writer-email',
    ),

    url(
        r'^admin/tasks/emails/reader/(?P<email_slug>.+)'
        '/(?P<pk>{uuid})/$'.format(uuid=UUID_PATTERN),
        staff_member_required(AdminTaskListReaderEmailView.as_view()),
        name='admin-task-list-reader-email',
    ),

    url(
        r'^admin/tasks/emails/allocation/(?P<email_slug>.+)'
        '/(?P<pk>\d\d\d-\d\d\d)/$',
        staff_member_required(AdminTaskListAllocationEmailView.as_view()),
        name='admin-task-list-allocation-email',
    ),

    url(
        r'^admin/allocate-writers/$',
        staff_member_required(AdminAllocateWriters.as_view()),
        name='admin-allocate-writers'
    ),

]
