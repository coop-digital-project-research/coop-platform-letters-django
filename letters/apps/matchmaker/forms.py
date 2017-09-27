from django.forms import ModelForm, HiddenInput

from .models import Sender


class ExtraAttrsMixin(object):
    extra_attrs = {}

    def __init__(self, *args, **kwargs):
        super(ExtraAttrsMixin, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            attrs = self.extra_attrs.get(field_name, {})

            field.widget.attrs.update(attrs)


class OverrideRequiredMixin(object):
    override_fields_required = []
    override_fields_not_required = []

    def __init__(self, *args, **kwargs):
        super(OverrideRequiredMixin, self).__init__(*args, **kwargs)
        for key in self.fields:
            if key in self.override_fields_not_required:
                self.fields[key].required = False

            elif key in self.override_fields_required:
                self.fields[key].required = True


class SenderForm(ExtraAttrsMixin, OverrideRequiredMixin, ModelForm):
    class Meta:
        model = Sender
        fields = (
            'first_name',
            'age',
            'profile_story',
            'private_story'
        )

        labels = {
            'age': 'Your age',
            'profile_story': 'What was your debt situation?',
        }

        widgets = {
            'private_story': HiddenInput(),
        }

    override_fields_required = ['age']

    extra_attrs = {
        'profile_story': {'rows': '6'},
    }

    # override_fields_required = (
    #     'ticket_type',
    #     'ticket_face_value',
    #     'journey_date',
    #     'journey_departure_time',
    # )
