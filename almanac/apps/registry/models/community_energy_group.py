from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class CommunityEnergyGroup(models.Model):

    name = models.CharField(
        help_text=(
            "The name the gorup uses to describe itself. Be careful "
            "to get this right as the URL will be automatically generated "
            "from this value and it's best if URLs don't change."
        ),
        max_length=500
    )

    slug = models.SlugField(
        help_text=(
            "This will form the URL for this group. Try not to change this "
            "as it will break the URL."
        )
    )

    legal_name = models.CharField(
        help_text=(
            "The legal name as registered with companies house or other "
            "registrar, e.g. Liverpool Community Renewables Limited"
        ),
        blank=True, null=True,
        max_length=500
    )

    postcode = models.CharField(
        blank=True, null=True,
        max_length=10
    )

    website = models.URLField(
        blank=True, null=True
    )

    contact_telephone = PhoneNumberField(
        help_text="Use country code, e.g. +44151002233",
        blank=True, null=True
    )

    contact_email = models.EmailField(
        blank=True, null=True
    )

    postcode_source_url = models.URLField(
        help_text="The source URL where the postcode information came from.",
        blank=True, null=True
    )

    group_source_url = models.URLField(
        help_text=(
            "The source URL where the existence of this community energy "
            "group was found."
        ),
        blank=True, null=True
    )
