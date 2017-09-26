import jwt

from django.conf import settings
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView
from django.urls import reverse


from .models import Sender
from .forms import SenderForm


class GetSenderObjectFromJWTMixin:
    def get_object(self, *args, **kwargs):
        json_web_token = self.kwargs['json_web_token']
        result = jwt.decode(json_web_token, settings.SECRET_KEY)
        return Sender.objects.get(uuid=result['sender_uuid'])


class UpdateSenderProfileView(GetSenderObjectFromJWTMixin, UpdateView):
    form_class = SenderForm
    template_name = 'matchmaker/update_sender_profile.html'
    model = Sender
    context_object_name = 'sender'

    def get_success_url(self, **kwargs):
        return reverse(
            'sender-profile-detail',
            kwargs={'json_web_token': self.kwargs['json_web_token']}
        )


class SenderProfileDetailView(GetSenderObjectFromJWTMixin, DetailView):
    template_name = 'matchmaker/sender_profile.html'
    model = Sender
    context_object_name = 'sender'

    def get_context_data(self, **kwargs):
        existing_context = super(
            SenderProfileDetailView, self
        ).get_context_data(**kwargs)

        existing_context.update(
            {'json_web_token': self.kwargs['json_web_token']}
        )
        # raise RuntimeError('{} {}'.format(self.kwargs, kwargs))
        return existing_context
