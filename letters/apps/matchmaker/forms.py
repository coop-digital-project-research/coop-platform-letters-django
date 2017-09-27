from django.forms import ModelForm

from .models import Sender


class ExtraAttrsMixin(object):
    extra_attrs = {}

    def __init__(self, *args, **kwargs):
        super(ExtraAttrsMixin, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            attrs = self.extra_attrs.get(field_name, {})

            field.widget.attrs.update(attrs)


class SenderForm(ExtraAttrsMixin, ModelForm):
    class Meta:
        model = Sender
        fields = (
            'first_name',
            'age',
            'profile_story',
        )

        labels = {
            'age': 'Your age',
            'profile_story': 'What was your debt situation?',
        }

    extra_attrs = {
        'profile_story': {'rows': '6'},
    }
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
