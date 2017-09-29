import jwt

from django.conf import settings
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView, ListView
from django.urls import reverse


from .models import Sender, Receiver
from .forms import SenderForm


class GetObjectFromJWT:

    def get_object(self, *args, **kwargs):
        json_web_token = self.kwargs['json_web_token']

        try:
            result = jwt.decode(json_web_token, settings.SECRET_KEY)

        except jwt.exceptions.ExpiredSignatureError:
            # TODO: handle this
            raise

        except jwt.exceptions.InvalidTokenError:
            # TODO: handle more general types of token error
            # https://github.com/jpadilla/pyjwt/blob/master/jwt/exceptions.py
            raise

        return self.object_class.objects.get(uuid=result[self.uuid_key])


class GetSenderObjectFromJWTMixin(GetObjectFromJWT):
    object_class = Sender
    uuid_key = 'sender_uuid'


class GetReceiverObjectFromJWTMixin(GetObjectFromJWT):
    object_class = Receiver
    uuid_key = 'receiver_uuid'


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


class ReceiverChooseSendersView(GetReceiverObjectFromJWTMixin, ListView):
    template_name = 'matchmaker/receiver_choose_senders.html'
    model = Sender
    context_object_name = 'senders'
