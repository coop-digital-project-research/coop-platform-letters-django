from django.contrib import admin

from .models import CommunityEnergyGroup


@admin.register(CommunityEnergyGroup)
class CommunityEnergyGroupAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'website',
        'contact_email',
        'contact_telephone',
        'postcode',
    )

    readonly_fields = (
        'latitude',
        'longitude',
    )

    search_fields = (
        'name',
        'legal_name',
        'website',
        'postcode',
    )

    ordering = (
        'name',
    )
