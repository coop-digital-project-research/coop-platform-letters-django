from django.forms import ModelForm

from .models import Sender


class SenderForm(ModelForm):
    class Meta:
        model = Sender
        fields = (
            'first_name',
            'profile_story',
            'age',
        )

        # widgets = {
        #     'ticket_type': RadioSelect(),
        #     'journey_date': HTML5DateInput(),
        #     'journey_departure_time': TimeInput(),
        # }

    # override_fields_required = (
    #     'ticket_type',
    #     'ticket_face_value',
    #     'journey_date',
    #     'journey_departure_time',
    # )

    # extra_attrs = {
    #     'ticket_type': {'autofocus': ''},
    #     'journey_date': {'placeholder': 'e.g. {}'.format(pretty_date())},
    #     'journey_departure_time': {
    #         'placeholder': 'e.g. 14:08',
    #         'pattern': "^[0-9]{1,2}[.:]?[0-9]{2}$"
    #     }
    # }
