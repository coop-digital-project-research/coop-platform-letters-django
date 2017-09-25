from django.shortcuts import render
from django.views.generic.edit import FormView


from .models import Sender


class UpdateSenderProfileView(FormView):
    template_name = 'matchmaker/update_sender_profile.html'
    model = Sender
    context_object_name = 'sender'
